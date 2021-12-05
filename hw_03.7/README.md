# Домашнее задание к занятию "3.7. Компьютерные сети, лекция 2"

>**NB!**  
>Для корректного развёртывания ВМ в VirtualBox следует в Vagrantfile изменить `apt -y install nginx;` на `apt update && apt -y install nginx;` (сначала актуализировать базу данных по пакетам, а потом ставить `nginx`)**

## 1. Проверьте список доступных сетевых интерфейсов на вашем компьютере. Какие команды есть для этого в Linux и в Windows?

**Linux (`ipconfig`, `ip`)**
```bash
root@netology1:~# ip -br link
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP>
eth0             UP             08:00:27:73:60:cf <BROADCAST,MULTICAST,UP,LOWER_UP>
eth1             UP             08:00:27:86:6b:b0 <BROADCAST,MULTICAST,UP,LOWER_UP>
root@netology1:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:73:60:cf brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic eth0
       valid_lft 85698sec preferred_lft 85698sec
    inet6 fe80::a00:27ff:fe73:60cf/64 scope link
       valid_lft forever preferred_lft forever
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:86:6b:b0 brd ff:ff:ff:ff:ff:ff
    inet 172.28.128.10/24 scope global eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe86:6bb0/64 scope link
       valid_lft forever preferred_lft forever
```

**Windows (CMD: `ipconfig`, PS:`Get-NetAdapter`, `Get-NetIPAddress` etc.)**
```powershell
PS C:\Users\Administrator> ipconfig
Windows IP Configuration

Ethernet adapter Ethernet:

   Connection-specific DNS Suffix  . :
   IPv4 Address. . . . . . . . . . . : 192.168.0.251
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.0.1

Ethernet adapter VirtualBox Host-Only Network:

   Connection-specific DNS Suffix  . :
   Link-local IPv6 Address . . . . . : fe80::fd31:57fc:30f:d0e9%4
   IPv4 Address. . . . . . . . . . . : 192.168.56.1
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . :
```
```powershell
PS C:\Users\Administrator> Get-NetAdapter

Name                      InterfaceDescription                    ifIndex Status       MacAddress             LinkSpeed
----                      --------------------                    ------- ------       ----------             ---------
Ethernet                  Microsoft Hyper-V Network Adapter             5 Up           00-15-5D-6A-81-1A        10 Gbps
VirtualBox Host-Only N... VirtualBox Host-Only Ethernet Adapter         4 Up           0A-00-27-00-00-04         1 Gbps


PS C:\Users\Administrator> Get-NetIPAddress | sort InterfaceIndex | ft InterfaceIndex,InterfaceAlias,IPAddress,PrefixLength

InterfaceIndex InterfaceAlias               IPAddress                  PrefixLength
-------------- --------------               ---------                  ------------
             1 Loopback Pseudo-Interface 1  ::1                                 128
             1 Loopback Pseudo-Interface 1  127.0.0.1                             8
             4 VirtualBox Host-Only Network fe80::fd31:57fc:30f:d0e9%4           64
             4 VirtualBox Host-Only Network 192.168.56.1                         24
             5 Ethernet                     192.168.0.251                        24
             
```

## 2. Какой протокол используется для распознавания соседа по сетевому интерфейсу? Какой пакет и команды есть в Linux для этого?

