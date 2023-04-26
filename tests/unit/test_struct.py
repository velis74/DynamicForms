from django.test import TestCase

from dynamicforms.struct import Struct, StructDefault


class StructClassTest(TestCase):
    def test_empty_init(self):
        s = Struct()
        s.test = 1
        self.assertEqual(len(s.__to_dict__()), 1, "Struct should have only one member item")
        self.assertEqual(s.test, 1, "Struct.test member should have value == 1")
        self.assertEqual(repr(s), "Struct: {'test': 1}")

    def test_data_init(self):
        s = Struct(dict(test=1))
        self.assertEqual(len(s.__to_dict__()), 1, "Struct should have only one member item")
        self.assertEqual(s.test, 1, "Struct.test member should have value == 1")

    def test_kwds_init(self):
        s = Struct(test=1)
        self.assertEqual(len(s.__to_dict__()), 1, "Struct should have only one member item")
        self.assertEqual(s.test, 1, "Struct.test member should have value == 1")

    def test_wrapper_init(self):
        s = Struct(dict(obj=dict(test=1, lst=[1, 2, 3])))
        self.assertEqual(len(s.__to_dict__()), 1, "Struct should have only one member item")
        self.assertEqual("obj" in s.__to_dict__(), True, 'Struct should have a "test" member')
        self.assertEqual(len(s.__to_dict__()["obj"]), 2, "Struct.test should have only one member item")
        self.assertEqual(s.obj.test, 1, "Struct.obj.test member should have value == 1")

    def test_clone(self):
        s = Struct(dict(obj=dict(test=1, lst=[1, 2, 3])))
        sc1 = s.clone()
        sc1.obj.test = 2
        sc1.obj.lst.append(4)
        sc2 = s.clone(a=2)
        self.assertEqual(len(s.__to_dict__()), 1, "Struct should have only one member item")
        self.assertEqual("obj" in s.__to_dict__(), True, 'Struct should have a "test" member')
        self.assertEqual(len(s.__to_dict__()["obj"]), 2, "Struct.test should have only one member item")
        self.assertEqual(s.obj.test, 1, "Struct.obj.test member should have value == 1")

        self.assertEqual(len(sc1.__to_dict__()), 1, "Struct sc1 should have only one member item")
        self.assertEqual("obj" in sc1.__to_dict__(), True, 'Struct sc1 should have a "test" member')
        self.assertEqual(len(sc1.__to_dict__()["obj"]), 2, "Struct sc1.test should have only one member item")
        self.assertEqual(sc1.obj.test, 2, "Struct sc1.obj.test member should have value == 2")

        self.assertEqual(len(sc2.__to_dict__()), 2, "Struct sc2 should have only one member item")
        self.assertEqual("obj" in sc2.__to_dict__(), True, 'Struct sc2 should have a "test" member')
        self.assertEqual(len(sc2.__to_dict__()["obj"]), 2, "Struct sc2.test should have only one member item")
        self.assertEqual(sc2.obj.test, 1, "Struct sc2.obj.test member should have value == 1")
        self.assertEqual(len(sc2.obj.lst), 3, "Struct sc2.obj.lst member should have 3 members")
        self.assertEqual(sc2.a, 2, "Struct sc2.a member should have value == 2")

    def test_struct_default(self):
        s = StructDefault(a=1, _default_=15)
        self.assertEqual(len(s.__to_dict__()), 2, "StructDefault should have two member items")
        self.assertEqual(hasattr(s, "test"), True, 'StructDefault should have a "test" member')
        self.assertEqual(s.test, 15, "StructDefault.test should have value == 15")
