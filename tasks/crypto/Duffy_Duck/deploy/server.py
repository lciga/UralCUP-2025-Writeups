import socketserver
import threading
import time
from math import gcd
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Параметры Diffie-Hellman
# p - большое простое, n = p-1 имеет гладкие делители
p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
g = 2  # Генератор с составным порядком
n = p - 1  # Порядок группы, факторизуется как n = 2^2 * 3 * 5 * ... (гладкие делители)
a = 12345678901234567890  # Секретный ключ сервера
A = pow(g, a, p)  # Публичный ключ сервера

# Флаг
FLAG = b"UralCTF{L1f3_15_l1K3_4_hURr1c4N3}"

# Лимиты
TIMEOUT = 60
MAX_QUERIES = 10

class DHHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(TIMEOUT)
        queries = 0

        # Отправляем параметры
        self.request.sendall(f"p = {p}\n".encode())
        self.request.sendall(f"g = {g}\n".encode())
        self.request.sendall(f"A = {A}\n".encode())
        self.request.sendall(b"Send your public key B (hex): ")

        try:
            while queries < MAX_QUERIES:
                data = self.request.recv(1024).strip()
                if not data:
                    break

                try:
                    B = int(data.decode(), 16)
                    if B < 1 or B >= p:
                        self.request.sendall(b"Invalid B\n")
                        continue

                    # Вычисляем общий секрет
                    S = pow(B, a, p)
                    # Используем S как ключ для AES-CBC
                    key = str(S).encode()[:16].rjust(16, b"\x00")
                    iv = os.urandom(16)
                    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
                    encryptor = cipher.encryptor()
                    padded_flag = FLAG + b"\x00" * (16 - len(FLAG) % 16)
                    ciphertext = encryptor.update(padded_flag) + encryptor.finalize()

                    self.request.sendall(f"IV (hex): {iv.hex()}\n".encode())
                    self.request.sendall(f"Ciphertext (hex): {ciphertext.hex()}\n".encode())
                    queries += 1
                    self.request.sendall(f"Queries left: {MAX_QUERIES - queries}\n".encode())
                    if queries < MAX_QUERIES:
                        self.request.sendall(b"Send another B (hex): ")

                except ValueError:
                    self.request.sendall(b"Invalid input, send B as hex\n")
                except Exception as e:
                    self.request.sendall(f"Error: {str(e)}\n".encode())

        except TimeoutError:
            self.request.sendall(b"Timeout reached\n")
        except Exception as e:
            self.request.sendall(f"Error: {str(e)}\n".encode())

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 5099
    server = ThreadedServer((HOST, PORT), DHHandler)
    server.allow_reuse_address = True
    print(f"Server running on {HOST}:{PORT}")
    server.serve_forever()