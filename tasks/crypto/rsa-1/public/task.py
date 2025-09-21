from Crypto.Util.number import bytes_to_long, long_to_bytes, isPrime, getPrime
from secret import ease as flag

e = 3
p, q = 4, 4

while (p - 1) % 3 == 0 or (q - 1) % 3 == 0:
    p = getPrime(1000)
    for i in range(p, p + 10000):
        if isPrime(i):
            q = i

n = p * q
msg = bytes_to_long(flag)
ct = pow(msg, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{ct = }")
