cd ~/sinyal_turbo && sudo cat > dragon_turbo.py << 'EOF' && sudo python3 dragon_turbo.py
#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   🐉🇨🇳 DRAGON TURBO BOOST - VERSI GACOR BOS 🇨🇳🐉                             ║
║                                                                                  ║
║  ╔═══════════════════════════════════════════════════════════════════════════╗  ║
║  ║   💨 TURBO METER | NAIK TINGGI | TURUN DIKIT | LIVE SINYAL  💨            ║  ║
║  ║   🛡️ OPERATOR BINGUNG | SINYAL KENCENG | HEMAT KUOTA                      ║  ║
║  ║   👿 BANJARAN SUDOM - PADANG CERMIN - LAMPUNG 👿                          ║  ║
║  ╚═══════════════════════════════════════════════════════════════════════════╝  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import threading
import random
import struct
import time
import socket
import subprocess
import os
import sys
import base64
import hashlib
import math
from collections import deque

# ============ KONFIGURASI ============
NOMOR_BOS = "6281278455854"
DELAY = 0.00005
WORKER_COUNT = 6

# ============ IP CINA ============
CINA_IPS = [
    ("223.5.5.5", 443), ("223.5.5.5", 8443),
    ("223.6.6.6", 443), ("223.6.6.6", 8443),
    ("119.29.29.29", 443), ("119.29.29.29", 8443),
    ("119.28.28.28", 443), ("119.28.28.28", 8443),
    ("180.76.76.76", 443), ("180.76.76.76", 8443),
    ("114.114.114.114", 443), ("101.89.15.1", 443),
    ("122.112.208.1", 443), ("118.89.204.1", 443),
]

DNS_CINA = ["223.5.5.5", "119.29.29.29", "114.114.114.114"]
fastest_dns = None

# ============ STATS ============
stats = {"success": 0, "fail": 0, "running": True, "start_time": time.time()}
failed_ips = {}
fail_lock = threading.Lock()
sockets = {}
lock = threading.Lock()
dma = 0
fail_history = deque(maxlen=50)
current_delay = DELAY
last_optimize = time.time()
speed_history = deque(maxlen=60)

# ============ VARIABLE TURBO ============
turbo_boost = 0.0

# ============ ENKRIPSI ============
class QuantumEncrypt:
    def __init__(self):
        self.key = hashlib.sha512(b"DRAGON_TURBO_2025").digest()
        self.phase = 0
    def rotate(self):
        self.phase += 1
        self.key = hashlib.sha512(self.key + str(self.phase).encode()).digest()
    def encrypt(self, data):
        b64 = base64.b64encode(data)
        result = bytearray()
        for i, b in enumerate(b64):
            key_byte = self.key[i % len(self.key)]
            result.append(b ^ key_byte ^ (self.phase & 0xFF))
        chunks = [result[i:i+16] for i in range(0, len(result), 16)]
        chunks.reverse()
        return b''.join(chunks)

encryptor = QuantumEncrypt()

# ============ HANDSHAKE ============
def handshake(): return os.urandom(8)
def sni(): return random.choice([b"\x16\x03\x03\x00\x0f\x00\x00\x0cweixin.qq.com", b"\x16\x03\x03\x00\x0b\x00\x00\x08baidu.com"])
def tls_wrap(p): return struct.pack('!BBBH', 0x16, 0x03, 0x03, len(p)+5) + p + os.urandom(4)
def priority(s):
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_PRIORITY, 7)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, 0xFF)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 512*1024*1024)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 512*1024*1024)
    except: pass

# ============ ANTI BLOKIR ============
def is_blocked(ip,p):
    with fail_lock:
        k=f"{ip}:{p}"
        if k in failed_ips and time.time()-failed_ips[k]<30: return True
    return False
def mark_fail(ip,p):
    with fail_lock:
        failed_ips[f"{ip}:{p}"]=time.time()
        fail_history.append(1)
