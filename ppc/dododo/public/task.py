import itertools

def check(x):
    assert x[0] >= 1
    assert x[1] >= 1
    assert x[2] >= 1
    assert x[3] >= 1
    assert x[4] >= 1

    assert 5009*x[0] + 7755*x[1] + 9823*x[2] + 3317*x[3] + 846*x[4] <= 1187369997
    assert 7865*x[0] + 3885*x[1] + 2678*x[2] + 8383*x[3] + 3160*x[4] <= 1820381515
    assert 6495*x[0] + 6597*x[1] + 1299*x[2] + 7243*x[3] + 2685*x[4] <= 1381435487
    assert 9942*x[0] + 1447*x[1] + 2224*x[2] + 5884*x[3] + 5670*x[4] <= 1526595559
    assert 7098*x[0] + 2805*x[1] + 6830*x[2] + 5323*x[3] + 9603*x[4] <= 1926297218

    return 2*x[0] + 8*x[1] + 10*x[2] + 6*x[3] + 2*x[4]

result = 0
for x in itertools.permutations(range(1, 200000), r=5):
    try:
        result = max(result, check(x))
    except:
        pass

flag = list(b'\x9d\xce\x1d\xd2\xc0]\xdb\xdd\xd8S\xb1\x04\x87\xb38\xc1\xf6\xa5Z\xa6\xc5&\xb6\xcek\xbemo_\xac\xc5\x8c\x13\xdd')

for i in range(len(flag)):
    byte = ((pow(result, i, 48673) + (result**2 + result*3 + 43)) % 48673) % 256
    flag[i] ^= byte

flag = b'goctf{'+bytes(flag)+b'}'
