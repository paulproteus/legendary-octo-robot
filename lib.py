# Write functions in here.
#
# You can also execute this file if you want; it'll run the unit tests for library functions.

def decode_ascii(bytes):
    # Try AND-ing against top bit set to on. If the result has the top
    # bit set after an AND, then the input had the top bit set to
    # 1. So reject if so.
    if len(bytes) > 1:
        raise ValueError("this one does one byte at a time")
    mask_ = 0b10000000
    first_char = ord(bytes[0])
    masked = mask_ & first_char
    if masked != mask_:
        return unicode(chr(first_char), 'ascii')
    raise ValueError()

def decode_two_byte_utf8(bytes):
    mask_ = 0b11100000
    valid = 0b11000000
    first_char = ord(bytes[0])
    masked = mask_ & first_char
    if masked == valid:
        print 'This should be 2-char utf-8'
        first_chunk = ord(bytes[0]) -  0b11000000
        second_chunk = ord(bytes[1]) - 0b10000000
        codepoint = (first_chunk << 6) + (second_chunk)
        return unichr(codepoint)
    raise ValueError("Too bad, did not decode")

def decode_three_byte_utf8(bytes):
    if len(bytes) != 3:
        raise ValueError('skip me')
    mask_ = 0b11110000
    valid = 0b11100000
    first_char = ord(bytes[0])
    masked = mask_ & first_char
    if masked == valid:
        print 'This should be 3-char utf-8'
        first_chunk = ord(bytes[0]) -  0b11100000
        second_chunk = ord(bytes[1]) - 0b10000000
        third_chunk = ord(bytes[2]) -  0b10000000
        codepoint = (first_chunk << 15) + (second_chunk << 6) + third_chunk
        if codepoint < 0xffff:
            print 'hee hee'
        return unichr(codepoint)
    raise ValueError("Too bad, did not decode")

def decode_normal_utf8(bytes):
    return bytes.decode('utf-8')

def decode_overlong_two_bytes_utf8(bytes):
    pass

def decode_overlong_three_bytes_utf8(bytes):
    pass

def decode_overlong_four_bytes_utf8(bytes):
    pass



TRY_TO_DECODE_WITH_THESE = [
    decode_ascii,
    decode_two_byte_utf8,
    decode_three_byte_utf8,
]

def actual_main():
    import sys
    encoded = ''
    decoded = u''
    while True:
        encoded += sys.stdin.read(1)
        if len(encoded) > 8:
            print 'Got this so far:', decoded.encode('utf-8')
            print 'AKA            :', repr(decoded)
            raise ValueError("Proceeded with these bytes " +
                             repr(encoded) + "that no function could decode.")
        for fn in TRY_TO_DECODE_WITH_THESE:
            try:
                decoded = fn(encoded)
                encoded = ''
            except:
                pass

###
import unittest

class Tests(unittest.TestCase):
    def test_ascii(self):
        self.assertEqual(u'a', decode_ascii('a'))

    def test_two_byte_utf8(self):
        self.assertEqual(u"\u00E9", decode_two_byte_utf8('\xc3\xa9'))

    def test_three_byte_utf8(self):
        self.assertEqual(u"\u0800", decode_three_byte_utf8('\xe0\xa0\x80'))

if __name__ == '__main__':
    unittest.main()
