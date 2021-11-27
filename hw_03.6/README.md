# Домашнее задание к занятию "3.6. Компьютерные сети, лекция 1"

## 1. Работа c HTTP через телнет.

* Подключитесь утилитой телнет к сайту stackoverflow.com `telnet stackoverflow.com 80`

```bash
root@vagrant:~# telnet stackoverflow.com 80
Trying 151.101.65.69...
Connected to stackoverflow.com.
Escape character is '^]'.
```

* Отправьте HTTP запрос
```bash
GET /questions HTTP/1.0
HOST: stackoverflow.com
[press enter]
[press enter]
```

* В ответе укажите полученный HTTP код, что он означает?
 
**Ответ: получен код `301 Moved Permanently`, который означает, что ресурс перемещён на постоянной основе (перманентный редирект) на новый адрес указанный в поле `location`**

```bash
HTTP/1.1 301 Moved Permanently
cache-control: no-cache, no-store, must-revalidate
location: https://stackoverflow.com/questions
x-request-guid: 342ae2bc-d907-4948-8290-45bf350a7f28
feature-policy: microphone 'none'; speaker 'none'
content-security-policy: upgrade-insecure-requests; frame-ancestors 'self' https://stackexchange.com
Accept-Ranges: bytes
Date: Sat, 27 Nov 2021 20:50:25 GMT
Via: 1.1 varnish
Connection: close
X-Served-By: cache-hhn4074-HHN
X-Cache: MISS
X-Cache-Hits: 0
X-Timer: S1638046225.842586,VS0,VE184
Vary: Fastly-SSL
X-DNS-Prefetch-Control: off
Set-Cookie: prov=54814b61-6c7b-5fd9-6948-5cf68f79f1cd; domain=.stackoverflow.com; expires=Fri, 01-Jan-2055 00:00:00 GMT; path=/; HttpOnly

Connection closed by foreign host.
```

## 2.   Повторите задание 1 в браузере, используя консоль разработчика F12.

* откройте вкладку Network
* отправьте запрос http://stackoverflow.com
* найдите первый ответ HTTP сервера, откройте вкладку Headers
* укажите в ответе полученный HTTP код.

**IE11 возвращает ошибку 301 и не продолжает обработку (не срабатывает автопереход).**

**Firefox и Chrome сразу переходят на HTTPS (ошибка 301 даже не отображается в истории загрузки) и начинают показывать историю с кода 200 "OK" на URL = https://stackoverflow.com/**

* проверьте время загрузки страницы, какой запрос обрабатывался дольше всего?
Дольше всего (573 мс) обрабатывался запрос на загрузку самого документа:

```bash
curl "https://stackoverflow.com/" ^
  -H "authority: stackoverflow.com" ^
  -H "sec-ch-ua: ^\^" Not A;Brand^\^";v=^\^"99^\^", ^\^"Chromium^\^";v=^\^"96^\^", ^\^"Google Chrome^\^";v=^\^"96^\^"" ^
  -H "sec-ch-ua-mobile: ?0" ^
  -H "sec-ch-ua-platform: ^\^"Windows^\^"" ^
  -H "upgrade-insecure-requests: 1" ^
  -H "user-agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36" ^
  -H "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ^
  -H "sec-fetch-site: none" ^
  -H "sec-fetch-mode: navigate" ^
  -H "sec-fetch-user: ?1" ^
  -H "sec-fetch-dest: document" ^
  -H "accept-language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7" ^
  --compressed
```

* приложите скриншот консоли браузера в ответ.

