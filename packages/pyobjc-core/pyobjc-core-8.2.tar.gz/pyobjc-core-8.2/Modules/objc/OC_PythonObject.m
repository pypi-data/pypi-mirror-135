/* Copyright (c) 1996,97 by Lele Gaifax. All Rights Reserved
 * Copyright 2002, 2003 Ronald Oussoren, Jack Jansen
 * Copyright 2003-2021 Ronald Oussoren
 *
 * This software may be used and distributed freely for any purpose
 * provided that this notice is included unchanged on any and all
 * copies. The author does not warrant or guarantee this software in
 * any way.
 */

#include "pyobjc.h"

/* XXX: Are these includes still needed */
#include "compile.h" /* From Python */
#include <dlfcn.h>

#include <stdarg.h>

#import <Foundation/NSDictionary.h>
#import <Foundation/NSEnumerator.h>
#import <Foundation/NSInvocation.h>
#import <Foundation/NSMethodSignature.h>
#import <Foundation/NSObject.h>
#import <Foundation/NSString.h>

#if MAC_OS_X_VERSION_MAX_ALLOWED >= MAC_OS_X_VERSION_10_3
#import <Foundation/NSKeyValueObserving.h>
#endif

#import "OC_PythonUnicode.h"

NS_ASSUME_NONNULL_BEGIN

/* XXX: Is this still needed? */
extern NSString* const NSUnknownKeyException; /* Radar #3336042 */

@implementation OC_PythonObject
+ (id<NSObject> _Nullable)objectWithPythonObject:(PyObject*)obj
{
    id instance;
    if (likely(PyObjCObject_Check(obj))) {
        instance = PyObjCObject_GetObject(obj);
    } else {
        instance = [[[self alloc] initWithPyObject:obj] autorelease];
    }
    return instance;
}

- (id _Nullable)initWithPyObject:(PyObject*)obj
{
    /* XXX: Why check for NULL here? */
    if (pyObject) {
        PyObjC_UnregisterObjCProxy(pyObject, self);
    }

    PyObjC_RegisterObjCProxy(obj, self);

    SET_FIELD_INCREF(pyObject, obj);

    return self;
}

- (oneway void)release
{
    /* See comment in OC_PythonUnicode */
    if (unlikely(!Py_IsInitialized())) {
        [super release];
        return;
    }

    PyObjC_BEGIN_WITH_GIL
        @try {
            [super release];

        } @catch (NSObject* exc) {
            PyObjC_LEAVE_GIL;
            @throw;
        }
    PyObjC_END_WITH_GIL
}

- (void)dealloc
{
    if (unlikely(!Py_IsInitialized())) {
        [super dealloc];
        return;
    }

    PyObjC_BEGIN_WITH_GIL
        PyObjC_UnregisterObjCProxy(pyObject, self);
        Py_CLEAR(pyObject);

    PyObjC_END_WITH_GIL

    [super dealloc];
}

- (id)copyWithZone:(NSZone* _Nullable)zone
{
    (void)zone;
    NSObject* result;
    PyObject* copy;

    if (PyObjC_CopyFunc == NULL) {
        [NSException raise:NSInvalidArgumentException
                    format:@"cannot copy Python objects"];

    } else {
        PyObjC_BEGIN_WITH_GIL
            copy = PyObjC_CallCopyFunc(pyObject);
            if (copy == NULL) {
                PyObjC_GIL_FORWARD_EXC();
            }

            if (depythonify_python_object(copy, &result) == -1) {
                Py_DECREF(copy);
                PyObjC_GIL_FORWARD_EXC();
            }
            Py_DECREF(copy);

        PyObjC_END_WITH_GIL
    }

    if (result) {
        [result retain];
    }
    return result;
}

- (id)copy
{
    return [self copyWithZone:NULL];
}

/* Undocumented method used by NSLog, this seems to work. */
- (NSString*)_copyDescription
{
    return [[self description] copy];
}

- (NSString*)description
{
    PyObject* repr;

    if (pyObject == NULL)
        return @"no python object";

    PyObjC_BEGIN_WITH_GIL

        repr = PyObject_Repr(pyObject);

        if (repr) {
            int       err;
            NSString* result;

            /* XXX: use other function */
            err = depythonify_c_value(@encode(id), repr, &result);
            Py_DECREF(repr);
            if (err == -1) {
                PyObjC_GIL_FORWARD_EXC();
            }

            PyObjC_GIL_RETURN(result);
        } else {
            PyObjC_GIL_FORWARD_EXC();
        }

    PyObjC_END_WITH_GIL

    /* not reached */
    return @"a python object";
}

