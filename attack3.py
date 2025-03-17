from scapy.all import *
src = '192.168.1.103'		#可以是任意地址, 隐藏攻击者的真实ip
dst = '192.168.1.102'		#假设树莓派在这里
sport = 11451
dport = 8716				#start_docker监听的端口

packet =  IP(src=src,dst=dst)/UDP(sport=sport,dport=dport)/"Hello,world!"
packet.show()
send(packet)