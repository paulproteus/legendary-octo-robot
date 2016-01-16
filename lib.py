# Write functions in here.
#
# You can also execute this file if you want; it'll run the unit tests for library functions.

import warnings

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
    mask_ = 0b11110000
    valid = 0b11100000
    first_char = ord(bytes[0])
    masked = mask_ & first_char
    if masked == valid:
        print 'This should be 3-char utf-8'
        first_chunk = ord(bytes[0]) -  0b11100000
        second_chunk = ord(bytes[1]) - 0b10000000
        third_chunk = ord(bytes[2]) - 0b10000000
        codepoint = (first_chunk << 15) + (second_chunk << 8) + third_chunk
        return unichr(codepoint)
    raise ValueError("Too bad, did not decode")

def _validate(length, n, i, b_ord):
    if length != 0:
        warnings.warn("Starting new codepoint of length %d with %d left in sequence at index %d" % (n, length, i))
    first_bit = 5 - n
    if b_ord & (1 << first_bit) == 0:
        warnings.warn('Overlong code-point at position %d' % (i))
    
    

def decode_weird_utf8(bytes):
    chars = []
    codepoint = 0
    length = 0
    for i, b in enumerate(bytes):
        b_ord = ord(b)
        if b_ord & 0b10000000 == 0b00000000:
            chars.append(chr(b_ord & 0b01111111))
        elif b_ord & 0b11000000 == 0b10000000:
            codepoint = (codepoint << 6) + (b_ord & 0b00111111)
            length -= 1
            if length == 0:
                chars.append(unichr(codepoint))
                codepoint = 0
            if length < 0:
                warnings.warn("Too-long intermediate char sequence at %d" % i)
        elif b_ord & 0b11100000 == 0b11000000:
            codepoint = (codepoint << 5) + (b_ord & 0b00011111)
            _validate(length, 1, i, b_ord)
            length = 1
        elif b_ord & 0b11110000 == 0b11100000:
            codepoint = (codepoint << 4) + (b_ord & 0b00001111)
            _validate(length, 2, i, b_ord)
            length = 2
        elif b_ord & 0b11111000 == 0b11110000:
            codepoint = (codepoint << 3) + (b_ord & 0b00000111)
            _validate(length, 3, i, b_ord)
            length = 3
        elif b_ord & 0b11111100 == 0b11111000:
            codepoint = (codepoint << 2) + (b_ord & 0b00000011)
            _validate(length, 4, i, b_ord)
            length = 4
        elif b_ord & 0b11111110 == 0b11111100:
            codepoint = (codepoint << 1) + (b_ord & 0b00000001)
            _validate(length, 5, i, b_ord)
            length = 5
        else:
            warnings.warn("Unrecognized code-point: %d" % b_ord)

    if codepoint != 0:
        warnings.warn("Finished with partial character %d, with %d codepoints to go" % (codepoint, length))
        
    print
    
    for i, ch in enumerate(chars):
        print i, ord(ch), ch
    print

    return u''.join(chars)



    

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
        self.assertEqual(u"\u00E9", decode_weird_utf8('\xc3\xa9'))

    def test_three_byte_utf8(self):
        self.assertEqual(u"\u0800", decode_weird_utf8('\xe0\xa0\x80'))

    

    def test_full(self):
        ## Do stuff
        with open("utf_txt") as f:
            print decode_weird_utf8(f.read())

if __name__ == '__main__':
    unittest.main()