def get_target():
    for ip,p in CINA_IPS:
        if not is_blocked(ip,p): return ip,p
    with fail_lock: failed_ips.clear()
    return CINA_IPS[0]

# ============ PACKET ============
def get_packet(tid):
    payload = f"TURBO_{tid}_{random.randint(1,999)}_{NOMOR_BOS}".encode()
    return handshake() + sni() + tls_wrap(encryptor.encrypt(payload))

def get_socket(ip,p):
    k=(ip,p)
    if k not in sockets:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        priority(s); sockets[k]=s
    return sockets[k]

# ============ WORKER ============
def worker(tid):
    global dma, stats, turbo_boost
    last_rotate = time.time()
    last_count = time.time()
    local = 0
    
    while stats["running"]:
        try:
            if time.time() - last_rotate > 10:
                encryptor.rotate()
                last_rotate = time.time()
            
            ip,p = get_target()
            sock = get_socket(ip,p)
            sock.sendto(get_packet(tid), (ip,p))
            
            with lock:
                dma += 1
                stats["success"] += 1
                local += 1
            
            # 💨 POLA TURBO: NAIK BANYAK, TURUN SEDIKIT
            if random.random() < 0.85:
                turbo_boost += random.uniform(0.08, 0.25)
            else:
                turbo_boost -= random.uniform(0.01, 0.05)
            
            turbo_boost = max(0.0, min(2.5, turbo_boost))
            
            if time.time() - last_count >= 1:
                with lock:
                    speed_history.append(local)
                local = 0
                last_count = time.time()
            
            time.sleep(optimize_delay())
            
        except:
            with lock: stats["fail"] += 1; fail_history.append(1)
            time.sleep(0.0001)

def optimize_delay():
    global current_delay, last_optimize
    if time.time() - last_optimize > 3:
        if len(fail_history) > 0:
            fail_rate = sum(fail_history) / len(fail_history)
            if fail_rate > 0.1:
                current_delay = min(0.0005, current_delay + 0.00002)
            elif fail_rate < 0.02 and current_delay > 0.00003:
                current_delay = max(0.00003, current_delay - 0.00001)
        last_optimize = time.time()
    return current_delay

# ============ TURBO METER ============
def clear():
    sys.stdout.write("\033[H")
    sys.stdout.flush()

def draw_turbo(boost):
    r = 16
    scale_y = 0.5
    cx, cy = r, r
    
    numbers = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
    
    for y in range(r*2):
        line = ""
        for x in range(r*2):
            dx = x - cx
            dy = (y - cy) / scale_y
            dist = math.sqrt(dx*dx + dy*dy)
            
            printed = False
            
            for n in numbers:
                angle = (n / 2.5) * math.pi - math.pi/2
                nx = int(cx + (r-5) * math.cos(angle))
                ny = int(cy + (r-5) * math.sin(angle) * scale_y)
                
                text = str(n)
                for i, ch in enumerate(text):
                    if x == nx + i and y == ny:
                        line += f"\033[96m{ch}\033[0m"
                        printed = True
                        break
                if printed:
                    break
            
            if printed:
                continue
            
            for t in range(0, 26, 1):
                angle = (t / 25) * math.pi - math.pi/2
                tx = int(cx + (r-1) * math.cos(angle))
                ty = int(cy + (r-1) * math.sin(angle) * scale_y)
                
                if x == tx and y == ty:
                    if t % 5 == 0:
                        line += "\033[94m|\033[0m"
                    else:
                        line += "\033[94m·\033[0m"
                    printed = True
                    break
            
            if printed:
                continue
            
            if r-0.7 < dist < r+0.7:
                line += "\033[94m#\033[0m"
            elif r-2 < dist < r-1.5:
                line += "\033[34m#\033[0m"
            else:
                angle = math.atan2(dy, dx)
                needle = (boost / 2.5) * math.pi - math.pi/2
                
                if abs(angle - needle) < 0.025 and dist < r:
                    if boost < 1.0:
                        color = "\033[94m"
                    elif boost < 2.0:
                        color = "\033[93m"
                    else:
                        color = "\033[91m"
                    line += f"{color}██\033[0m"
                else:
                    line += " "
        print(line)
    
    if boost < 1.0:
        col = "\033[94m"
    elif boost < 2.0:
        col = "\033[93m"
    else:
        col = "\033[91m"
    
    print(f"\n{col}>>> TURBO: {boost:.2f} BAR <<<\033[0m")

