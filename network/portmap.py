#端口扫描
import socket
import threading
import argparse

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 设置超时时间为1秒

        result = sock.connect_ex((ip, port))  # connect_ex() 返回0表示连接成功，非0表示失败

        if result == 0:
            print(f"端口 {port} 在 {ip} 上开放")
        sock.close()  # 关闭连接
    except socket.error:
        pass

def scan_ports(ip, ports):
    threads = []

    for port in ports:
        thread = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def main():
    parser = argparse.ArgumentParser(description='端口扫描工具')
    parser.add_argument('-i', '--ip', required=True, help='目标IP地址')
    parser.add_argument('-p', '--ports', required=True, type=lambda s: [int(port) for port in s.split(',')], help='要扫描的端口列表，以逗号分隔')

    args = parser.parse_args()

    target_ip = args.ip
    target_ports = args.ports

    print(f"开始扫描 {target_ip} 的端口...")
    scan_ports(target_ip, target_ports)

if __name__ == "__main__":
    main()
