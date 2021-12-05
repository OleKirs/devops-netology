# Домашнее задание к занятию "3.7. Компьютерные сети, лекция 2"

>**NB!**  
> *Для корректного развёртывания ВМ в VirtualBox следует в Vagrantfile изменить `apt -y install nginx;` на `apt update && apt -y install nginx;` (сначала актуализировать базу данных по пакетам, а потом ставить `nginx`)*

## 1. Проверьте список доступных сетевых интерфейсов на вашем компьютере. Какие команды есть для этого в Linux и в Windows?  

### 1.1.  Какие команды есть для этого в Linux?  

**Linux (`ipconfig`, `ip` из пакета `iproute2`)**

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

### 1.2.  Какие команды есть для этого в Windows?  

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

### 2.1. Какой протокол используется для распознавания соседа по сетевому интерфейсу? 
**Для распознавания "соседа" по сетевому интерфейсу (ближайшее к интерфейсу активное оборудование) могут использоваться протоколы [CDP](http://xgu.ru/wiki/CDP) и [LLDP](http://xgu.ru/wiki/LLDP)**

### 2.2. Какой пакет и команды есть в Linux для этого?

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

### 3.1. Какая технология используется для разделения L2 коммутатора на несколько виртуальных сетей?

**Для разделения разделения L2 коммутатора на несколько виртуальных сетей в формате `Ethernet II` (протокол 802.3) может быть использована технология `VLAN` (Virtual Local Area Network), которая основана на загловках Eth-кадров рписанных в стандарте IEEE 802.1q) и её развитие, решающее проблему малого количества VLAN для больших развёртываний - `QnQ` (IEEE 802.1ad, "двойное тегирование в заголовке").**  

**Есть и другие варианты мультиплексирования поверх L1, но, пожалуй, основной - это использование VLAN в Ethernet (802.1q)**

### 3.2. пакет и команды есть в Linux для этого?

