try:
    import ctypes
except ImportError:
    ctypes = None

import objc
from PyObjCTest.pointersupport import object_capsule, opaque_capsule
from PyObjCTools.TestSupport import TestCase, skipUnless

OpaqueType = objc.createOpaquePointerType("OpaqueType", b"^{OpaqueType}", None)


class TestProxySupport(TestCase):
    def test_cobject_roundtrip(self):
        arr = objc.lookUpClass("NSArray").array()

        p = arr.__cobject__()
        self.assertEqual(type(p).__name__, "PyCapsule")
        self.assertIn("objc.__object__", repr(p))
        # Note:

        v = objc.objc_object(cobject=p)
        self.assertIs(v, arr)

    @skipUnless(ctypes is not None, "requires ctypes")
    def test_voidp_roundtrip(self):
        arr = objc.lookUpClass("NSArray").array()

        p = arr.__c_void_p__()
        self.assertIsInstance(p, ctypes.c_void_p)
        self.assertEqual(p.value, objc.pyobjc_id(arr))

        v = objc.objc_object(c_void_p=p)
        self.assertIs(v, arr)

    @skipUnless(ctypes is not None, "requires ctypes")
    def test_voidp_using_ctypes(self):
        lib = ctypes.CDLL(
            "/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation"
        )
        func = lib.CFStringCreateWithCString
        func.restype = ctypes.c_void_p
        func.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]

        kCFStringEncodingISOLatin1 = 0x0201
        ct_obj = func(None, b"hello world", kCFStringEncodingISOLatin1)

        value = objc.objc_object(c_void_p=ct_obj)
        self.assertIsInstance(value, objc.pyobjc_unicode)
        self.assertEqual(objc.pyobjc_id(value.nsstring()), ct_obj)

    def test_pyobjc_id_invalid(self):
        with self.assertRaisesRegex(
            TypeError,
            r"(function missing required argument 'obj' \(pos 1\))|(Required argument 'obj' \(pos 1\) not found)",
        ):
            objc.pyobjc_id()

        with self.assertRaisesRegex(TypeError, r"not an Objective-C object"):
            objc.pyobjc_id(42)

    def test_opaque_capsule(self):
        cap = opaque_capsule()

        value = OpaqueType(cobject=cap)
        self.assertIsInstance(value, OpaqueType)
        self.assertEqual(value.__pointer__, 1234)

        with self.assertRaisesRegex(
            ValueError, "PyCapsule_GetPointer called with incorrect name"
        ):
            OpaqueType(cobject=object_capsule())
        with self.assertRaisesRegex(TypeError, "cobject' argument is not a PyCapsule"):
            OpaqueType(cobject=42)

    @skipUnless(ctypes is not None, "requires ctypes")
    def test_opaque_ctypes(self):
        ptr = ctypes.c_void_p(0xABCD)

        value = OpaqueType(c_void_p=ptr)
        self.assertIsInstance(value, OpaqueType)
        self.assertEqual(value.__pointer__, 0xABCD)

        value = OpaqueType(c_void_p=0xDEFA)
        self.assertIsInstance(value, OpaqueType)
        self.assertEqual(value.__pointer__, 0xDEFA)

    def test_object_capsule(self):
        NSObject = objc.lookUpClass("NSObject")
        cap = object_capsule()

        value = NSObject(cobject=cap)
        self.assertIsInstance(value, NSObject)

        with self.assertRaisesRegex(
            ValueError, "PyCapsule_GetPointer called with incorrect name"
        ):
            NSObject(cobject=opaque_capsule())
        with self.assertRaisesRegex(TypeError, "cobject' argument is not a PyCapsule"):
            NSObject(cobject=42)
