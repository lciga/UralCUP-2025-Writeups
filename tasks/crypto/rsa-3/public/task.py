from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
from secret import flag
flag2 = flag + b" from Ural"
e = 3
p, q = 4, 4
while (p - 1) % 3 == 0 or (q - 1) % 3 == 0:
    p = getPrime(1000)
    q = getPrime(1000)

n = p * q
msg = bytes_to_long(flag)
ct = pow(msg, e, n)
print(f"{n = }")
print(f"{e = }")
print(f"{ct = }")
msg = bytes_to_long(flag2)
ct2 = pow(msg, e, n)
print(f"{ct2 = }")
