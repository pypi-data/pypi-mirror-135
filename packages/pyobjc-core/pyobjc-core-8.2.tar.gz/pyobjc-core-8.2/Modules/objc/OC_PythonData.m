#include "pyobjc.h"

NS_ASSUME_NONNULL_BEGIN

@implementation OC_PythonData

+ (instancetype _Nullable)dataWithPythonObject:(PyObject*)v
{
    return [[[self alloc] initWithPythonObject:v] autorelease];
}

- (instancetype _Nullable)initWithPythonObject:(PyObject*)v
{
    self = [super init];
    if (unlikely(self == nil))
        return nil;

    if (!PyObject_CheckBuffer(v)) {
        PyErr_SetString(PyExc_TypeError, "not a buffer");
        [self release];
        return nil;
    }

    SET_FIELD_INCREF(value, v);
    return self;
}

- (PyObject*)__pyobjc_PythonObject__
{
    Py_INCREF(value);
    return value;
}

- (PyObject*)__pyobjc_PythonTransient__:(int*)cookie
{
    *cookie = 0;
    Py_INCREF(value);
    return value;
}

+ (BOOL)supportsSecureCoding
{
    return NO;
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
        } @catch (NSException* exc) {
            PyObjC_LEAVE_GIL;
            [exc raise];
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
        PyObjC_UnregisterObjCProxy(value, self);
        Py_XDECREF(value);

    PyObjC_END_WITH_GIL

    [super dealloc];
}

- (NSUInteger)length
{
    NSUInteger rval;

    PyObjC_BEGIN_WITH_GIL
        OCReleasedBuffer* temp = [[OCReleasedBuffer alloc] initWithPythonBuffer:value
                                                                       writable:NO];
        if (temp == nil) {
            @try {
                [self release];
            } @catch (NSException* exc) {
                PyObjC_LEAVE_GIL;
                [exc raise];
            }
            PyErr_Clear();
            PyObjC_GIL_RETURN(0);
        }
        rval = [temp length];
        [temp release];

    PyObjC_END_WITH_GIL
    return rval;
}

- (const void*)bytes
{
    void* rval;

    PyObjC_BEGIN_WITH_GIL
        OCReleasedBuffer* temp = [[OCReleasedBuffer alloc] initWithPythonBuffer:value
                                                                       writable:NO];
        rval                   = [temp buffer];
        [temp autorelease];

    PyObjC_END_WITH_GIL
    return rval;
}

- (Class)classForCoder
{
    if (PyBytes_CheckExact(value)) {
        return [NSData class];

    } else if (PyByteArray_CheckExact(value)) {
        return [NSMutableData class];

    } else {
        return [OC_PythonData class];
    }
}

- (Class _Nullable)classForKeyedArchiver
{
    return [OC_PythonData class];
}

- (void)encodeWithCoder:(NSCoder*)coder
{

    PyObjC_BEGIN_WITH_GIL
        @try {
            if (PyBytes_CheckExact(value)) {
                if ([coder allowsKeyedCoding]) {
                    [coder encodeInt32:3 forKey:@"pytype"];
                }
                [super encodeWithCoder:coder];
            } else if (PyByteArray_CheckExact(value)) {
                if ([coder allowsKeyedCoding]) {
                    [coder encodeInt32:4 forKey:@"pytype"];
                }
                [super encodeWithCoder:coder];
            } else {
                if ([coder allowsKeyedCoding]) {
                    [coder encodeInt32:2 forKey:@"pytype"];
                } else {
                    int v = 2;
                    [coder encodeValueOfObjCType:@encode(int) at:&v];
                }

                PyObjC_encodeWithCoder(value, coder);
            }
        } @catch (NSException* exc) {
            PyObjC_LEAVE_GIL;
            [exc raise];
        }
    PyObjC_END_WITH_GIL
}

/*
 * Helper method for initWithCoder, needed to deal with
 * recursive objects (e.g. o.value = o)
 */
- (void)pyobjcSetValue:(NSObject*)other
{
    PyObjC_BEGIN_WITH_GIL
        PyObject* v = id_to_python(other);

        SET_FIELD(value, v);
    PyObjC_END_WITH_GIL
}

