
#include "Python.h"
#include "pyobjc-api.h"
#include <stdarg.h>

#import <Foundation/Foundation.h>

@interface OC_ArrayInt : NSObject {
}
@end

@implementation OC_ArrayInt
+ (id)getNthElement:(NSArray*)array offset:(NSUInteger)offset
{
    @try {
        return [array objectAtIndex:offset];
    } @catch (NSException* exc) {
        return exc;
    }
}

+ (id)getSub:(NSArray*)array range:(NSRange)range
{
    static id buf[100];

    if (range.length > 100) {
        return @"too many items";
    }

    [array getObjects:buf range:range];
    return [NSArray arrayWithObjects:buf count:range.length];
}

+ (id)setNthElement:(NSMutableArray*)array offset:(NSUInteger)offset replacement:(id)value
{
    @try {
        [array replaceObjectAtIndex:offset withObject:value];
        return nil;
    } @catch (NSException* exc) {
        return exc;
    }
}

+ (id)addToArray:(NSMutableArray*)array value:(id)value
{
    @try {
        [array addObject:value];
        return nil;
    } @catch (NSException* exc) {
        return exc;
    }
}

+ (id)insertIntoArray:(NSMutableArray*)array offset:(NSUInteger)offset value:(id)value
{
    @try {
        [array insertObject:value atIndex:offset];
        return nil;
    } @catch (NSException* exc) {
        return exc;
    }
}

+ (id)removeLast:(NSMutableArray*)array
{
    @try {
        [array removeLastObject];
        return nil;
    } @catch (NSException* exc) {
        return exc;
    }
}
+ (id)remove:(NSMutableArray*)array offset:(NSUInteger)offset
{
    @try {
        [array removeObjectAtIndex:offset];
        return nil;
    } @catch (NSException* exc) {
        return exc;
    }
}

@end

static PyMethodDef mod_methods[] = {{0, 0, 0, 0}};

static struct PyModuleDef mod_module = {
    PyModuleDef_HEAD_INIT, "arrayint", NULL, 0, mod_methods, NULL, NULL, NULL, NULL};

PyObject* PyInit_arrayint(void);

PyObject* __attribute__((__visibility__("default"))) PyInit_arrayint(void)
{
    PyObject* m;

    m = PyModule_Create(&mod_module);
    if (!m) {
        return NULL;
    }

    PyObjC_ImportAPI(m);

    if (PyModule_AddObject(m, "OC_ArrayInt", PyObjC_IdToPython([OC_ArrayInt class]))
        < 0) {
        return NULL;
    }

    return m;
}