- (void)doesNotRecognizeSelector:(SEL)aSelector
{
    [NSException raise:NSInvalidArgumentException
                format:@"%@ does not recognize -%s", self, sel_getName(aSelector)];
}

static inline PyObject* _Nullable check_argcount(PyObject* pymethod, Py_ssize_t argcount)
{
    PyCodeObject* func_code;

    if (PyFunction_Check(pymethod)) {
        func_code = (PyCodeObject*)PyFunction_GetCode(pymethod);
        if (argcount == func_code->co_argcount) {
            return pymethod;
        }

    } else if (PyMethod_Check(pymethod)) {
        func_code = (PyCodeObject*)PyFunction_GetCode(PyMethod_Function(pymethod));
        if (argcount == func_code->co_argcount - 1) {
            return pymethod;
        }
    }

    return NULL;
}

/*#F If the Python object @var{obj} implements a method whose name matches
  the Objective-C selector @var{aSelector} and accepts the correct number
  of arguments, return that method, otherwise NULL. */
static PyObject* _Nullable get_method_for_selector(PyObject* obj, SEL aSelector)
{
    const char* meth_name;
    char        pymeth_name[256];
    Py_ssize_t  argcount;
    PyObject*   pymethod;
    const char* p;
    PyObject*   result;

    if (!aSelector) {
        [NSException raise:NSInvalidArgumentException format:@"nil selector"];
    }

    meth_name = sel_getName(aSelector);

    for (argcount = 0, p = meth_name; *p; p++) {
        if (*p == ':') {
            argcount++;
        }
    }

    const char* py_meth_name =
        PyObjC_SELToPythonName(aSelector, pymeth_name, sizeof(pymeth_name));
    if (py_meth_name == NULL) {
        return NULL;
    }
    pymethod = PyObject_GetAttrString(obj, py_meth_name);
    if (pymethod == NULL) {
        return NULL;
    }

    result = check_argcount(pymethod, argcount);
    if (result == NULL) {
        Py_DECREF(pymethod);
    }
    return result;
}

- (BOOL)respondsToSelector:(SEL)aSelector
{
    PyObject*    m;
    Method*      methods;
    unsigned int method_count;
    unsigned int i;
    void*        cookie;

    /*
     * We cannot rely on NSProxy, it doesn't implement most of the
     * NSObject interface anyway.
     */

    cookie  = NULL;
    methods = class_copyMethodList(object_getClass(self), &method_count);
    if (methods == NULL) {
        return NO;
    }

    for (i = 0; i < method_count; i++) {
        if (sel_isEqual(method_getName(methods[i]), aSelector)) {
            free(methods);
            return YES;
        }
    }
    free(methods);

    PyObjC_BEGIN_WITH_GIL
        m = get_method_for_selector(pyObject, aSelector);

        if (m) {
            Py_DECREF(m);
            PyObjC_GIL_RETURN(YES);
        } else {
            PyErr_Clear();
            PyObjC_GIL_RETURN(NO);
        }

    PyObjC_END_WITH_GIL
}

+ (NSMethodSignature* _Nullable)methodSignatureForSelector:(SEL)sel
{
    Method m;

    m = class_getClassMethod(self, sel);
    if (m) {
        /* A real Objective-C method */
        const char* typestr = method_getTypeEncoding(m);
        if (typestr == NULL) {
            return nil;
        }
        return [NSMethodSignature signatureWithObjCTypes:typestr];
    }

    [NSException
         raise:NSInvalidArgumentException
        format:@"Class %s: no such selector: %s", class_getName(self), sel_getName(sel)];
    return nil;
}

