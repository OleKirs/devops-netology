# Домашнее задание к занятию "3.8. Компьютерные сети, лекция 3"

## 1. Подключитесь к публичному маршрутизатору в интернет. Найдите маршрут к вашему публичному IP
```
telnet route-views.routeviews.org
Username: rviews
show ip route x.x.x.x/32
show bgp x.x.x.x/32
```

**Выполнено:**

```bash
vagrant@netology1:~$ telnet route-views.routeviews.org
Trying 128.223.51.103...
Connected to route-views.routeviews.org.
Escape character is '^]'.
C
**********************************************************************

                    RouteViews BGP Route Viewer
                    route-views.routeviews.org

 route views data is archived on http://archive.routeviews.org

 ...

 To login, use the username "rviews".

**********************************************************************

User Access Verification

Username: rviews
route-views>show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is 128.223.51.1 to network 0.0.0.0

S*    0.0.0.0/0 [1/0] via 128.223.51.1
      1.0.0.0/8 is variably subnetted, 3151 subnets, 18 masks
B        1.0.0.0/24 [20/0] via 64.71.137.241, 2w0d
B        ...
B        1.1.146.0/24 [20/0] via 64.71.137.241, 1w4d

route-views>show ip route 195.144.224.***
Routing entry for 195.144.224.0/19, supernet
  Known via "bgp 6447", distance 20, metric 0
  Tag 3356, type external
  Last update from 4.68.4.46 2w5d ago
  Routing Descriptor Blocks:
  * 4.68.4.46, from 4.68.4.46, 2w5d ago
      Route metric is 0, traffic share count is 1
      AS Hops 3
      Route tag 3356
      MPLS label: none
route-views>
...
route-views>show bgp 195.144.231.149
BGP routing table entry for 195.144.224.0/19, version 1373893071
Paths: (24 available, best #11, table default)
  Not advertised to any peer
  Refresh Epoch 3
  3303 31133 20632
    217.192.89.50 from 217.192.89.50 (138.187.128.158)
      Origin IGP, localpref 100, valid, external
      Community: 0:15169 3303:1004 3303:1006 3303:1030 3303:3056 20632:64361 20632:65401 31133:26149 65535:20632 65535:65001
      path 7FE01841BCB8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  4901 6079 31133 20632
    162.250.137.254 from 162.250.137.254 (162.250.137.254)
      Origin IGP, localpref 100, valid, external
      Community: 65000:10100 65000:10300 65000:10400
      path 7FE0BBC4C2F0 RPKI State not found
      rx pathid: 0, tx pathid: 0
...
  Refresh Epoch 1
  3356 31133 20632
    4.68.4.46 from 4.68.4.46 (4.69.184.201)
      Origin IGP, metric 0, localpref 100, valid, external, best
      Community: 3356:2 3356:22 3356:90 3356:123 3356:519 3356:903 3356:2094 20632:64361 20632:65401 31133:33 31133:100 31133:178 31133:300 31133:1000 31133:1078 65001:1299 65535:20632 65535:65001
      path 7FE0AA3D9110 RPKI State not found
      rx pathid: 0, tx pathid: 0x0
...
  Refresh Epoch 1
  19214 174 31133 20632
    208.74.64.40 from 208.74.64.40 (208.74.64.40)
      Origin IGP, localpref 100, valid, external
      Community: 174:21101 174:22005
      path 7FE0504B7D20 RPKI State not found
      rx pathid: 0, tx pathid: 0
route-views>exit
Connection closed by foreign host.
```

## 2. Создайте dummy0 интерфейс в Ubuntu. Добавьте несколько статических маршрутов. Проверьте таблицу маршрутизации.

```bash

```

## 3. Проверьте открытые TCP порты в Ubuntu, какие протоколы и приложения используют эти порты? Приведите несколько примеров.

### 3.1. Проверьте открытые TCP порты в Ubuntu.
```bash
root@netology1:~# ss -tanp
State              Recv-Q             Send-Q                         Local Address:Port                         Peer Address:Port             Process
LISTEN             0                  4096                                 0.0.0.0:111                               0.0.0.0:*                 users:(("rpcbind",pid=565,fd=4),("systemd",pid=1,fd=44))
LISTEN             0                  511                                  0.0.0.0:80                                0.0.0.0:*                 users:(("nginx",pid=7167,fd=6),("nginx",pid=7166,fd=6),("nginx",pid=7165,fd=6))
LISTEN             0                  4096                           127.0.0.53%lo:53                                0.0.0.0:*                 users:(("systemd-resolve",pid=566,fd=13))
LISTEN             0                  128                                  0.0.0.0:22                                0.0.0.0:*                 users:(("sshd",pid=795,fd=3))
ESTAB              0                  0                                  10.0.2.15:22                               10.0.2.2:50913             users:(("sshd",pid=22068,fd=4),("sshd",pid=22018,fd=4))
LISTEN             0                  4096                                    [::]:111                                  [::]:*                 users:(("rpcbind",pid=565,fd=6),("systemd",pid=1,fd=46))
LISTEN             0                  511                                     [::]:80                                   [::]:*                 users:(("nginx",pid=7167,fd=7),("nginx",pid=7166,fd=7),("nginx",pid=7165,fd=7))
LISTEN             0                  128                                     [::]:22                                   [::]:*                 users:(("sshd",pid=795,fd=4))
```

