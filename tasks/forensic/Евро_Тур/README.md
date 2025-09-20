# Евро Тур | easy | forensic

## Информация

> -О-оу

> -Что?

> -Длинный тонель!

## Выдать участникам

[Файл](./public/capture.pcapng)

## Описание

Дамп сетевого трафика с эксфильтрацией данных через DNS-тунель. Необходимо найти паттерн и собрать закодированный PNG в котором LSB-стега

## Решение

### Анализ артефактов
Открыв дамп в Wireshark можем заметить большое число DNS пакетов с аномально большими поддоменами в зоне eurotour.com, причём поддомены похожи на base32. Также можно отметить большое число пакетов с похожим паттерном: `<SEQ>.<B32>.<B32>.<B32>.eurotour.com`. Из чего можно сделать вывод о том, что что-то передавалось через DNS-туннель.

Вытащим из пакетов только имена запросов:
```sh
tshark -r capture.pcapng -Y 'dns && dns.qry.name contains ".eurotour.com"' \
  -T fields -e dns.qry.name > qnames.txt
```

Изучив [файл](./solve/qnames.txt) можно заметить кучу мусора (cdn123, img42 и т.д.) и строки, начинающиеся с пяти цифр: `^\d{5}\..` Также есть маркер окончания `end.<SEQ>.eurotour.com`

### Восстановление файла из доменных имён
Попробуем из каждой строки вытащить SEQ, забрать все base32-лейблы между SEQ и зоной, склеить, декодировать и собрать файл по порядку SEQ. Для этого напишем скрипт:
```python
#!/usr/bin/env python3
import re, base64, sys

ZONE = "eurotour.com"
pat_seq = re.compile(r'(?i)^(\d{5})\.(.+?)\.' + re.escape(ZONE) + r'\.?$')
b32lab = re.compile(r'(?i)^[A-Z2-7]+$')

def pad_b32(s: str) -> str:
    return s + '=' * ((8 - len(s) % 8) % 8)

chunks = {}
with open('qnames.txt', 'r', errors='ignore') as f:
    for line in f:
        name = line.strip()
        m = pat_seq.match(name)
        if not m: 
            continue
        seq = int(m.group(1))
        middle = m.group(2).split('.')
        labels = [x for x in middle if b32lab.fullmatch(x)]
        if not labels:
            continue
        data_b32 = ''.join(x.upper() for x in labels)
        chunks[seq] = data_b32

if not chunks:
    print("no data chunks found", file=sys.stderr); sys.exit(1)

# проверка целостности
maxseq = max(chunks.keys())
missing = [i for i in range(maxseq+1) if i not in chunks]
if missing:
    print(f"missing chunks: {len(missing)} (e.g. {missing[:10]})", file=sys.stderr)
    sys.exit(2)

# склейка и декодирование
all_b32 = ''.join(chunks[i] for i in range(maxseq+1))
data = base64.b32decode(pad_b32(all_b32))
open('restored.bin','wb').write(data)
print(f"OK: wrote restored.bin ({len(data)} bytes)")
```

Открыв полученныё файл в HEX редакторе, мы можем увидеть сигнатуру `89 50 4E 47 0D 0A 1A 0A`, что говорит нам о том, что это PNG.

Открыв полученное [изображение](./solve/restored.png) мы не обнаруживаем что-то похожее на флаг.

### Стеганография
Закинем файл в stegsolve и посмотрим что можно найти. На Alpha plane 0 можем заметить пиксели вверху изображения:
![пиксели на Alpha plane 0](./solve/image.png)

Скорее всего это LSB-стега и флаг зашифрован в данных битах. Воспользуемся [скриптом](./solve/lsb_decode.py) для решения LSB-стеги, чтобы вытащить флаг. Получаем флаг

## Флаг

`UralCTF{wH47_d035_7h3_M0v13_H4v3_70_d0_w17H_17?}`