- (NSMethodSignature* _Nullable)methodSignatureForSelector:(SEL)sel
{
    /* We can't call our superclass implementation, NSProxy just raises
     * an exception.
     */

    char*         encoding;
    PyObject*     pymethod;
    PyCodeObject* func_code;
    Py_ssize_t    argcount;
    Class         cls;
    Method        m;

    cls = object_getClass(self);
    m   = class_getInstanceMethod(cls, sel);
    if (m) {
        /* A real Objective-C method */
        const char* typestr = method_getTypeEncoding(m);
        if (typestr == NULL) {
            return nil;
        }
        return [NSMethodSignature signatureWithObjCTypes:typestr];
    }

    PyObjC_BEGIN_WITH_GIL

        pymethod = get_method_for_selector(pyObject, sel);
        if (!pymethod) {
            PyErr_Clear();
            PyObjC_LEAVE_GIL;
            /* XXX: Use @throw */
            [NSException raise:NSInvalidArgumentException
                        format:@"Class %s: no such selector: %s",
                               object_getClassName(self), sel_getName(sel)];
        }

        if (PyMethod_Check(pymethod)) {
            func_code = (PyCodeObject*)PyFunction_GetCode(PyMethod_Function(pymethod));
            argcount  = func_code->co_argcount - 1;

        } else {
            func_code = (PyCodeObject*)PyFunction_GetCode(pymethod);
            argcount  = func_code->co_argcount;
        }
        Py_DECREF(pymethod);

        encoding = alloca(argcount + 4);
        memset(encoding, '@', argcount + 3);
        encoding[argcount + 3] = '\0';
        encoding[2]            = ':';

    PyObjC_END_WITH_GIL

    return [NSMethodSignature signatureWithObjCTypes:encoding];
}

- (BOOL)_forwardNative:(NSInvocation*)invocation
{
    SEL aSelector = [invocation selector];

    if (sel_isEqual(aSelector, @selector(description))) {
        id res = [self description];
        [invocation setReturnValue:&res];

        return YES;

    } else if (sel_isEqual(aSelector, @selector(_copyDescription))) {
        id res = [self _copyDescription];
        [invocation setReturnValue:&res];

        return YES;

    } else if (sel_isEqual(aSelector, @selector(respondsToSelector:))) {
        SEL  sel;
        BOOL b;

        [invocation getArgument:&sel atIndex:2];

        b = [self respondsToSelector:sel];
        [invocation setReturnValue:&b];

        return YES;

    } else if (sel_isEqual(aSelector, @selector(classForKeyedArchiver))) {
        Class c;

        c = [self classForKeyedArchiver];
        [invocation setReturnValue:&c];

        return YES;

    } else if (sel_isEqual(aSelector, @selector(classForArchiver))) {
        Class c;

        c = [self classForArchiver];
        [invocation setReturnValue:&c];

        return YES;

    } else if (sel_isEqual(aSelector, @selector(classForCoder))) {
        Class c;

        c = [self classForCoder];
        [invocation setReturnValue:&c];

        return YES;

    } else if (sel_isEqual(aSelector, @selector(classForPortCoder))) {
        Class c;

        c = [self classForPortCoder];
        [invocation setReturnValue:&c];

        return YES;

    } else if (sel_isEqual(aSelector, @selector(replacementObjectForKeyedArchiver:))) {
        NSObject*        c;
        NSKeyedArchiver* archiver;

        [invocation getArgument:&archiver atIndex:2];
        c = [self replacementObjectForKeyedArchiver:archiver];
        [invocation setReturnValue:&c];

        return YES;

    } else if (sel_isEqual(aSelector, @selector(replacementObjectForArchiver:))) {
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wdeprecated-declarations"

        NSObject*   c;
        NSArchiver* archiver;

        [invocation getArgument:&archiver atIndex:2];
        c = [self replacementObjectForArchiver:archiver];
        [invocation setReturnValue:&c];

#pragma clang diagnostic pop

        return YES;

    } else if (sel_isEqual(aSelector, @selector(replacementObjectForCoder:))) {
        NSObject* c;
        NSCoder*  archiver;

        [invocation getArgument:&archiver atIndex:2];
        c = [self replacementObjectForCoder:archiver];
        [invocation setReturnValue:&c];

        return YES;

    } else if (sel_isEqual(aSelector, @selector(replacementObjectForPortCoder:))) {
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wdeprecated-declarations"

        NSObject*    c;
        NSPortCoder* archiver;

        [invocation getArgument:&archiver atIndex:2];
        c = [self replacementObjectForPortCoder:archiver];
        [invocation setReturnValue:&c];

#pragma clang diagnostic pop

        return YES;

    } else if (sel_isEqual(aSelector, @selector(copy))) {
        NSObject* c;

        c = [self copy];
        [invocation setReturnValue:&c];

        return YES;

    } else if (sel_isEqual(aSelector, @selector(copyWithZone:))) {
        NSObject* c;
        NSZone*   zone;

        [invocation getArgument:&zone atIndex:2];
        c = [self copyWithZone:zone];
        [invocation setReturnValue:&c];

        return YES;
    }

    return NO;
}

