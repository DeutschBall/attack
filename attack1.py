from scapy.all import *
src = '192.168.1.105'			#可以是任意地址, 隐藏攻击者的真实ip
dst = '192.168.1.102'			#树莓派ip
sport = 11451
dport = 8715					#task1使用的端口

packet =  IP(src=src,dst=dst)/UDP(sport=sport,dport=dport)/"Hello,world!"
packet.show()
send(packet)