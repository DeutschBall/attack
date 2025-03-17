
# ARP Spoofing 
```
python arp_spoof.py -t 192.168.1.10 -r 192.168.1.1
```

-t指定目标主机 ，-r指定网关

效果是伪装成网关，截获来自目标主机的报文。

# hostscan

```
python hostscan.py -i 192.168.1.1/24
```

-i指定目标主机

效果是发现目标主机是否存活

# Portmap

```c
python portmap.py -i 192.168.1.1 -p 22,80,443,8080,3306,6379
```

-i指定目标主机

-p指定目标端口

效果是发现目标端口是否开放