- (void)forwardInvocation:(NSInvocation*)invocation
{
    NSMethodSignature* msign     = [invocation methodSignature];
    SEL                aSelector = [invocation selector];
    PyObject*          pymethod;
    PyObject*          result;
    const char*        rettype = [msign methodReturnType];
    int                err;
    PyObject*          args = NULL;
    unsigned int       i;
    NSUInteger         argcount;
    Py_ssize_t         retsize;
    char*              retbuffer;

    if ([self _forwardNative:invocation]) {
        return;
    }

    PyObjC_BEGIN_WITH_GIL

        retsize = PyObjCRT_SizeOfType(rettype);
        if (retsize == -1) {
            PyObjC_GIL_FORWARD_EXC();
        }

        retbuffer = alloca(retsize);

        /* XXX: Convert this to vectorcall, needs with some
         * luck this can be done without creating a bound
         * method.
         */
        pymethod = get_method_for_selector(pyObject, aSelector);

        if (!pymethod) {
            PyObjC_LEAVE_GIL;

            [self doesNotRecognizeSelector:aSelector];
            return;
        }

        argcount = [msign numberOfArguments];
        args     = PyTuple_New(argcount - 2);
        if (args == NULL) {
            Py_DECREF(pymethod);
            PyObjC_GIL_FORWARD_EXC();
        }
        for (i = 2; i < argcount; i++) {
            const char* argtype;
            char*       argbuffer;
            Py_ssize_t  argsize;
            PyObject*   pyarg;

            @try {
                argtype = [msign getArgumentTypeAtIndex:i];
            } @catch (NSObject* exc) {
                PyObjC_LEAVE_GIL;
                @throw;
            }

            argsize = PyObjCRT_SizeOfType(argtype);
            if (argsize == -1) {
                Py_DECREF(args);
                Py_DECREF(pymethod);
                PyObjC_GIL_FORWARD_EXC();
            }
            argbuffer = alloca(argsize);

            Py_BEGIN_ALLOW_THREADS
                @try {
                    [invocation getArgument:argbuffer atIndex:i];

                } @catch (NSObject* exc) {
                    PyObjC_LEAVE_GIL;
                    @throw;
                }
            Py_END_ALLOW_THREADS

            pyarg = pythonify_c_value(argtype, argbuffer);
            if (pyarg == NULL) {
                Py_DECREF(args);
                Py_DECREF(pymethod);
                PyObjC_GIL_FORWARD_EXC();
            }

            PyTuple_SET_ITEM(args, i - 2, pyarg);
        }
        result = PyObject_CallObject(pymethod, args);
        Py_DECREF(args);
        args = NULL;
        Py_DECREF(pymethod);
        pymethod = NULL;

        if (result == NULL) {
            PyObjC_GIL_FORWARD_EXC();
            return;
        }

        err = depythonify_c_value(rettype, result, retbuffer);
        Py_DECREF(result);
        if (err == -1) {
            PyObjC_GIL_FORWARD_EXC();
        } else {
            Py_BEGIN_ALLOW_THREADS
                @try {
                    [invocation setReturnValue:retbuffer];

                } @catch (NSObject* localException) {
                    PyObjC_LEAVE_GIL;
                    @throw;
                }
            Py_END_ALLOW_THREADS
        }

    PyObjC_END_WITH_GIL
}

/* XXX: Remove this method */
- (PyObject*)pyObject
{
    return pyObject;
}

- (PyObject* _Nullable)__pyobjc_PythonObject__
{
    PyObjC_BEGIN_WITH_GIL
        /* XXX: This is a bit too magic. Can pyObject ever be NULL?
         * and why not return None in that case?
         */
        if (pyObject == NULL) {
            PyObject* r = PyObjCObject_New(self, PyObjCObject_kDEFAULT, YES);
            PyObjC_GIL_RETURN(r);
        } else {
            Py_XINCREF(pyObject);
            PyObjC_GIL_RETURN(pyObject);
        }
    PyObjC_END_WITH_GIL
}
- (PyObject*)__pyobjc_PythonTransient__:(int*)cookie
{
    PyObjC_BEGIN_WITH_GIL
        *cookie = 0;
        Py_INCREF(pyObject);
    PyObjC_END_WITH_GIL
    return pyObject;
}

+ (PyObject* _Nullable)__pyobjc_PythonTransient__:(int*)cookie
{
    PyObject* rval;

    PyObjC_BEGIN_WITH_GIL
        rval    = PyObjCClass_New([OC_PythonObject class]);
        *cookie = 0;
    PyObjC_END_WITH_GIL

    return rval;
}

