#主机发现
import scapy.all as scapy
import sys

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  
    arp_request_broadcast = broadcast/arp_request  

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    active_hosts = []
    for element in answered_list:
        host_info = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        active_hosts.append(host_info)
    
    return active_hosts

def display_result(results_list):
    print("IP Address\t\tMAC Address")
    print("-----------------------------------------")
    for host in results_list:
        print(f"{host['ip']}\t\t{host['mac']}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python hostscan.py -i <target_ip>")
        sys.exit(1)

    ip_range = sys.argv[1]  
    scan_result = scan(ip_range)
    display_result(scan_result)

if __name__ == "__main__":
    main()