![Скриншот Google Chrome](https://github.com/OleKirs/devops-netology/blob/main/hw_03.6/hw_03.6-1.png "Скриншот Google Chrome")

## 3. Какой IP адрес у вас в интернете?

```bash
root@vagrant:~# dig +short myip.opendns.com @resolver1.opendns.com
195.144.231.174
```

## 4. Какому провайдеру принадлежит ваш IP адрес? Какой автономной системе AS? Воспользуйтесь утилитой whois

**Провайдер: `PSTAR-MNT` (North-West branch of OJSC MegaFon)**  
  
**Автономная система: `AS20632`**  

```bash
root@vagrant:~# whois 195.144.231.174
% This is the RIPE Database query service.
% The objects are in RPSL format.
%
% The RIPE Database is subject to Terms and Conditions.
% See http://www.ripe.net/db/support/db-terms-conditions.pdf

% Note: this output has been filtered.
%       To receive output for a database update, use the "-B" flag.

% Information related to '195.144.231.172 - 195.144.231.175'

% Abuse contact for '195.144.231.172 - 195.144.231.175' is 'abuse-mailbox@megafon.ru'

inetnum:        195.144.231.172 - 195.144.231.175
netname:        TEKSTIL-REPUBLIK-LAN
descr:          Tekstil Republik
descr:          St.Petersburg
descr:          JSC PeterStar
country:        RU
admin-c:        DTD1-RIPE
tech-c:         DTD1-RIPE
status:         ASSIGNED PA
mnt-by:         PSTAR-MNT
created:        2014-05-23T06:45:55Z
last-modified:  2014-05-23T06:45:55Z
source:         RIPE

role:           MegaFon Network Operation Center
address:        North-West branch of OJSC MegaFon
address:        10, Karavannaya street
address:        Saint-Petersburg, Russia, 191011
phone:          +7 812 329 9090
fax-no:         +7 812 329 9003
abuse-mailbox:  abuse-mailbox@megafon.ru
remarks:        trouble: --------------------------------------------------
remarks:        SPAM and Network security: abuse-mailbox@megafon.ru
remarks:        Technical questions: gnocwest_tr@megafon.ru
remarks:        Routing and peering: gnoceast_backbone@megafon.ru
remarks:        Information: http://www.megafon.ru
remarks:        trouble: --------------------------------------------------
admin-c:        MFON-RIPE
tech-c:         NATS-RIPE
tech-c:         ASIM1-RIPE
tech-c:         KB302-RIPE
tech-c:         TIMP-RIPE
tech-c:         FS1768-RIPE
tech-c:         AA10300-RIPE
tech-c:         MFON-RIPE
nic-hdl:        DTD1-RIPE
mnt-by:         PSTAR-MNT
mnt-by:         MEGAFON-RIPE-MNT
mnt-by:         MEGAFON-GNOC-MNT
mnt-by:         MEGAFON-WEST-MNT
created:        2001-11-27T07:58:31Z
last-modified:  2019-04-22T13:37:41Z
source:         RIPE # Filtered

% Information related to '195.144.224.0/19AS20632'

route:          195.144.224.0/19
descr:          PJSC "Megafon"
descr:          St.Petersburg
mnt-routes:     MEGAFON-AUTO-MNT
origin:         AS20632
mnt-by:         MEGAFON-RIPE-MNT
created:        2004-01-13T07:00:50Z
last-modified:  2020-03-04T14:43:43Z
source:         RIPE

% This query was served by the RIPE Database Query Service version 1.101 (WAGYU)
```

## 5. Через какие сети проходит пакет, отправленный с вашего компьютера на адрес 8.8.8.8? Через какие AS? Воспользуйтесь утилитой `traceroute`

```bash
root@Deb10-Lab:~# traceroute -An 8.8.8.8
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
 1  10.10.7.1 [*]  0.611 ms  1.045 ms  0.649 ms
 2  10.10.0.1 [*]  1.524 ms * *
 3  8.8.8.8 [AS15169]  28.476 ms  32.633 ms  32.361 ms
```

## 6. Повторите задание 5 в утилите mtr. На каком участке наибольшая задержка - delay?

![Скриншот консоли с `mtr`](https://github.com/OleKirs/devops-netology/blob/main/hw_03.6/hw_03.6-2.png "Скриншот консоли с `mtr`")

### На каком участке наибольшая задержка - delay?

**В целом RTT приемлемое. Если смотреть на графу `wrst`, то это ip=74.125.244.180. Но это может быть разовый "провал".**

## 7. Какие DNS сервера отвечают за доменное имя dns.google? Какие A записи? воспользуйтесь утилитой dig

### Какие DNS сервера отвечают за доменное имя `dns.google`?

```bash
root@vagrant:~# dig google.com NS +short
ns2.google.com.
ns1.google.com.
ns3.google.com.
ns4.google.com.
```

### Какие `A` записи?

```bash
root@vagrant:~# dig google.com A +short
173.194.222.100
173.194.222.102
173.194.222.113
173.194.222.138
173.194.222.101
173.194.222.139
```

## 8. Проверьте `PTR` записи для IP адресов из задания 7. Какое доменное имя привязано к IP? воспользуйтесь утилитой `dig`

```bash
root@vagrant:~# dig +short -x 173.194.222.100
lo-in-f100.1e100.net.
root@vagrant:~# dig +short -x 173.194.222.101
lo-in-f101.1e100.net.
root@vagrant:~# dig +short -x 173.194.222.102
lo-in-f102.1e100.net.
root@vagrant:~# dig +short -x 173.194.222.113
lo-in-f113.1e100.net.
root@vagrant:~# dig +short -x 173.194.222.138
lo-in-f138.1e100.net.
root@vagrant:~# dig +short -x 173.194.222.139
lo-in-f139.1e100.net.
```

___