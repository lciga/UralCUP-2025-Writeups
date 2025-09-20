# rutracker | medium | forensic

## Информация

> Решил вспомнить молодость и скачал одну игру, но видимо там был вирус и теперь я потерял самое ценное, что у меня было...

> [Файл](https://disk.360.yandex.ru/d/omaRreDqamuhCw)

## Выдать участникам
[GTA cheatcodes.enc](./public/GTA%20cheatcodes.enc) и [README_RECOVER.txt](./public/README_RECOVER.txt)

## Описание

Дан дамп оперативной памяти Windows в которой поработал вымогатель и зашифровал файл с флагом. Необходимо через volatility вывтащить ключ шифрования и IV из переменных окружения в памяти и расшифровать файл

## Решение

### Изучение артефактов
Нам дан RAW дамп оперативной памяти, из условия понятно, что это скорее всего Windows.
Проверим содержимое файлов:
```sh
file GTA\ cheatcodes.enc
xxd -l 32 public/GTA\ cheatcodes.enc
```
Файл не похож на ZIP или PE и т.д. — значит скорее всего это чистый шифротекст.

В записке «one Advanced cipher» — может быть намёк на AES (Advanced Encryption Standard). То есть скорее AES-256 или AES-128.

### Анализ дампа
Изучим дерево процессов:
```sh
volatility3 -f dump.raw -o ~/Python/tasks/tasks/forensic/Евро_Тур/src windows.pstree
```
Находим процесс powershell.exe с PID 6044, который исполняет `powershell.exe -NoP -Ep Bypass -File "C:\Program Files\Internet Explorer\unistall.ps1" -PassLeft Sakura-`. В данной команде видно, что левая часть пароля: `Sakura-`, осталось найти вторую половину.

Попробуем проверить наличие второй части ключа в переменных окружения:
```sh
volatility3 -f dump.raw windows.envars --pid 6044
```
Находим там следующие параметры:
```
6044	powershell.exe	0x183cce31b90	AES_ITER	40000
6044	powershell.exe	0x183cce31b90	AES_SALT	s4WZyVqfYkYk0x5f8mF7iw==
```
Похоже на параметры KDF (соль и количество итераций). Возможно при шифровании использовался PBKDF2 для генерации ключа.

### Поиск недостающей части пароля
Попробуем пройтись по веткам реестра и попытаемся найти там что-нибудь подозрительное:
```sh
volatility3 -f dump.raw windows.registry.printkey --key "Software"
```
Находим подозрительную ветку `HKCU\Software\IEUpd`
```
2025-09-13 08:15:10.000000 UTC	0xcf0f8f327000	Key	\??\C:\Users\user\ntuser.dat\SOFTWARE	IEUpd	N/A	False
```
Выведем значение ключа:
```sh
volatility3 -f dump.raw windows.registry.printkey --key "Software\IEUpd"
```
Находим строку `Ur4lCTF-53cR3t`
```
2025-09-13 08:15:10.000000 UTC	0xcf0f8f327000	REG_SZ	\??\C:\Users\user\ntuser.dat\SOFTWARE\IEUpd	Hint	Ur4lCTF-53cR3t	False
```
Скорее всего это вторая часть пароля, то есть весь пароль `Sakura-Ur4lCTF-53cR3t`

Оталось понять откуда берётся IV. Однако явно он нигде в дампе не светится. Попробуем запустить `windows.malfind`:
```sh
 volatility3 -f dump.raw windows.malfind
```
В полученных функциях нет ничего, что может натолкнуть нас на IV. Попробуем написать YARA-правило, которое будет ловить всё, что может быть связано с шифрованием:
```sh
cat <<'YARA' > crypto.yar
rule crypto {
  strings:
    $a1 = "AesCryptoServiceProvider" ascii wide
    $a2 = "Rfc2898DeriveBytes" ascii wide
    $a3 = "CipherMode" ascii wide
    $a4 = "PaddingMode" ascii wide
    $a5 = "MD5" ascii wide
    $a6 = "WindowsIdentity" ascii wide
    $a7 = "GetCurrent" ascii wide
    $a8 = "User.Value" ascii wide
    $a9 = "ComputeHash" ascii wide
  condition: any of them
}
YARA
volatility3 -f dump.raw yarascan.YaraScan --yara-file crypto.yar
```
В выводе встречаются строки вида:
```
0xb6851e810275	crypto	$a6	
57 69 6e 64 6f 77 73 49 64 65 6e 74 69 74 79    WindowsIdentity
0x7ff8a2aa81b7	crypto	$a5	
4d 44 35                                        MD5
```
Что наталкивает на идею, что в качестве IV использовался один идентификатор WindowsIdentity. Проверим это предположение:
```sh 
volatility3 -f dump.raw windows.getsids
```
Получаем SID и имя пользователя: `S-1-5-21-3362121514-1744446750-4204895441-1001`

Напишем скрипт, который на основе всёго, что мы нашли, расшифровывает файл:
```python
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
```

## Флаг

`UralCTF{M0m_1M_n07_4_p1R4t3}`