/*
 * Implementation for Key-Value Coding.
 *
 * Because this is a subclass of NSProxy we must implement all of the protocol,
 * and cannot rely on the implementation in our superclass.
 *
 */

+ (BOOL)useStoredAccessor
{
    return YES;
}

+ (BOOL)accessInstanceVariablesDirectly
{
    return YES;
}

/* XXX:
 * - Try to use PyImport_ImportModuleLevel here
 * - Preferably switch to an objc.option for setting
 *   the function.
 */
static PyObject* _Nullable getModuleFunction(char* modname, char* funcname)
{
    PyObject* func;
    PyObject* name;
    PyObject* mod;

    name = PyUnicode_FromString(modname);
    if (name == NULL) {
        return NULL;
    }

    mod = PyImport_Import(name);
    if (mod == NULL) {
        Py_DECREF(name);
        return NULL;
    }
    func = PyObject_GetAttrString(mod, funcname);
    if (func == NULL) {
        Py_DECREF(name);
        Py_DECREF(mod);
        return NULL;
    }
    Py_DECREF(name);
    Py_DECREF(mod);

    return func;
}

/*
 *  Call PyObjCTools.KeyValueCoding.getKey to get the value for a key
 */
- (id)valueForKey:(NSString*)key
{
    static PyObject* getKeyFunc = NULL;

    PyObject* keyName;
    PyObject* val;
    id        res = nil;

    PyObjC_BEGIN_WITH_GIL

        if (getKeyFunc == NULL) {
            getKeyFunc = getModuleFunction("PyObjCTools.KeyValueCoding", "getKey");
            if (getKeyFunc == NULL) {
                PyObjC_GIL_FORWARD_EXC();
            }
        }

        keyName = id_to_python(key);
        if (keyName == NULL) {
            PyObjC_GIL_FORWARD_EXC();
        }

        PyObject* args[3] = {NULL, pyObject, keyName};

        val = PyObject_Vectorcall(getKeyFunc, args + 1,
                                  2 | PY_VECTORCALL_ARGUMENTS_OFFSET, NULL);
        Py_DECREF(keyName);
        if (val == NULL) {
            PyObjC_GIL_FORWARD_EXC();
        }

        if (depythonify_c_value(@encode(id), val, &res) < 0) {
            Py_DECREF(val);
            PyObjC_GIL_FORWARD_EXC();
        }
        Py_DECREF(val);

    PyObjC_END_WITH_GIL

    return res;
}

- (id _Nullable)storedValueForKey:(NSString*)key
{
    return [self valueForKey:key];
}

- (void)takeValue:value forKey:(NSString*)key
{
    [self setValue:value forKey:key];
}

- (void)setValue:value forKey:(NSString*)key
{
    static PyObject* setKeyFunc = NULL;

    PyObject* keyName;
    PyObject* pyValue;
    PyObject* val;

    PyObjC_BEGIN_WITH_GIL

        if (setKeyFunc == NULL) {
            setKeyFunc = getModuleFunction("PyObjCTools.KeyValueCoding", "setKey");
            if (setKeyFunc == NULL) {
                PyObjC_GIL_FORWARD_EXC();
            }
        }

        keyName = id_to_python(key);
        if (keyName == NULL) {
            PyObjC_GIL_FORWARD_EXC();
        }

        pyValue = id_to_python(value);
        if (pyValue == NULL) {
            Py_DECREF(keyName);
            PyObjC_GIL_FORWARD_EXC();
        }

        PyObject* args[4] = {NULL, pyObject, keyName, pyValue};

        val = PyObject_Vectorcall(setKeyFunc, args + 1,
                                  3 | PY_VECTORCALL_ARGUMENTS_OFFSET, NULL);
        Py_DECREF(keyName);
        Py_DECREF(pyValue);
        if (val == NULL) {
            PyObjC_GIL_FORWARD_EXC();
        }

        Py_DECREF(val);

    PyObjC_END_WITH_GIL
}

- (void)takeStoredValue:value forKey:(NSString*)key
{
    [self takeValue:value forKey:key];
}

- (NSDictionary* _Nullable)valuesForKeys:(NSArray*)keys
{
    NSMutableDictionary* result;
    NSEnumerator*        enumerator;
    id                   aKey, aValue;

    enumerator = [keys objectEnumerator];
    result     = [NSMutableDictionary dictionary];

    while ((aKey = [enumerator nextObject]) != NULL) {
        aValue = [self valueForKey:aKey];
        [result setObject:aValue forKey:aKey];
    }

    return result;
}

