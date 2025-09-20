#!/usr/bin/env python3

import argparse, base64, binascii, hashlib, sys, pathlib
from Crypto.Cipher import AES

def pbkdf2_key(pass_bytes: bytes, salt_b64: str, iters: int) -> bytes:
    salt = base64.b64decode(salt_b64)
    return hashlib.pbkdf2_hmac("sha1", pass_bytes, salt, iters, dklen=32)

def iv_from_sid(sid: str) -> bytes:
    return hashlib.md5(sid.encode("utf-8")).digest()

def pkcs7_unpad(data: bytes) -> bytes:
    if not data:
        raise ValueError("Empty plaintext after decrypt")
    n = data[-1]
    if not (1 <= n <= 16) or data[-n:] != bytes([n]) * n:
        raise ValueError(f"PKCS7 invalid (pad={n}) -> неверные key/iv/артефакты или чужой .enc")
    return data[:-n]

def main():
    p = argparse.ArgumentParser(description="Decrypt AES-256-CBC by CTF artifacts")
    p.add_argument("-i","--in",  dest="inp", required=True, help="входной .enc")
    p.add_argument("-o","--out", dest="out", help="выходной файл (по умолчанию: <in>.dec)")
    p.add_argument("--pass-left",  required=True, help='PassLeft (из cmdline), например: Sakura-')
    p.add_argument("--pass-right", required=True, help='PassRight/Hint (HKCU\\Software\\IEUpd\\Hint)')
    p.add_argument("--salt-b64",   required=True, help='AES_SALT (Base64 из env), например: s4WZyVqfYkYk0x5f8mF7iw==')
    p.add_argument("--iter",       required=True, type=int, help='AES_ITER (из env), например: 40000')
    p.add_argument("--sid",        required=True, help='SID пользователя (из getsids), например: S-1-5-21-...-1001')
    p.add_argument("--show-keys",  action="store_true", help="печать key/iv в hex для самопроверки")
    args = p.parse_args()

    inp = pathlib.Path(args.inp)
    if not inp.exists():
        print(f"[!] Файл не найден: {inp}", file=sys.stderr); sys.exit(1)
    out = pathlib.Path(args.out) if args.out else inp.with_suffix(inp.suffix + ".dec")

    # Пароль как в скрипте атакующего
    password = (args.pass_left + args.pass_right).encode("utf-8")

    key = pbkdf2_key(password, args.salt_b64, args.iter)
    iv  = iv_from_sid(args.sid)

    if args.show_keys:
        print("key_hex =", binascii.hexlify(key).decode())
        print("iv_hex  =", binascii.hexlify(iv).decode())

    ct = inp.read_bytes()
    if len(ct) % 16 != 0:
        print(f"[!] Ciphertext length {len(ct)} не кратна 16 → это не сырое AES-CBC или файл битый", file=sys.stderr)
        sys.exit(2)

    pt_padded = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    try:
        pt = pkcs7_unpad(pt_padded)
    except ValueError as e:
        print(f"[!] {e}", file=sys.stderr); sys.exit(3)

    out.write_bytes(pt)
    print(f"[+] OK: расшифровано -> {out}  ({len(pt)} bytes)")

if __name__ == "__main__":
    main()
