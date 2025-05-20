import wave
import struct

def extract_flag_from_wav(filename, spacing=1000, num_bits=8*30):
    with wave.open(filename, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        samples = list(struct.iter_unpack('<h', frames))

    bits = []
    for i in range(num_bits):
        idx = i * spacing
        if idx < len(samples):
            bits.append('1' if samples[idx][0] == 0 else '0')

    chars = [chr(int(''.join(bits[i:i+8]), 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

flag = extract_flag_from_wav("silent_transmission.wav")
print(flag)

