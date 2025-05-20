from Crypto.Util.number import getPrime, bytes_to_long


def gen_rsa_broken():
    while True:
        p = getPrime(1024)
        q = getPrime(1024)
        if p % 4 == 3 and q % 4 == 3:
            break

    n = p * q
    e = 1024

    m = b"goctf{k1nd4_l1k3_r4b1n_r5a_bu7_n0t_3x4c7ly}"
    m_int = bytes_to_long(m)
    c = pow(m_int, e, n)

    return n, e, c, p, q, m, m_int


if __name__ == '__main__':
    n, e, c, p, q, m, m_int = gen_rsa_broken()
    with open("./rsa.txt", "w") as f:
        f.write(f'''
[+] RSA Parameters
n = {n}
e = {e}
c = {c}
p = {p}
q = {q}
original plaintext = {m}
original plaintext (as int) = {m_int}
''')
