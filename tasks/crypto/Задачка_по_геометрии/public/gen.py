import json
import random
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

def char_to_point(c: str, p: int) -> List[int]:
    val = ord(c)
    return [val % p, (val * 2) % p]

def apply_matrix(M: List[List[int]], point: List[int], p: int) -> List[int]:
    x = (M[0][0] * point[0] + M[0][1] * point[1]) % p
    y = (M[1][0] * point[0] + M[1][1] * point[1]) % p
    return [x, y]

def generate_task():
    p = 251
    k = 42
    # Генерация матрицы M с определителем 1
    while True:
        M = [[random.randint(1, p-1) for _ in range(2)] for _ in range(2)]
        if det(M, p) == 1:
            break
    M = [[3, 5], [7, 2]]  # Фиксированная матрица для воспроизводимости
    
    # Чтение флага
    with open("flag.txt", "r") as f:
        flag = f.read().strip()
    
    # Шифрование
    Mk = matrix_power(M, k, p)
    ciphertext = ""
    ciphertext_points = []
    for c in flag:
        point = char_to_point(c, p)
        cipher_point = apply_matrix(Mk, point, p)
        ciphertext_points.append(cipher_point)
        ciphertext += chr(cipher_point[0])  # Используем x-координату
    
    # Сохранение параметров
    task = {
        "field": p,
        "matrix_M": M,
        "k": k,
        "ciphertext": ciphertext
    }
    
    with open("task.json", "w") as f:
        json.dump(task, f, indent=4)
    
    print("Задание сгенерировано. Зашифрованный флаг:", ciphertext)
    print("Сохранено в task.json")

if __name__ == "__main__":
    generate_task()