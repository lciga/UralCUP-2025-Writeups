from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime
from secret import medium_1 as flag

e = 3
p, q = 4, 4
while (p - 1) % 3 == 0 or (q - 1) % 3 == 0:
    p = getPrime(512)
    q = getPrime(512)

msg = bytes_to_long(flag)
n = p * q 
ct = pow(msg, e, n)
print(f"{n = }")
print(f"{e = }")
print(f"{ct = }")