- (id _Nullable)initWithCoder:(NSCoder*)coder
{
    int v;

    if ([coder allowsKeyedCoding]) {
        v = [coder decodeInt32ForKey:@"pytype"];

    } else {
        [coder decodeValueOfObjCType:@encode(int) at:&v];
    }
    if (v == 1) {
        /* Backward compatibility:
         * PyObjC up to version 3 used this type to archive instances of bytes
         */
        self = [super init];
        if (unlikely(self == nil))
            return nil;

        const void* bytes;
        NSUInteger  length;

        if ([coder allowsKeyedCoding]) {
            bytes = [coder decodeBytesForKey:@"pybytes" returnedLength:&length];

        } else {
            bytes = [coder decodeBytesWithReturnedLength:&length];
        }

        PyObjC_BEGIN_WITH_GIL
            value = PyBytes_FromStringAndSize(bytes, length);
            if (value == NULL) {
                @try {
                    [super dealloc]; /* XXX: Is this correct? */
                } @catch (NSException* exc) {
                    PyObjC_LEAVE_GIL;
                    [exc raise];
                }
                PyObjC_GIL_FORWARD_EXC();
            }

        PyObjC_END_WITH_GIL;
        return self;

    } else if (v == 2) {
        if (PyObjC_Decoder != NULL) {
            PyObjC_BEGIN_WITH_GIL
                PyObject* cdr = id_to_python(coder);
                PyObject* setValue;
                PyObject* selfAsPython;
                PyObject* v2;

                if (cdr == NULL) {
                    PyObjC_GIL_FORWARD_EXC();
                }

                selfAsPython = PyObjCObject_New(self, 0, YES);
                if (selfAsPython == NULL) {
                    PyObjC_GIL_FORWARD_EXC();
                }
                setValue = PyObject_GetAttrString(selfAsPython, "pyobjcSetValue_");

                v2 = PyObjC_CallDecoder(cdr, setValue);
                Py_DECREF(cdr);
                Py_DECREF(setValue);
                Py_DECREF(selfAsPython);

                if (v2 == NULL) {
                    PyObjC_GIL_FORWARD_EXC();
                }

                SET_FIELD(value, v2);

                self = PyObjC_FindOrRegisterObjCProxy(value, self);

            PyObjC_END_WITH_GIL

            return self;

        } else {
            [NSException raise:NSInvalidArgumentException
                        format:@"decoding Python objects is not supported"];
            return nil;
        }

    } else if (v == 3) {
        return [super initWithCoder:coder];

    } else if (v == 4) {
        PyObjC_BEGIN_WITH_GIL
            value = PyByteArray_FromStringAndSize(NULL, 0);
            if (value == NULL) {
                PyObjC_GIL_FORWARD_EXC();
            }

        PyObjC_END_WITH_GIL
        return [super initWithCoder:coder];

    } else {
        [NSException raise:NSInvalidArgumentException
                    format:@"encoding Python data objects is not supported"];
    }
    return self;
}

- (id)initWithData:(NSData*)data
{
    return [self initWithBytes:[data bytes] length:[data length]];
}

- (id)initWithBytes:(const void* _Nullable)bytes length:(NSUInteger)length
{
    PyObjC_BEGIN_WITH_GIL
        if (length > PY_SSIZE_T_MAX) {
            PyErr_SetString(PyExc_ValueError, "Trying to decode a too long data object");
            PyObjC_GIL_FORWARD_EXC();
        }

        if (value != NULL && PyByteArray_CheckExact(value)) {
            if (PyByteArray_Resize(value, length) < 0) {
                PyObjC_GIL_FORWARD_EXC();
            }
            memcmp(PyByteArray_AS_STRING(value), bytes, length);
        } else {
            value = PyBytes_FromStringAndSize(bytes, length);
            if (value == NULL) {
                PyObjC_GIL_FORWARD_EXC();
            }
        }
    PyObjC_END_WITH_GIL

    return self;
}

/* Ensure that we can be unarchived as a generic data object by pure ObjC
 * code.
 */
+ (NSArray*)classFallbacksForKeyedArchiver
{
    return [NSArray arrayWithObject:@"NSData"];
}

@end /* implementation OC_PythonData */

NS_ASSUME_NONNULL_END