- (id _Nullable)valueForKeyPath:(NSString*)keyPath
{
    static PyObject* getKeyFunc = NULL;

    PyObject* keyName;
    PyObject* val;
    id        res = nil;

    PyObjC_BEGIN_WITH_GIL

        if (getKeyFunc == NULL) {
            getKeyFunc = getModuleFunction("PyObjCTools.KeyValueCoding", "getKeyPath");
            if (getKeyFunc == NULL) {
                PyObjC_GIL_FORWARD_EXC();
            }
        }

        keyName = id_to_python(keyPath);
        if (keyName == NULL) {
            PyObjC_GIL_FORWARD_EXC();
        }

        PyObject* args[3] = {NULL, pyObject, keyName};

        val = PyObject_Vectorcall(getKeyFunc, args + 1,
                                  2 | PY_VECTORCALL_ARGUMENTS_OFFSET, NULL);
        Py_DECREF(keyName);
        if (val == NULL) {
            PyObjC_GIL_FORWARD_EXC();
        }

        if (depythonify_python_object(val, &res) < 0) {
            Py_DECREF(val);
            PyObjC_GIL_FORWARD_EXC();
        }
        Py_DECREF(val);

    PyObjC_END_WITH_GIL

    return res;
}

- (void)takeValue:value forKeyPath:(NSString*)keyPath
{
    [self setValue:value forKeyPath:keyPath];
}

- (void)setValue:value forKeyPath:(NSString*)keyPath
{
    static PyObject* setKeyFunc = NULL;

    PyObject* keyName;
    PyObject* pyValue;
    PyObject* val;

    PyObjC_BEGIN_WITH_GIL

        if (setKeyFunc == NULL) {
            setKeyFunc = getModuleFunction("PyObjCTools.KeyValueCoding", "setKeyPath");
            if (setKeyFunc == NULL) {
                PyObjC_GIL_FORWARD_EXC();
            }
        }

        keyName = id_to_python(keyPath);
        if (keyName == NULL) {
            PyObjC_GIL_FORWARD_EXC();
        }

        pyValue = id_to_python(value);
        if (pyValue == NULL) {
            Py_DECREF(keyName);
            PyObjC_GIL_FORWARD_EXC();
        }

        PyObject* args[4] = {NULL, pyObject, keyName, pyValue};

        val = PyObject_Vectorcall(setKeyFunc, args + 1,
                                  3 | PY_VECTORCALL_ARGUMENTS_OFFSET, NULL);
        Py_DECREF(keyName);
        Py_DECREF(pyValue);
        if (val == NULL) {
            PyObjC_GIL_FORWARD_EXC();
        }

        Py_DECREF(val);

    PyObjC_END_WITH_GIL
}

- (void)takeValuesFromDictionary:(NSDictionary*)aDictionary
{
    [self setValuesForKeysWithDictionary:aDictionary];
}

- (void)setValuesForKeysWithDictionary:(NSDictionary*)aDictionary
{
    NSEnumerator* enumerator = [aDictionary keyEnumerator];
    id            aKey;
    id            aValue;

    while ((aKey = [enumerator nextObject]) != NULL) {
        aValue = [aDictionary objectForKey:aKey];
        [self takeValue:aValue forKey:aKey];
    }
}

- (void)unableToSetNilForKey:(NSString*)key
{
    [NSException raise:NSUnknownKeyException format:@"cannot set Nil for key: %@", key];
}

- (void)handleQueryWithUnboundKey:(NSString*)key
{
    [self valueForUndefinedKey:key];
}

- (void)valueForUndefinedKey:(NSString*)key
{
    [NSException raise:NSUnknownKeyException format:@"query for unknown key: %@", key];
}

- (void)handleTakeValue:value forUnboundKey:(NSString*)key
{
    [self setValue:value forUndefinedKey:key];
}

- (void)setValue:value forUndefinedKey:(NSString*)key
{
    [NSException raise:NSUnknownKeyException
                format:@"setting unknown key: %@ to <%@>", key, value];
}