**В Debian-like дистрибутивах раньше использовался пакет `vlan`, сейчас такой функционал добавлен в пакет `iproute`**
Источник - [VLAN в Linux](http://xgu.ru/wiki/VLAN_%D0%B2_Linux)

Конфигурацию можно задавать динамически, через команды `ip` пакета `iproute`, например:

```bash
root@vagrant:~# ip link add link eth0 name vl100 type vlan id 100
root@vagrant:~# ip link show dev vl100
6: vl100@eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 08:00:27:73:60:cf brd ff:ff:ff:ff:ff:ff
root@vagrant:~# ip address add 172.31.0.5/12 brd + dev vl100
root@vagrant:~# ip address show dev vl100
6: vl100@eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 08:00:27:73:60:cf brd ff:ff:ff:ff:ff:ff
    inet 172.31.0.5/12 brd 172.31.255.255 scope global vl100
       valid_lft forever preferred_lft forever
root@vagrant:~#  ip link del vl100
root@vagrant:~# ip link show dev vl100
Device "vl100" does not exist.
```
Для сохранения настроек сети при перезагрузках в настоящее время в Deb-like дистрибутивах сеть конфигурируется утилитой [`netplan`](https://netplan.io/):

>Netplan is a utility for easily configuring networking on a linux system. You simply create a YAML description of the required network interfaces and what each should be configured to do. From this description Netplan will generate all the necessary configuration for your chosen renderer tool.

### 3.3. Приведите пример конфига

Пример конфигурации с VLAN ID = 50 поверх `eth0`, статическим IP-адресом и маршрутом в сеть 192.168.0.0/16 через этот интерфейс.

```bash
root@netology1:/etc/netplan# cat /etc/netplan/01-netcfg.yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: true
  vlans:
    vlan50:
      id: 50
      link: eth0
      dhcp4: no
      addresses: [192.168.1.2/24]
      routes:
          - to: 192.168.0.0/16
            via: 192.168.1.1
            on-link: true
```

Применим изменения и перезагрузим систему:

```bash
root@netology1:/etc/netplan# netplan apply
root@netology1:/etc/netplan# reboot
Connection to 127.0.0.1 closed by remote host.
Connection to 127.0.0.1 closed.
```

Зайдём в систему по SSH:

```powershell
PS D:\VBox\VMs\DevOps2021\hv_03.7> vagrant ssh netology1
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Sun 05 Dec 2021 05:22:48 PM UTC

  System load:  0.21              Processes:               121
  Usage of /:   2.5% of 61.31GB   Users logged in:         0
  Memory usage: 14%               IPv4 address for eth0:   10.0.2.15
  Swap usage:   0%                IPv4 address for vlan50: 192.168.1.2


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Sun Dec  5 15:36:56 2021 from 10.0.2.2
```

Проверим, что изменения сохранились (есть `vlan50@eth0`):

```bash
vagrant@vagrant:~$ sudo su -
root@vagrant:~# ip -details link show dev vlan50
4: vlan50@eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:73:60:cf brd ff:ff:ff:ff:ff:ff promiscuity 0 minmtu 0 maxmtu 65535
    vlan protocol 802.1Q id 50 <REORDER_HDR> addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535
```

## 4. Какие типы агрегации интерфейсов есть в Linux? Какие опции есть для балансировки нагрузки? Приведите пример конфига.

###  Какие типы агрегации интерфейсов есть в Linux? 

Агрегация интерфейсов (LAG - Link Aggregation Group) в Linux называется `Bonding` или `Ethernet Channel Bonding`.  
Типы (modes) балансировки поддерживаемые ядром Linux:

```bash
root@vagrant:~# modinfo bonding | grep mode
parm:           mode:Mode of operation; 0 for balance-rr, 1 for active-backup, 2 for balance-xor, 3 for broadcast, 4 for 802.3ad, 5 for balance-tlb, 6 for balance-alb (charp)
```

Типы LAG можно сгруппировать:  
*По наличию отказоустойчивости и балансировки между агрегированными каналами*
- Только отказоустойчивость (active-backup, broadcast)  
- Отказоустойчивость и балансировка (остальные режимы)  
*По необходимости настройки коммутаторов*  
- Требующие настройки коммутаторов (balance-rr, broadcast, (при подключении к разным коммутаторам), 802.3ad, )  
- Не требющие настройки (active-backup,  balance-xor, balance-tlb, balance-alb (charp))  

## Какие опции есть для балансировки нагрузки?  

***Типы агрегации (объединения) интерфейсов в Linux:***  

**mode=0 (balance-rr)** Этот режим используется по-умолчанию, если в настройках не указано другое. balance-rr обеспечивает балансировку нагрузки и отказоустойчивость. В данном режиме пакеты отправляются "по кругу" от первого интерфейса к последнему и сначала. Если выходит из строя один из интерфейсов, пакеты отправляются на оставшиеся. Дополнительной настройки коммутатора не требуется при нахождении портов в одном коммутаторе. При разных коммутаторах требуется дополнительная настройка.  

**mode=1 (active-backup)** При active-backup один интерфейс работает в активном режиме, остальные в ожидающем. Если активный падает, управление передается одному из ожидающих. Не требует поддержки данной функциональности от коммутатора.  

**mode=2 (balance-xor)** Передача пакетов распределяется между объединенными интерфейсами по формуле ((MAC-адрес источника) XOR (MAC-адрес получателя)) % число интерфейсов. Один и тот же интерфейс работает с определённым получателем. Режим даёт балансировку нагрузки и отказоустойчивость.  

**mode=3 (broadcast)** Происходит передача во все объединенные интерфейсы, обеспечивая отказоустойчивость. Подходит для вещания Broadcast/Multycast-траффика  

**mode=4 (802.3ad)** Это динамическое объединение портов (LACP). В данном режиме можно получить значительное увеличение пропускной способности как входящего так и исходящего трафика, используя все объединенные интерфейсы. Требует поддержки режима от коммутатора. Со стороны коммутаторов может быть реализован как MC-LAG для защиты от выхода из строя одного из линков/коммутаторов в "Multy Сhassis"-группе.  

**mode=5 (balance-tlb)** Адаптивная балансировка нагрузки. При balance-tlb входящий трафик получается только активным интерфейсом, исходящий - распределяется в зависимости от текущей загрузки каждого интерфейса. Обеспечивается отказоустойчивость и распределение нагрузки исходящего трафика. Не требует специальной поддержки коммутатора.  

**mode=6 (balance-alb)** Адаптивная балансировка нагрузки (более совершенная). Обеспечивает балансировку нагрузки как исходящего (TLB, transmit load balancing), так и входящего трафика (для IPv4 через механизмы протокола ARP). Не требует специальной поддержки коммутатором, но требует возможности изменять MAC-адрес устройства (MAC- спуфинг).  

### Приведите пример конфига.

>NB!  
>VirtualBox не работает с bound-интерфейсами (состояние интерфейсов правильное, но траффик не ходит, пока не "развалишь" LAG)

***Проверено на тестовой ВМ с Linux Mint***

```bash
root@Deb10-Lab:~# cat /etc/netplan/1-network-manager-all.yaml
# Let NetworkManager manage all devices on this system
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    eth0:
      dhcp4: true
    eth1:
      dhcp4: no
    eth2:
      dhcp4: no
  bonds:
    bond0:
      dhcp4: no
      interfaces: [eth1,eth2]
      parameters:
        mode: balance-rr
        mii-monitor-interval: 1
  vlans:
    vl1017:
      id: 1017
      link: bond0
      dhcp4: no
      addresses: [10.10.17.19/24]
```

Проверка:

```bash
root@Deb10-Lab:~# ping 10.10.15.10
PING 10.10.5.10 (10.10.5.10) 56(84) bytes of data.
64 bytes from 10.10.15.10: icmp_seq=1 ttl=127 time=0.681 ms
64 bytes from 10.10.15.10: icmp_seq=2 ttl=127 time=0.748 ms
64 bytes from 10.10.15.10: icmp_seq=3 ttl=127 time=0.839 ms
^C
--- 10.10.15.10 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2026ms
rtt min/avg/max/mdev = 0.681/0.756/0.839/0.064 ms
```

## 5. Сколько IP адресов в сети с маской /29 ? Сколько /29 подсетей можно получить из сети с маской /24. Приведите несколько примеров /29 подсетей внутри сети 10.10.10.0/24.

256 адресов / 8 адресов = 32 подсети

```bash
root@vagrant:~# ipcalc 10.10.10.17/24 -s 6 6 6 6 6 6 6 6 6 6 6 6 6 | grep /29
Network:   10.10.10.0/29        00001010.00001010.00001010.00000 000
Network:   10.10.10.8/29        00001010.00001010.00001010.00001 000
Network:   10.10.10.16/29       00001010.00001010.00001010.00010 000
Network:   10.10.10.24/29       00001010.00001010.00001010.00011 000
Network:   10.10.10.32/29       00001010.00001010.00001010.00100 000
Network:   10.10.10.40/29       00001010.00001010.00001010.00101 000
Network:   10.10.10.48/29       00001010.00001010.00001010.00110 000
Network:   10.10.10.56/29       00001010.00001010.00001010.00111 000
Network:   10.10.10.64/29       00001010.00001010.00001010.01000 000
Network:   10.10.10.72/29       00001010.00001010.00001010.01001 000
Network:   10.10.10.80/29       00001010.00001010.00001010.01010 000
Network:   10.10.10.88/29       00001010.00001010.00001010.01011 000
Network:   10.10.10.96/29       00001010.00001010.00001010.01100 000
```


## 6. Задача: вас попросили организовать стык между 2-мя организациями. Диапазоны 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 уже заняты. Из какой подсети допустимо взять частные IP адреса? Маску выберите из расчета максимум 40-50 хостов внутри подсети.

Частные адреса можно взять из диапазана CGNAT - 100.64.0.0/10

## 7. Как проверить ARP таблицу в Linux, Windows? Как очистить ARP кеш полностью? Как из ARP таблицы удалить только один нужный IP?


### 7.1. проверить ARP таблицу  

**Linux:**  

`ip neigh list`  

```bash
root@netology3:~# ip neigh list
10.0.2.2 dev eth0 lladdr 52:54:00:12:35:02 REACHABLE
172.28.128.10 dev eth1 lladdr ce:6f:47:14:cc:dd STALE
172.28.128.60 dev eth1 lladdr 08:00:27:67:1c:b0 STALE
10.0.2.3 dev eth0 lladdr 52:54:00:12:35:03 STALE
```

**Windows**  

`arp -a`  

```powershell
PS C:\Users\Administrator> arp -a

Interface: 192.168.56.1 --- 0x4
  Internet Address      Physical Address      Type
  192.168.56.255        ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
```


### 7.2. Как очистить ARP кеш полностью?

**Linux:**  

`ip neigh flush dev <DeviceName>`  

```bash
root@netology3:~# ip neigh flush dev eth1
root@netology3:~#
root@netology3:~# ip neigh show
10.0.2.2 dev eth0 lladdr 52:54:00:12:35:02 REACHABLE
10.0.2.3 dev eth0 lladdr 52:54:00:12:35:03 STALE
```

**Windows**  

`arp -d *`  

```powershell
PS C:\Users\Administrator> arp -d *
```

## 7.3. Как из ARP таблицы удалить только один нужный IP?

**Linux:**  

`ip neigh del <IP-addr> dev <DeviceName>`  

```bash
root@netology3:~# ip neigh show
10.0.2.2 dev eth0 lladdr 52:54:00:12:35:02 REACHABLE
172.28.128.10 dev eth1 lladdr ce:6f:47:14:cc:dd STALE
172.28.128.60 dev eth1 lladdr 08:00:27:67:1c:b0 STALE
10.0.2.3 dev eth0 lladdr 52:54:00:12:35:03 STALE
root@netology3:~# ip neigh del 172.28.128.10 dev eth1
root@netology3:~# ip neigh show
10.0.2.2 dev eth0 lladdr 52:54:00:12:35:02 REACHABLE
172.28.128.60 dev eth1 lladdr 08:00:27:67:1c:b0 STALE
10.0.2.3 dev eth0 lladdr 52:54:00:12:35:03 STALE
```

**Windows**  

`arp -d <IP-addr>`

```powershell
PS C:\Users\Administrator> arp -d 192.168.0.1
```

 ---
## Задание для самостоятельной отработки (необязательно к выполнению)

## 8*. Установите эмулятор EVE-ng.
 
 Инструкция по установке - [https://github.com/svmyasnikov/eve-ng](https://github.com/svmyasnikov/eve-ng)

 Выполните задания на lldp, vlan, bonding в эмуляторе EVE-ng. 
 
 ---