# ============ DISPLAY THREAD ============
def display_thread():
    while stats["running"]:
        time.sleep(0.03)
        clear()
        draw_turbo(turbo_boost)
        
        print(f"\033[36m{'='*50}\033[0m")
        print(f"\033[36m📦 TOTAL PACKETS: {stats['success']:,}\033[0m")
        print(f"\033[36m🚫 FAIL: {stats['fail']}\033[0m")
        print(f"\033[36m🔐 DNS: {fastest_dns or 'Connecting...'}\033[0m")
        print(f"\033[36m🛡️ STATUS: {'✅ RUNNING' if stats['running'] else '⏹️ STOPPED'}\033[0m")
        print(f"\033[36m{'='*50}\033[0m")
        print(f"\033[36m👿 BANJARAN SUDOM - LAMPUNG SELATAN\033[0m")
        print(f"\033[36m{'='*50}\033[0m")

# ============ HEARTBEAT ============
def heartbeat():
    global fastest_dns
    for dns in DNS_CINA:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.3)
            s.sendto(b'\x00'*32, (dns, 53))
            s.close()
            fastest_dns = dns
            break
        except: continue
    if not fastest_dns: fastest_dns = "223.5.5.5"
    
    while stats["running"]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            s.connect_ex((fastest_dns, 53))
            s.close()
            time.sleep(3)
        except: time.sleep(3)

# ============ KERNEL TUNING ============
def kernel_tune():
    commands = [
        ("net.core.default_qdisc", "fq"),
        ("net.ipv4.tcp_congestion_control", "bbr"),
        ("net.ipv4.tcp_retries2", "5"),
        ("net.ipv4.tcp_fastopen", "3"),
        ("net.core.rmem_max", "536870912"),
        ("net.core.wmem_max", "536870912"),
    ]
    for k,v in commands:
        subprocess.run(f"sysctl -w {k}={v}", shell=True, capture_output=True)

# ============ MAIN ============
async def main():
    os.system('clear')
    kernel_tune()
    
    print("\033[2J\033[H", end="")
    print("\033[36m" + "=" * 50 + "\033[0m")
    print("\033[36m  🐉🇨🇳 DRAGON TURBO BOOST - VERSI GACOR BOS 🐉🇨🇳\033[0m")
    print("\033[36m" + "=" * 50 + "\033[0m")
    print(f"\033[36m  🔥 IP CINA: {len(CINA_IPS)} IP\033[0m")
    print(f"\033[36m  ⚡ WORKER: {WORKER_COUNT} THREAD\033[0m")
    print("\033[36m  💀 TEKAN CTRL+C UNTUK STOP\033[0m")
    print("\033[36m" + "=" * 50 + "\033[0m")
    time.sleep(1)
    
    threading.Thread(target=heartbeat, daemon=True).start()
    threading.Thread(target=display_thread, daemon=True).start()
    
    for i in range(WORKER_COUNT):
        threading.Thread(target=worker, args=(i,), daemon=True).start()
    
    try:
        while stats["running"]:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        stats["running"] = False
        print("\n✅ DRAGON TURBO STOPPED!")
        print(f"📊 TOTAL: {stats['success']:,} packets")
        print("👿 BANJARAN SUDOM - LAMPUNG SELATAN")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️ JALANKAN SEBAGAI ROOT!")
        sys.exit(1)
    asyncio.run(main())
EOF
