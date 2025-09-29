import base64

a = base64.b64decode("H0o7a48=")
b = base64.b64decode("TyF6EcM=")
array = [5,6,7,8,9,8,7,6,7,8,9,8,9]

ds = bytes([a[i] ^ b[i] for i in range(min(len(a), len(b)))])

password = bytes([ds[i] ^ array[i % len(array)] for i in range(len(ds))]).decode()
print(password)
