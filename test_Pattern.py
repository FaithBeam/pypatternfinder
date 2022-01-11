from unittest import TestCase
from pypatternfinder.pattern import transform, find, find_all, scan, Byte, Nibble
from pypatternfinder.signature import Signature


class Test(TestCase):
    def test_transform(self):
        pattern = transform("456?89?B")
        self.assertEqual(len(pattern), 4)
        self.assertEqual(pattern[0].n1.data, 4)
        self.assertFalse(pattern[0].n1.wildcard)
        self.assertEqual(pattern[0].n2.data, 5)
        self.assertFalse(pattern[0].n2.wildcard)
        self.assertEqual(pattern[1].n1.data, 6)
        self.assertFalse(pattern[1].n1.wildcard)
        self.assertEqual(pattern[1].n2.data, 5)
        self.assertTrue(pattern[1].n2.wildcard)
        self.assertEqual(pattern[2].n1.data, 8)
        self.assertFalse(pattern[2].n1.wildcard)
        self.assertEqual(pattern[2].n2.data, 9)
        self.assertFalse(pattern[2].n2.wildcard)
        self.assertEqual(pattern[3].n1.data, 8)
        self.assertTrue(pattern[3].n1.wildcard)
        self.assertEqual(pattern[3].n2.data, 11)
        self.assertFalse(pattern[3].n2.wildcard)

    def test_find(self):
        pattern = transform("456?89?B")

        data = bytearray([0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF])
        result, offset = find(data, pattern)
        self.assertTrue(result)
        self.assertEqual(offset, 2)

        data = bytearray([0x01, 0x23, 0x45, 0x66, 0x89, 0x6B, 0xCD, 0xEF])
        result, offset = find(data, pattern)
        self.assertTrue(result)
        self.assertEqual(offset, 2)

        data = bytearray([0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11])
        result, offset = find(data, pattern)
        self.assertFalse(result)
        self.assertEqual(offset, -1)

    def test_find_all(self):
        pattern = transform("11")

        data = bytearray([0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11])
        result, offsets_found = find_all(data, pattern)
        self.assertTrue(result)
        self.assertCountEqual(offsets_found, [0, 1, 2, 3, 4, 5, 6, 7])

        data = bytearray([0x11, 0x11, 0x11, 0xFF, 0x11, 0x11, 0x11, 0x11])
        result, offsets_found = find_all(data, pattern)
        self.assertTrue(result)
        self.assertCountEqual(offsets_found, [0, 1, 2, 4, 5, 6, 7])

    def test_scan(self):
        pattern = transform("456?89?B")
        data = bytearray([0x01, 0x23, 0x45, 0x66, 0x89, 0x6B, 0xCD, 0xEF])
        signature = Signature()
        signature.name = "First"
        signature.pattern = pattern

        signatures = [signature]
        found_signatures = scan(data, signatures)

        self.assertEqual(len(found_signatures), 1)
        self.assertEqual(found_signatures[0].name, "First")
        self.assertEqual(found_signatures[0].found_offset, 2)

    def test_byte(self):
        my_byte = Byte()
        self.assertIsInstance(my_byte, Byte)

    def test_nibble(self):
        my_nibble = Nibble()
        self.assertIsInstance(my_nibble, Nibble)
