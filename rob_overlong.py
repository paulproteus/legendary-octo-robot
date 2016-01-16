#!/usr/bin/env python3

def list_to_byte(lst):
    num = 0
    for bit in lst:
        num <<= 1
        num += bit
    return bytes([num])


def decode_overlong(file, bytes_out, text_out, textbits_out):
    bits = []
    outbytes = []
    chars = []
    while True:
        bs = file.read(1)
        if not bs:
            break
        byte = bs[0]
        cutoff = 0

        if byte >= 0xf8:
            raise ValueError
        elif byte >= 0xf0:
            start = byte - 0xf0
            cont = file.read(3)
            cutoff = 0x10000
        elif byte >= 0xe0:
            start = byte - 0xe0
            cont = file.read(2)
            cutoff = 0x800
        elif byte >= 0xc0:
            start = byte - 0xc0
            cont = file.read(1)
            cutoff = 0x80
        elif byte >= 0x80:
            raise ValueError
        else:
            start = byte
            cont = b''

        num = start
        for byte in cont:
            assert byte >> 6 == 2
            num <<= 6
            num += byte - 0b10000000

        if num == 0xfeff:
            continue

        text_out.write(chr(num))
        if num < cutoff:
            bits.append(1)
            textbits_out.write('1')
        else:
            bits.append(0)
            textbits_out.write('0')
        if len(bits) == 8:
            byte = list_to_byte(bits)
            bytes_out.write(byte)
            textbits_out.write('\n')
            bits.clear()

    return b''.join(outbytes).decode('utf-8', 'replace')


the_file = open('overlong.txt', 'rb')
bytes_out = open('bytes.dat', 'wb')
text_out = open('text.txt', 'w', encoding='utf-8')
textbits_out = open('textbits.txt', 'w', encoding='utf-8')
print(decode_overlong(the_file, bytes_out, text_out, textbits_out))