#if MAC_OS_X_VERSION_MAX_ALLOWED >= MAC_OS_X_VERSION_10_3
- (void)addObserver:(NSObject*)observer
         forKeyPath:(NSString*)keyPath
            options:(NSKeyValueObservingOptions)options
            context:(void*)context
{
    NSLog(@"*** Ignoring *** %@ for '%@' (of %@ with %#lx in %p).\n",
          NSStringFromSelector(_cmd), keyPath, observer, (long)options, context);
    return;
}
- (void)removeObserver:(NSObject*)observer forKeyPath:(NSString*)keyPath
{
    NSLog(@"*** Ignoring *** %@ for '%@' (of %@).", NSStringFromSelector(_cmd), keyPath,
          observer);
}
#endif

/* NSObject protocol */
- (NSUInteger)hash
{
    Py_hash_t rval;

    PyObjC_BEGIN_WITH_GIL
        rval = PyObject_Hash([self pyObject]);
        if (rval == -1) {
            PyErr_Clear();
            rval = (NSUInteger)[self pyObject];
        }

    PyObjC_END_WITH_GIL

    return rval;
}

- (BOOL)isEqual:(id)anObject
{
    if (anObject == nil) {
        return NO;

    } else if (self == anObject) {
        return YES;
    }

    PyObjC_BEGIN_WITH_GIL
        PyObject* otherPyObject = id_to_python(anObject);
        if (otherPyObject == NULL) {
            PyErr_Clear();
            PyObjC_GIL_RETURN(NO);
        }
        if (otherPyObject == [self pyObject]) {
            PyObjC_GIL_RETURN(YES);
        }
        switch (PyObject_RichCompareBool([self pyObject], otherPyObject, Py_EQ)) {
        case -1:
            PyErr_Clear();
        case 0:
            PyObjC_GIL_RETURN(NO);
            break;
        default:
            PyObjC_GIL_RETURN(YES);
        }
    PyObjC_END_WITH_GIL
}

/* NSObject methods */
- (NSComparisonResult)compare:(id)other
{
    if (other == nil) {
        [NSException raise:NSInvalidArgumentException format:@"nil argument"];
    } else if (self == other) {
        return NSOrderedSame;
    }
    PyObjC_BEGIN_WITH_GIL
        PyObject* otherPyObject = id_to_python(other);
        if (otherPyObject == NULL) {
            PyObjC_GIL_FORWARD_EXC();
        }
        if (otherPyObject == [self pyObject]) {
            PyObjC_GIL_RETURN(NSOrderedSame);
        }
        int r;
        if (PyObjC_Cmp([self pyObject], otherPyObject, &r) == -1) {
            PyObjC_GIL_FORWARD_EXC();
        }
        NSComparisonResult rval;
        switch (r) {
        case -1:
            rval = NSOrderedAscending;
            break;
        case 0:
            rval = NSOrderedSame;
            break;
        default:
            rval = NSOrderedDescending;
        }
        PyObjC_GIL_RETURN(rval);
    PyObjC_END_WITH_GIL
}

/*
 * Support of the NSCoding protocol
 */
- (void)encodeWithCoder:(NSCoder*)coder
{
    PyObjC_encodeWithCoder(pyObject, coder);
}

/*
 * Helper method for initWithCoder, needed to deal with
 * recursive objects (e.g. o.value = o)
 */
- (void)pyobjcSetValue:(NSObject*)other
{
    PyObjC_BEGIN_WITH_GIL
        PyObject* value = id_to_python(other);

        SET_FIELD(pyObject, value);
    PyObjC_END_WITH_GIL
}

- (id _Nullable)initWithCoder:(NSCoder*)coder
{
    pyObject = NULL;

    if (PyObjC_Decoder != NULL) {
        PyObjC_BEGIN_WITH_GIL
            PyObject* cdr = id_to_python(coder);
            PyObject* setValue;
            PyObject* selfAsPython;
            PyObject* v;

            if (cdr == NULL) {
                PyObjC_GIL_FORWARD_EXC();
            }

            selfAsPython = PyObjCObject_New(self, 0, YES);
            if (selfAsPython == NULL) {
                PyObjC_GIL_FORWARD_EXC();
            }
            setValue = PyObject_GetAttrString(selfAsPython, "pyobjcSetValue_");

            v = PyObjC_CallDecoder(cdr, setValue);
            Py_DECREF(cdr);
            Py_DECREF(setValue);
            Py_DECREF(selfAsPython);

            if (v == NULL) {
                PyObjC_GIL_FORWARD_EXC();
            }

            /* To make life more interesting the correct proxy
             * type for 'v' might not be OC_PythonObject, in particular
             * when introducing new proxy types in new versions
             * of PyObjC, and in some error cases.
             */
            NSObject* temp;
            if (depythonify_python_object(v, &temp) == -1) {
                Py_DECREF(v);
                PyObjC_GIL_FORWARD_EXC();
            }

            if (temp != (NSObject*)self) {
                [temp retain];
                [self release];
                self = (OC_PythonObject*)temp;
            }
            Py_DECREF(pyObject);

        PyObjC_END_WITH_GIL

        return self;

    } else {
        [NSException raise:NSInvalidArgumentException
                    format:@"decoding Python objects is not supported"];
        return nil;
    }
}

