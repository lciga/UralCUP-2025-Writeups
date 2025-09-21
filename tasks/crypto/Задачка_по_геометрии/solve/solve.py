import json
from typing import List, Tuple

def mod_inverse(a: int, m: int) -> int:
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    _, x, _ = extended_gcd(a, m)
    return (x % m + m) % m

def matrix_multiply(A: List[List[int]], B: List[List[int]], p: int) -> List[List[int]]:
    return [
        [(A[0][0] * B[0][0] + A[0][1] * B[1][0]) % p, (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % p],
        [(A[1][0] * B[0][0] + A[1][1] * B[1][0]) % p, (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % p]
    ]

def matrix_power(M: List[List[int]], k: int, p: int) -> List[List[int]]:
    result = [[1, 0], [0, 1]]
    base = [[x % p for x in row] for row in M]
    while k > 0:
        if k % 2 == 1:
            result = matrix_multiply(result, base, p)
        base = matrix_multiply(base, base, p)
        k //= 2
    return result

def det(M: List[List[int]], p: int) -> int:
    return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % p

def inverse_matrix(M: List[List[int]], p: int) -> List[List[int]]:
    d = det(M, p)
    d_inv = mod_inverse(d, p)
    return [
        [(M[1][1] * d_inv) % p, (-M[0][1] * d_inv) % p],
        [(-M[1][0] * d_inv) % p, (M[0][0] * d_inv) % p]
    ]

def apply_matrix(M: List[List[int]], point: List[int], p: int) -> List[int]:
    x = (M[0][0] * point[0] + M[0][1] * point[1]) % p
    y = (M[1][0] * point[0] + M[1][1] * point[1]) % p
    return [x, y]

def point_to_char(point: List[int], p: int) -> str:
    x, y = point
    if (x * 2) % p == y:  # Проверяем согласованность
        return chr(x)
    return '?'  # Если точка некорректна

def solve():
    # Читаем параметры
    with open("task.json", "r") as f:
        task = json.load(f)
    
    p = task["field"]
    M = task["matrix_M"]
    k = task["k"]
    ciphertext = task["ciphertext"]
    
    # Вычисляем M^k
    Mk = matrix_power(M, k, p)
    
    # Находим обратную матрицу (M^k)^(-1)
    Mk_inv = inverse_matrix(Mk, p)
    
    # Расшифровываем
    plaintext = ""
    for c in ciphertext:
        point = [ord(c) % p, (ord(c) * 2) % p]  # Восстанавливаем точку из x-координаты
        plain_point = apply_matrix(Mk_inv, point, p)
        plaintext += point_to_char(plain_point, p)
    
    print("Флаг:", plaintext)

if __name__ == "__main__":
    solve()