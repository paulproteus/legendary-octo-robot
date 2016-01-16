###
import unittest
from lib import *

class Tests(unittest.TestCase):
    def test_ascii(self):
        self.assertEqual(u'a', decode_ascii('a'))

    def test_two_byte_utf8(self):
        self.assertEqual(u"\u00E9", decode_two_byte_utf8('\xc3\xa9'))

    def test_three_byte_utf8(self):
        self.assertEqual(u"\u0800", decode_three_byte_utf8('\xe0\xa0\x80'))

    def test_four_byte_utf8(self):
        self.assertEqual(u"\U0001F800", decode_four_byte_utf8('\xF0\x9F\xA0\x80'))


if __name__ == '__main__':
    unittest.main()