**Для распознавания "соседа" по сетевому интерфейсу (ближайшее к интерфейсу активное оборудование) могут использоваться протоколы [CDP](http://xgu.ru/wiki/CDP) и [LLDP](http://xgu.ru/wiki/LLDP)**

**В Linux есть пакет `lldpd`, реализующий протоколы LLDP, CDP, EDP и др.**

***Пример установки и использования:***

Установим пакет `lldpd` из репозитория:

```bash
root@netology1:~# apt install -y lldpd
Reading package lists... Done
Building dependency tree
Reading state information... Done
...
Setting up lldpd (1.0.4-1build2) ...
Created symlink /etc/systemd/system/multi-user.target.wants/lldpd.service → /lib/systemd/system/lldpd.service.
Processing triggers for libc-bin (2.31-0ubuntu9.2) ...
Processing triggers for systemd (245.4-4ubuntu3.11) ...
Processing triggers for man-db (2.9.1-1) ...
```

Сконфигурируем, запустим и проверим состояние сервиса:

```bash
root@netology1:~# echo 'DAEMON_ARGS="-x -c -s -e"' >> /etc/default/lldpd

root@netology1:~# systemctl start lldpd

root@netology1:~# systemctl status lldpd
● lldpd.service - LLDP daemon
     Loaded: loaded (/lib/systemd/system/lldpd.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2021-12-05 15:53:13 UTC; 41s ago
       Docs: man:lldpd(8)
   Main PID: 22010 (lldpd)
      Tasks: 2 (limit: 1071)
     Memory: 2.0M
     CGroup: /system.slice/lldpd.service
             ├─22010 lldpd: monitor.
             └─22022 lldpd: connected to netology1.

Dec 05 15:53:13 netology1 systemd[1]: Starting LLDP daemon...
Dec 05 15:53:13 netology1 systemd[1]: Started LLDP daemon.
Dec 05 15:53:13 netology1 lldpd[22022]: /etc/localtime copied to chroot
Dec 05 15:53:13 netology1 lldpd[22022]: protocol LLDP enabled
Dec 05 15:53:13 netology1 lldpd[22022]: protocol CDPv1 disabled
Dec 05 15:53:13 netology1 lldpd[22022]: protocol CDPv2 disabled
Dec 05 15:53:13 netology1 lldpd[22022]: protocol SONMP disabled
Dec 05 15:53:13 netology1 lldpd[22022]: protocol EDP disabled
Dec 05 15:53:13 netology1 lldpd[22022]: protocol FDP disabled
Dec 05 15:53:13 netology1 lldpd[22022]: libevent 2.1.11-stable initialized with epoll method
```

Получим сведения о "соседях":

```bash
root@netology1:~# lldpctl
-------------------------------------------------------------------------------
LLDP neighbors:
-------------------------------------------------------------------------------
Interface:    eth1, via: LLDP, RID: 1, Time: 0 day, 00:06:18
  Chassis:
    ChassisID:    mac 08:00:27:73:60:cf
    SysName:      netology3
    SysDescr:     Ubuntu 20.04.2 LTS Linux 5.4.0-80-generic #90-Ubuntu SMP Fri Jul 9 22:49:44 UTC 2021 x86_64
    MgmtIP:       10.0.2.15
    MgmtIP:       fe80::a00:27ff:fe73:60cf
    Capability:   Bridge, off
    Capability:   Router, off
    Capability:   Wlan, off
    Capability:   Station, on
  Port:
    PortID:       mac 08:00:27:67:1c:b0
    PortDescr:    eth1
    TTL:          120
    PMD autoneg:  supported: yes, enabled: yes
      Adv:          10Base-T, HD: yes, FD: yes
      Adv:          100Base-TX, HD: yes, FD: yes
      Adv:          1000Base-T, HD: no, FD: yes
      MAU oper type: 1000BaseTFD - Four-pair Category 5 UTP, full duplex mode
-------------------------------------------------------------------------------
Interface:    eth1, via: LLDP, RID: 1, Time: 0 day, 00:00:53
  Chassis:
    ChassisID:    mac 08:00:27:73:60:cf
    SysName:      netology3
    SysDescr:     Ubuntu 20.04.2 LTS Linux 5.4.0-80-generic #90-Ubuntu SMP Fri Jul 9 22:49:44 UTC 2021 x86_64
    MgmtIP:       10.0.2.15
    MgmtIP:       fe80::a00:27ff:fe73:60cf
    Capability:   Bridge, off
    Capability:   Router, off
    Capability:   Wlan, off
    Capability:   Station, on
  Port:
    PortID:       mac 08:00:27:79:90:cf
    PortDescr:    eth1
    TTL:          120
    PMD autoneg:  supported: yes, enabled: yes
      Adv:          10Base-T, HD: yes, FD: yes
      Adv:          100Base-TX, HD: yes, FD: yes
      Adv:          1000Base-T, HD: no, FD: yes
      MAU oper type: 1000BaseTFD - Four-pair Category 5 UTP, full duplex mode
-------------------------------------------------------------------------------

```

## 3. Какая технология используется для разделения L2 коммутатора на несколько виртуальных сетей? Какой пакет и команды есть в Linux для этого? Приведите пример конфига.

## 4. Какие типы агрегации интерфейсов есть в Linux? Какие опции есть для балансировки нагрузки? Приведите пример конфига.

## 5. Сколько IP адресов в сети с маской /29 ? Сколько /29 подсетей можно получить из сети с маской /24. Приведите несколько примеров /29 подсетей внутри сети 10.10.10.0/24.

## 6. Задача: вас попросили организовать стык между 2-мя организациями. Диапазоны 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 уже заняты. Из какой подсети допустимо взять частные IP адреса? Маску выберите из расчета максимум 40-50 хостов внутри подсети.

## 7. Как проверить ARP таблицу в Linux, Windows? Как очистить ARP кеш полностью? Как из ARP таблицы удалить только один нужный IP?



 ---
## Задание для самостоятельной отработки (необязательно к выполнению)

## 8*. Установите эмулятор EVE-ng.
 
 Инструкция по установке - [https://github.com/svmyasnikov/eve-ng](https://github.com/svmyasnikov/eve-ng)

 Выполните задания на lldp, vlan, bonding в эмуляторе EVE-ng. 
 
 ---

