# Домашнее задание к занятию "3.9. Элементы безопасности информационных систем"

## 1. Установите Bitwarden плагин для браузера. Зарегестрируйтесь и сохраните несколько паролей.

![Bitwarden плагин для браузера](imgs/hw_03.9_pic_01.png "Bitwarden плагин для браузера")

## 2. Установите Google authenticator на мобильный телефон. Настройте вход в Bitwarden акаунт через Google authenticator OTP.

### 2.1. Установите Google authenticator на мобильный телефон.  

**Выполнено**  

### 2.2. Настройте вход в Bitwarden акаунт через Google authenticator OTP.  

**Выполнено по [инструкции "Bitwarden Authenticator (TOTP)"](https://bitwarden.com/help/article/authenticator-keys/)**  

![вход в Bitwarden акаунт через Google authenticator OTP](imgs/hw_03.9_pic_02.png "вход в Bitwarden акаунт через Google authenticator OTP")  

Здесь:  

 * #1 - Приглашение Bitwarden на ввод логина и пароля  
 * #2 - Приглашение Bitwarden на 6-цифрового OTP (One Time Password) из программы "Google authenticator"  
 * #3 - Отображение главного окна приложения в браузере после успешного входа.  


## 3. Установите apache2, сгенерируйте самоподписанный сертификат, настройте тестовый сайт для работы по HTTPS.

### 3.1. Установите apache2

Проверим имя ВМ и локальные адреса:
```bash
root@netology1:~# hostname -s
netology1
root@netology1:~# hostname -f
netology1.netology.test
root@netology1:~# hostname -i
127.0.0.1 10.0.2.15
root@netology1:/etc/apache2# cat /etc/hostname
netology1.netology.test
root@netology1:/etc/apache2# cat /etc/hosts
127.0.0.1       localhost
...
127.0.0.1       netology1.netology.test netology1
10.0.2.15       netology1.netology.test netology1
...
```

Установим пакет Apache2 из репозитория:

```bash
root@netology1:~# apt install apache2
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  apache2-bin apache2-data apache2-utils libapr1 libaprutil1 libaprutil1-dbd-sqlite3 libaprutil1-ldap libjansson4 liblua5.2-0 ssl-cert
...
```

Проверим, что сервис установлен:
```bash
root@netology1:~# systemctl status apache2
● apache2.service - The Apache HTTP Server
     Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2021-12-13 07:25:59 UTC; 20s ago
       Docs: https://httpd.apache.org/docs/2.4/
   Main PID: 1411 (apache2)
      Tasks: 55 (limit: 1071)
     Memory: 5.6M
     CGroup: /system.slice/apache2.service
             ├─1411 /usr/sbin/apache2 -k start
             ├─1412 /usr/sbin/apache2 -k start
             └─1413 /usr/sbin/apache2 -k start

Dec 13 07:25:58 netology1.netology.test systemd[1]: Starting The Apache HTTP Server...
Dec 13 07:25:59 netology1.netology.test systemd[1]: Started The Apache HTTP Server.
```

### 3.2. Сгенерируйте самоподписанный сертификат.

Сгенерируем с помощью OpenSSL самоподписанный серитификат и включим поддержку SSl в Apache:

```bash
root@netology1:~# cd /etc/apache2
root@netology1:/etc/apache2# mkdir ssl ; cd ssl
root@netology1:/etc/apache2/ssl# openssl req -new -x509 -days 731 -nodes -out cert.pem -keyout cert.key -subj "/C=RU/ST=SPb/L=SPb/O=Global Security/OU=IT Dept/CN=netology1.netology.test/CN=netology1"
...

root@netology1:/etc/apache2/ssl# apachectl -M | grep ssl
root@netology1:/etc/apache2/ssl# a2enmod ssl
Considering dependency setenvif for ssl:
...
Enabling module ssl.
See /usr/share/doc/apache2/README.Debian.gz on how to configure SSL and create self-signed certificates.
To activate the new configuration, you need to run:
  systemctl restart apache2
root@netology1:/etc/apache2/ssl# systemctl restart apache2
```

### 3.3. Настройте тестовый сайт для работы по HTTPS

 Сконфигурируем виртуальный домен по-умолчанию на использование SSL и установим ключи шифрования для HTTPS. Затем, проверим правильность синтаксиса конфигурации, перечитаем конфигурацию Apache и применим изменения:
 
```bash
root@netology1:/etc/apache2# cat /etc/apache2/sites-enabled/010-site.conf
<VirtualHost *:443>
    ServerName netology.test
    DocumentRoot /var/www/html
    SSLEngine on
    SSLCertificateFile ssl/cert.pem
    SSLCertificateKeyFile ssl/cert.key
</VirtualHost>
root@netology1:/etc/apache2# apachectl configtest
Syntax OK
root@netology1:/etc/apache2# apachectl graceful
```

### 3.4. Проверим доступность web-документа:  

При попытке получить документ с помощью `curl` без указания ключей, получим ошибку, т.к. используется самоподписанный сертификат:  

```bash
$ curl https://netology1.netology.test:8443
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (60) SSL certificate problem: self signed certificate
More details here: https://curl.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
how to fix it, please visit the web page mentioned above.
```

Повторим с ключом `--insecure`, для игнорирования ошибки. Документ с сервера Apache получен:  

```bash
Administrator@TESTHOST51 MINGW64 /
$ curl https://netology1.netology.test:8443 --insecure
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <!--
    Modified from the Debian original for Ubuntu
    Last updated: 2016-11-16
    See: https://launchpad.net/bugs/1288690
  -->
  <head>
    ...
</html>
```

Проверим в браузере:

![Проверка доступности web-документа в браузере](imgs/hw_03.9_pic_03.png "Проверка доступности web-документа в браузере")  

Видно, что документ доступен после добавления его в исключения проверки безопасности соединения из-за самоподписанного сертификата.

## 4. Проверьте на TLS уязвимости произвольный сайт в интернете.

Выполнено на примере сайта "https://www.hackthissite.org/":

```bash
root@netology1:~/testssl/testssl.sh# ./testssl.sh -e --fast --parallel https://www.hackthissite.org/

###########################################################
    testssl.sh       3.1dev from https://testssl.sh/dev/
    (6da72bc 2021-12-10 20:16:28 -- )

      This program is free software. Distribution and
             modification under GPLv2 permitted.
      USAGE w/o ANY WARRANTY. USE IT AT YOUR OWN RISK!

       Please file bugs @ https://testssl.sh/bugs/

###########################################################

 Using "OpenSSL 1.0.2-chacha (1.0.2k-dev)" [~183 ciphers]
 on netology1:./bin/openssl.Linux.x86_64
 (built: "Jan 18 17:12:17 2019", platform: "linux-x86_64")


Testing all IPv4 addresses (port 443): 137.74.187.104 137.74.187.100 137.74.187.102 137.74.187.101 137.74.187.103
-----------------------------------------------------------------------------------------------------------------------------------------
 Start 2021-12-13 09:43:13        -->> 137.74.187.104:443 (www.hackthissite.org) <<--

 Further IP addresses:   137.74.187.100 137.74.187.102 137.74.187.101 137.74.187.103 2001:41d0:8:ccd8:137:74:187:103 2001:41d0:8:ccd8:137:74:187:102 2001:41d0:8:ccd8:137:74:187:101
                         2001:41d0:8:ccd8:137:74:187:104 2001:41d0:8:ccd8:137:74:187:100
 rDNS (137.74.187.104):  hackthissite.org.
 Service detected:       HTTP



 Testing all 183 locally available ciphers against the server, ordered by encryption strength


Hexcode  Cipher Suite Name (OpenSSL)       KeyExch.   Encryption  Bits     Cipher Suite Name (IANA/RFC)
-----------------------------------------------------------------------------------------------------------------------------
 xc030   ECDHE-RSA-AES256-GCM-SHA384       ECDH 256   AESGCM      256      TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
 xc028   ECDHE-RSA-AES256-SHA384           ECDH 256   AES         256      TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
 x9d     AES256-GCM-SHA384                 RSA        AESGCM      256      TLS_RSA_WITH_AES_256_GCM_SHA384
 x3d     AES256-SHA256                     RSA        AES         256      TLS_RSA_WITH_AES_256_CBC_SHA256
 xc02f   ECDHE-RSA-AES128-GCM-SHA256       ECDH 256   AESGCM      128      TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
 xc027   ECDHE-RSA-AES128-SHA256           ECDH 256   AES         128      TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256
 x9c     AES128-GCM-SHA256                 RSA        AESGCM      128      TLS_RSA_WITH_AES_128_GCM_SHA256
 x3c     AES128-SHA256                     RSA        AES         128      TLS_RSA_WITH_AES_128_CBC_SHA256


 Done 2021-12-13 09:43:20 [  12s] -->> 137.74.187.104:443 (www.hackthissite.org) <<--

-----------------------------------------------------------------------------------------------------------------------------------------
 Start 2021-12-13 09:43:20        -->> 137.74.187.100:443 (www.hackthissite.org) <<--

 Further IP addresses:   137.74.187.104 137.74.187.102 137.74.187.101 137.74.187.103 2001:41d0:8:ccd8:137:74:187:103 2001:41d0:8:ccd8:137:74:187:102 2001:41d0:8:ccd8:137:74:187:101
                         2001:41d0:8:ccd8:137:74:187:104 2001:41d0:8:ccd8:137:74:187:100
 rDNS (137.74.187.100):  hackthissite.org.
 Service detected:       HTTP



...


 Done 2021-12-13 09:43:51 [  43s] -->> 137.74.187.103:443 (www.hackthissite.org) <<--

-----------------------------------------------------------------------------------------------------------------------------------------
Done testing now all IP addresses (on port 443): 137.74.187.104 137.74.187.100 137.74.187.102 137.74.187.101 137.74.187.103
```

## 5. Установите на Ubuntu ssh сервер, сгенерируйте новый приватный ключ. Скопируйте свой публичный ключ на другой сервер. Подключитесь к серверу по SSH-ключу.

### 5.1. Установите на Ubuntu ssh сервер, сгенерируйте новый приватный ключ.

```bash
root@netology1:~/testssl/testssl.sh# apt install openssh-server
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  openssh-client openssh-sftp-server
...

root@netology1:~/testssl/testssl.sh# ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa):
...

root@netology1:~# ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa): /root/.ssh/id_rsa_v2
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /root/.ssh/id_rsa_v2
Your public key has been saved in /root/.ssh/id_rsa_v2.pub
The key fingerprint is:
SHA256:byuQavvL+iYqILGhxNJJWlw4DiO7BPVnvUw4iqF0hDQ root@netology1.netology.test
The key's randomart image is:
+---[RSA 3072]----+
|.Eo+.            |
|=.O.   o         |
|+@.+. = o        |
|B==o + + .       |
|*=. .  .S        |
|*     o  .       |
|o    . .  o      |
|.   +.. .. .     |
| ..ooB=. ..      |
+----[SHA256]-----+
root@netology1:~# 
```

### 5.2. Скопируйте свой публичный ключ на другой сервер. Подключитесь к серверу по SSH-ключу.

Скопируем ключ с помощью команды `ssh-copy-id` и подключимся без ввода пароля (с помощью ключа):  

```bash
$ ssh-copy-id -f -p 2222 vagrant@127.0.0.1
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/c/Users/Administrator/.ssh/id_rsa.pub"

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh -p '2222' 'vagrant@127.0.0.1'"
and check to make sure that only the key(s) you wanted were added.
$ ssh -p '2222' 'vagrant@127.0.0.1'
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon 13 Dec 2021 10:26:15 AM UTC

  System load:  0.0               Processes:             123
  Usage of /:   2.5% of 61.31GB   Users logged in:       2
  Memory usage: 19%               IPv4 address for eth0: 10.0.2.15
  Swap usage:   0%


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Mon Dec 13 09:58:47 2021 from 10.0.2.2
vagrant@netology1:~$
```
 
## 6. Переименуйте файлы ключей из задания 5. Настройте файл конфигурации SSH клиента, так чтобы вход на удаленный сервер осуществлялся по имени сервера.

### 6.1. Переименуйте файлы ключей из задания 5.

```bash
mv ~/.ssh/id_rsa ~/.ssh/id_rsa_v2
```

### 6.2. Настройте файл конфигурации SSH клиента, так чтобы вход на удаленный сервер осуществлялся по имени сервера.

Настроим соединение по SSH с сервером "netology2" c указанием имении и ключа шифрования.

```bash
root@netology1:~/.ssh# cat ./config
Host netology2
  HostName netology2
  IdentityFile ~/.ssh/id_rsa_v2
  User root
  #Port 2222
  #StrictHostKeyChecking no
Host *
  User vagrant
  IdentityFile ~/.ssh/id_rsa
```

Проверим, подключившись только по имени сервера командой `ssh <ИмяСервера>`:

```bash
root@netology1:~/.ssh# ssh netology2
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon 13 Dec 2021 10:48:18 AM UTC

  System load:  0.0               Processes:             116
  Usage of /:   2.5% of 61.31GB   Users logged in:       1
  Memory usage: 16%               IPv4 address for eth0: 10.0.2.15
  Swap usage:   0%                IPv4 address for eth1: 172.28.128.60


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

root@netology2:~#
```

Подключение успешно.

## 7. Соберите дамп трафика утилитой tcpdump в формате pcap, 100 пакетов. Откройте файл pcap в Wireshark.

### 7.1. Соберите дамп трафика утилитой tcpdump в формате pcap, 100 пакетов.
```bash
root@netology1:~# tcpdump -i eth0 -c 100 -w dump_eth0.pcap
tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
100 packets captured
100 packets received by filter
0 packets dropped by kernel
root@netology1:~#
```

### 7.2. Откройте файл pcap в Wireshark.

![Файл `dump_eth0.pcap`, открытый в Wireshark](imgs/hw_03.9_pic_07.png "Файл `dump_eth0.pcap`, открытый в Wireshark")  


 ---
## Задание для самостоятельной отработки (необязательно к выполнению)

## 8*. Просканируйте хост scanme.nmap.org. Какие сервисы запущены?

## 9*. Установите и настройте фаервол ufw на web-сервер из задания 3. Откройте доступ снаружи только к портам 22,80,443


 ---


