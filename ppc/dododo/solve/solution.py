from random import randint
from mip import Model, xsum, INTEGER, CBC, MINIMIZE, MAXIMIZE, maximize


var_count = 5
equation_count = 5

model = Model(MAXIMIZE)



vars = [model.add_var(var_type=INTEGER, lb=1) for i in range(var_count)]
mul = [2, 8, 10, 6, 2]

model.objective = maximize(xsum(vars[i] * mul[i] for i in range(var_count)))

arr = [([5009, 7755, 9823, 3317, 846], 1187369997),
 ([7865, 3885, 2678, 8383, 3160], 1820381515),
 ([6495, 6597, 1299, 7243, 2685], 1381435487),
 ([9942, 1447, 2224, 5884, 5670], 1526595559),
 ([7098, 2805, 6830, 5323, 9603], 1926297218)]

for equation_index in range(equation_count):
    coefs = arr[equation_index][0]


    su = xsum(vars[i] * coefs[i] for i in range(var_count))

    bound = arr[equation_index][1]
    model += su <= bound

# model.write("output.lp")
model.optimize()

x = [int(vars[i].x) for i in range(var_count)]

# format flag

result = 2*x[0] + 8*x[1] + 10*x[2] + 6*x[3] + 2*x[4]

flag = list(b'\x9d\xce\x1d\xd2\xc0]\xdb\xdd\xd8S\xb1\x04\x87\xb38\xc1\xf6\xa5Z\xa6\xc5&\xb6\xcek\xbemo_\xac\xc5\x8c\x13\xdd')

for i in range(len(flag)):
    byte = ((pow(result, i, 48673) + (result**2 + result*3 + 43)) % 48673) % 256
    flag[i] ^= byte

flag = b'goctf{'+bytes(flag)+b'}'

# b'goctf{ILP_problem_wowowowowo_dodoodod123}'