### 3.2. Какие протоколы и приложения используют эти порты? Приведите несколько примеров.

`LISTEN             0                  4096                                 0.0.0.0:111                               0.0.0.0:*                 users:(("rpcbind",pid=565,fd=4),("systemd",pid=1,fd=44))` - Демон `rpcbind`, сопоставляющий универсальные адреса и номера программ RPC. Это сервер, преобразующий номера программ RPC в универсальные адреса. Слушает порт TCP 111 на всех адресах хоста (`0.0.0.0:111`) по протоколу IPv4 со всех источников (`0.0.0.0:*`).

`LISTEN             0                  511                                  0.0.0.0:80                                0.0.0.0:*                 users:(("nginx",pid=7167,fd=6),("nginx",pid=7166,fd=6),("nginx",pid=7165,fd=6))` - демон `nginx` — веб-сервер и прокси-сервер.  Слушает порт TCP 80 на всех адресах хоста (`0.0.0.0:80`) по протоколу IPv4 со всех источников (`0.0.0.0:*`).

`LISTEN             0                  4096                           127.0.0.53%lo:53                                0.0.0.0:*                 users:(("systemd-resolve",pid=566,fd=13))` - служба, отвечающая за разрешение имён с возможностью кэширования результатов запросов с внешних DNS-серверов, входящая в состав "Systemd". Слушает порт TCP 53 на всех адресах хоста (`0.0.0.0:80`) по протоколу IPv4 со всех источников (`0.0.0.0:*`).

`ESTAB              0                  0                                  10.0.2.15:22                               10.0.2.2:50913             users:(("sshd",pid=22068,fd=4),("sshd",pid=22018,fd=4))` - Установленное соединение от хоста гипервизора (10.0.2.2:50913) до ВМ (10.0.2.15:22) по протоколу SSH (локальный порт TCP 22)

`LISTEN             0                  128                                     [::]:22                                   [::]:*                 users:(("sshd",pid=795,fd=4))` - Демон `sshd` сервиса SSH. Слушает порт TCP 22 на всех адресах хоста (`[::]:22`) по протоколу IPv6 со всех источников (`[::]:*`).


## 4. Проверьте используемые UDP сокеты в Ubuntu, какие протоколы и приложения используют эти порты?


### 4.1. Проверьте используемые UDP сокеты в Ubuntu

```bash
root@netology1:~# ss -uanp
State                 Recv-Q                Send-Q                                Local Address:Port                               Peer Address:Port               Process
UNCONN                0                     0                                     127.0.0.53%lo:53                                      0.0.0.0:*                   users:(("systemd-resolve",pid=566,fd=12))
UNCONN                0                     0                                    10.0.2.15%eth0:68                                      0.0.0.0:*                   users:(("systemd-network",pid=399,fd=15))
UNCONN                0                     0                                           0.0.0.0:111                                     0.0.0.0:*                   users:(("rpcbind",pid=565,fd=5),("systemd",pid=1,fd=45))
UNCONN                0                     0                                              [::]:111                                        [::]:*                   users:(("rpcbind",pid=565,fd=7),("systemd",pid=1,fd=47))
```

### 4.2. Какие протоколы и приложения используют эти порты?

`UNCONN                0                     0                                     127.0.0.53%lo:53                                      0.0.0.0:*                   users:(("systemd-resolve",pid=566,fd=12))` Протокол - UDP/IPv4, порт - 53, приложение - "systemd-resolve",pid=566 (локальный DNS)

`UNCONN                0                     0                                    10.0.2.15%eth0:68                                      0.0.0.0:*                   users:(("systemd-network",pid=399,fd=15))` Протокол - UDP/IPv4, порт - 68, приложение - "systemd-network",pid=399 (системный демон для управления сетевыми настройками)


`UNCONN                0                     0                                           0.0.0.0:111                                     0.0.0.0:*                   users:(("rpcbind",pid=565,fd=5),("systemd",pid=1,fd=45))` Протокол - UDP/IPv4, порт - 111, приложение - "rpcbind",pid=565 (демон, сопоставляющий универсальные адреса и номера программ RPC)

`UNCONN                0                     0                                              [::]:111                                        [::]:*                   users:(("rpcbind",pid=565,fd=7),("systemd",pid=1,fd=47))` - Протокол - UDP/IPv6, порт - 111, приложение - "rpcbind",pid=565 (демон, сопоставляющий универсальные адреса и номера программ RPC)


## 5. Используя diagrams.net, создайте L3 диаграмму вашей домашней сети или любой другой сети, с которой вы работали. 

![**Диаграмма сети**](https://1.ru "Диаграмма сети")

---
## Задание для самостоятельной отработки (необязательно к выполнению)

## 6*. Установите Nginx, настройте в режиме балансировщика TCP или UDP.

## 7*. Установите bird2, настройте динамический протокол маршрутизации RIP.

## 8*. Установите Netbox, создайте несколько IP префиксов, используя curl проверьте работу API.

---

