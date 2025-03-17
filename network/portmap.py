#端口扫描
import socket
import threading

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

if __name__ == "__main__":
    target_ip = "192.168.1.1"  # 设置目标IP地址
    target_ports = [22, 80, 443, 8080, 3306, 6379]  # 要扫描的端口列表

    print(f"开始扫描 {target_ip} 的端口...")
    scan_ports(target_ip, target_ports)
