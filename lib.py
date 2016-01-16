# Write functions in here.
#
# You can also execute this file if you want; it'll run the unit tests for library functions.

def decode_ascii(bytes):
    # TODO: Make less of a skeleton.
    return bytes.decode('ascii')

def decode_normal_utf8(bytes):
    return bytes.decode('utf-8')


TRY_TO_DECODE_WITH_THESE = [
    decode_ascii,
    decode_normal_utf8,
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

if __name__ == '__main__':
    unittest.main()
