import json

def mod_inverse(a: int, m: int) -> int:
    def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    _, x, _ = extended_gcd(a, m)
    return (x % m + m) % m

def matrix_multiply(A: list[list[int]], B: list[list[int]], p: int) -> list[list[int]]:
    return [
        [(A[0][0] * B[0][0] + A[0][1] * B[1][0]) % p, (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % p],
        [(A[1][0] * B[0][0] + A[1][1] * B[1][0]) % p, (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % p]
    ]

def matrix_power(M: list[list[int]], k: int, p: int) -> list[list[int]]:
    result = [[1, 0], [0, 1]]
    base = [[x % p for x in row] for row in M]
    while k > 0:
        if k % 2 == 1:
            result = matrix_multiply(result, base, p)
        base = matrix_multiply(base, base, p)
        k //= 2
    return result

def det(M: list[list[int]], p: int) -> int:
    return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % p

def inverse_matrix(M: list[list[int]], p: int) -> list[list[int]]:
    d = det(M, p)
    d_inv = mod_inverse(d, p)
    return [
        [(M[1][1] * d_inv) % p, (-M[0][1] * d_inv) % p],
        [(-M[1][0] * d_inv) % p, (M[0][0] * d_inv) % p]
    ]

def apply_matrix(M: list[list[int]], point: list[int], p: int) -> list[int]:
    x = (M[0][0] * point[0] + M[0][1] * point[1]) % p
    y = (M[1][0] * point[0] + M[1][1] * point[1]) % p
    return [x, y]

def point_to_char(point: list[int], p: int) -> str:
    x, y = point
    if (x * 2) % p == y:
        return chr(x)
    return '?'

def check_solution(submitted_flag: str) -> bool:
    correct_flag = "UralCTF{0MG_tH15_15_g30M37ry}"
    return submitted_flag == correct_flag

def main():
    # Загружаем параметры задания
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
        point = [ord(c) % p, (ord(c) * 2) % p]  # Предполагаем, что ciphertext использует x-координату
        plain_point = apply_matrix(Mk_inv, point, p)
        plaintext += point_to_char(plain_point, p)
    
    print("Расшифрованное сообщение:", plaintext)
    if check_solution(plaintext):
        print("Флаг верный!")
    else:
        print("Флаг неверный.")

if __name__ == "__main__":
    main()