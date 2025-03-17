from scapy.all import *
from cryptography.fernet import Fernet
src = '192.168.1.105'
dst = '127.0.0.1'				#受害者ip
sport = 11451
dport = 9973					#受害者task5 使用端口

data = "Hello,world!"           #此处发送任意消息


key = b"wldiPvKR6pNBrAWS_nXbszK_MnOx_Q4NKxcYH3eN5Os="
cipher_suite = Fernet(key)
msg = data.encode("utf-8")
enc_msg = cipher_suite.encrypt(msg)


packet =  IP(src=src,dst=dst)/UDP(sport=sport,dport=dport)/enc_msg
packet.show()
send(packet)