- (id _Nullable)awakeAfterUsingCoder:(NSCoder*)coder __attribute__((__unused__))
{
    return self;
}

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wdeprecated-declarations"

- (NSObject*)replacementObjectForArchiver:(NSArchiver*)archiver
    __attribute__((__unused__))
{
    return (NSObject*)self;
}

- (NSObject*)replacementObjectForPortCoder:(NSPortCoder*)archiver
    __attribute__((__unused__))
{
    return (NSObject*)self;
}
#pragma clang diagnostic pop

- (NSObject*)replacementObjectForKeyedArchiver:(NSKeyedArchiver*)archiver
    __attribute__((__unused__))
{
    return (NSObject*)self;
}

- (NSObject*)replacementObjectForCoder:(NSCoder*)archiver __attribute__((__unused__))
{
    return (NSObject*)self;
}

- (Class)classForArchiver
{
    return [OC_PythonObject class];
}

- (Class)classForKeyedArchiver
{
    return [OC_PythonObject class];
}

+ (Class)classForUnarchiver
{
    return [OC_PythonObject class];
}

+ (Class)classForKeyedUnarchiver
{
    return [OC_PythonObject class];
}

- (Class)classForCoder
{
    return [OC_PythonObject class];
}

- (Class)classForPortCoder
{
    return [OC_PythonObject class];
}

/* NOTE: NSProxy does not implement isKindOfClass on Leopard, therefore we
 * have to provide it ourself.
 *
 * Luckily that's kind of easy, we know the entiry class hierarchy and also
 * know there are no subclasses.
 */
- (BOOL)isKindOfClass:(Class)aClass
{
    if (aClass == [NSProxy class] || aClass == [OC_PythonObject class]) {
        return YES;
    }
    return NO;
}

/*
 * This is needed to be able to add a python object to a
 * NSArray and then use array.description()
 */
- (BOOL)isNSArray__
{
    return NO;
}
- (BOOL)isNSDictionary__
{
    return NO;
}
- (BOOL)isNSSet__
{
    return NO;
}
- (BOOL)isNSNumber__
{
    return NO;
}
- (BOOL)isNSData__
{
    return NO;
}
- (BOOL)isNSDate__
{
    return NO;
}
- (BOOL)isNSString__
{
    return NO;
}
- (BOOL)isNSValue__
{
    return NO;
}

+ (id _Nullable)classFallbacksForKeyedArchiver
{
    return nil;
}

/*
 * Fake implementation for _cfTypeID, which gets called by
 * system frameworks on some occasions.
 */
static BOOL     haveTypeID = NO;
static CFTypeID _NSObjectTypeID;

- (CFTypeID)_cfTypeID
{
    if (haveTypeID) {
        NSObject* obj   = [[NSObject alloc] init];
        _NSObjectTypeID = CFGetTypeID((CFTypeRef)obj);
        [obj release];
        haveTypeID = YES;
    }
    return _NSObjectTypeID;
}

@end /* OC_PythonObject class implementation */

void
PyObjC_encodeWithCoder(PyObject* pyObject, NSCoder* coder)
{
    if (PyObjC_Encoder != NULL) {
        PyObjC_BEGIN_WITH_GIL
            PyObject* cdr = id_to_python(coder);
            if (cdr == NULL) {
                PyObjC_GIL_FORWARD_EXC();
            }

            PyObject* args[3] = {NULL, pyObject, cdr};

            PyObject* r = PyObject_Vectorcall(PyObjC_Encoder, args + 1,
                                              2 | PY_VECTORCALL_ARGUMENTS_OFFSET, NULL);
            Py_DECREF(cdr);
            if (r == NULL) {
                PyObjC_GIL_FORWARD_EXC();

            } else {
                Py_DECREF(r);
            }

        PyObjC_END_WITH_GIL

    } else {
        [NSException raise:NSInvalidArgumentException
                    format:@"encoding Python objects is not supported"];
    }
}

NS_ASSUME_NONNULL_END
