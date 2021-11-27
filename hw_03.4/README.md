# Домашнее задание к занятию "3.4. Операционные системы, лекция 2"

## 1. На лекции мы познакомились с [node_exporter](https://github.com/prometheus/node_exporter/releases). В демонстрации его исполняемый файл запускался в background. Этого достаточно для демо, но не для настоящей production-системы, где процессы должны находиться под внешним управлением. 

### 1.1. Используя знания из лекции по systemd, создайте самостоятельно простой [unit-файл](https://www.freedesktop.org/software/systemd/man/systemd.service.html) для node_exporter:

**UNIT-file:**

```bash
root@vagrant:~# cat > node_exporter.service
    [Unit]
    Description=Node Exporter Service
    After=network.target
    
    [Service]
    User=nodeusr
    Group=nodeusr
    Type=simple
    ExecStart=/usr/local/bin/node_exporter
    ExecReload=/bin/kill -HUP $MAINPID
    Restart=on-failure
    
    [Install]
    WantedBy=multi-user.target

```

### 1.2. Поместите его в автозагрузку,

```bash
root@vagrant:~# cp node_exporter.service /etc/systemd/system
root@vagrant:~# systemctl enable node_exporter
...
         node_exporter.service - Node Exporter Service
             Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
...
```

### 1.3. Предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на `systemctl cat cron`),

**Создадим файл с описанием параметров запуска:** 

```bash
root@vagrant:~# cat /etc/node_exporter.cfg
    OPTIONS='--collector.systemd'
```

**Отредактируем файл `/etc/systemd/system/node_exporter.service`:**

```bash
root@vagrant:~# nano /etc/systemd/system/node_exporter.service
```

**Добавим в секцию `Service` параметры для запуска и расположение файла с ними:**

>[Service]  
>...  
>EnvironmentFile=/etc/node_exporter.cfg  
>ExecStart=/usr/local/bin/node_exporter ${OPTIONS}  
>...  

**Перечитаем файлы конфигурации и перезапустим процесс `node_exporter`. После чего проверим состояние процесса. Видно, что процесс запущен с параметром `-collector.systemd` из файла `/etc/node_exporter.cfg`:**

```bash
root@vagrant:~# systemctl daemon-reload
root@vagrant:~# systemctl restart node_exporter
root@vagrant:~# systemctl status node_exporter
● node_exporter.service - Node Exporter Service
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2021-11-27 10:39:19 UTC; 7min ago
   Main PID: 3029 (node_exporter)
      Tasks: 8 (limit: 1071)
     Memory: 8.6M
     CGroup: /system.slice/node_exporter.service
             └─3029 /usr/local/bin/node_exporter --collector.systemd
```
    
### 1.4. Удостоверьтесь, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается.

**Проверено, процесс стартует после перезагрузки и управляется через `systemctl` корректно.**

**Например:**

```bash
root@vagrant:~# systemctl stop node_exporter
root@vagrant:~# systemctl status node_exporter
● node_exporter.service - Node Exporter Service
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: inactive (dead) since Sat 2021-11-27 10:48:03 UTC; 1s ago
    Process: 3029 ExecStart=/usr/local/bin/node_exporter ${OPTIONS} (code=killed, signal=TERM)
   Main PID: 3029 (code=killed, signal=TERM)

...
Nov 27 10:48:03 vagrant systemd[1]: Stopping Node Exporter Service...
Nov 27 10:48:03 vagrant systemd[1]: node_exporter.service: Succeeded.
Nov 27 10:48:03 vagrant systemd[1]: Stopped Node Exporter Service.

root@vagrant:~# systemctl start node_exporter
root@vagrant:~# systemctl status node_exporter
● node_exporter.service - Node Exporter Service
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2021-11-27 10:48:16 UTC; 3s ago
   Main PID: 3076 (node_exporter)
      Tasks: 5 (limit: 1071)
     Memory: 2.9M
     CGroup: /system.slice/node_exporter.service
             └─3076 /usr/local/bin/node_exporter --collector.systemd
```

## 2. Ознакомьтесь с опциями node_exporter и выводом `/metrics` по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.

**Базовые метрики не очень удобны для мониторинга "руками". Но если использовать, то возможно есть смысл использовать эти метрики:**

**CPU (по каждому ядру):**

```bash
# TYPE node_cpu_seconds_total counter
node_cpu_seconds_total{cpu="0",mode="idle"} 5781.19
node_cpu_seconds_total{cpu="0",mode="iowait"} 28.36
node_cpu_seconds_total{cpu="0",mode="irq"} 0
node_cpu_seconds_total{cpu="0",mode="nice"} 0.07
node_cpu_seconds_total{cpu="0",mode="softirq"} 19.8
node_cpu_seconds_total{cpu="0",mode="steal"} 0
node_cpu_seconds_total{cpu="0",mode="system"} 134.97
node_cpu_seconds_total{cpu="0",mode="user"} 155.62
```

**Память:**

```bash
node_memory_MemAvailable_bytes 5.90307328e+08
node_memory_MemFree_bytes 1.28958464e+08
node_memory_MemTotal_bytes 1.028694016e+09
```

**Диски (по каждому диску) - IOPS, прочитано байтб записано байт.**
**Нужно смотреть в динамике:**

```bash
node_disk_io_now{device="sda"} 0
node_disk_read_bytes_total{device="sda"} 8.92548096e+08
node_disk_written_bytes_total{device="sda"} 1.082418176e+09
```

**Сетевые адаптеры (по интересующим нас интерфейсам). Для контроля скорости, ошибок и перегрузки на интерфейсе:**
**Нужно смотреть в динамике:**

```bash
node_network_receive_bytes_total{device="eth0"} 9.9387647e+07
node_network_receive_packets_total{device="eth0"} 89626
node_network_receive_drop_total{device="eth0"} 0
node_network_receive_errs_total{device="eth0"} 0
node_network_transmit_bytes_total{device="eth0"} 1.4594385e+07
node_network_transmit_packets_total{device="eth0"} 34929
node_network_transmit_colls_total{device="eth0"} 0
node_network_transmit_drop_total{device="eth0"} 0
node_network_transmit_errs_total{device="eth0"} 0
```

## 3. Установите в свою виртуальную машину [Netdata](https://github.com/netdata/netdata). Воспользуйтесь [готовыми пакетами](https://packagecloud.io/netdata/netdata/install) для установки (`sudo apt install -y netdata`). После успешной установки:

**Установлено**

```bash
    root@vagrant:~# apt list netdata
    Listing... Done
    netdata/focal,focal,now 1.19.0-3ubuntu1 all [installed]
```

* в конфигурационном файле `/etc/netdata/netdata.conf` в секции [web] замените значение с localhost на `bind to = 0.0.0.0

```bash
    root@vagrant:~# cat /etc/netdata/netdata.conf | grep sock
            # bind socket to IP = 127.0.0.1
            bind socket to IP = 0.0.0.0
```

* добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте `vagrant reload`:
```bash
    config.vm.network "forwarded_port", guest: 19999, host: 19999
```

После успешной перезагрузки в браузере *на своем ПК* (не в виртуальной машине) вы должны суметь зайти на `localhost:19999`. Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.

Консоль загрузилась успешно:
!["Netdata Dashboard"](https://github.com/OleKirs/devops-netology/blob/main/hw_03.4/hw3.4-1.png "Netdata Dashboard")


## 4. Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?

**ОС получает информацию о работt в вируальном окружении:**

```bash
root@vagrant:~# dmesg | grep virtual
[    0.021197] CPU MTRRs all blank - virtualized system.
[    2.970903] Booting paravirtualized kernel on KVM
[   10.210413] systemd[1]: Detected virtualization oracle.
```

**Видно, что ОС загружена в режиме паравиртуализации на KVM - `Booting paravirtualized kernel on KVM`. И, далее, видно, что обнаружена виртуализация Oracle (VirtualBox) - `Detected virtualization oracle`**

## 5. Как настроен sysctl `fs.nr_open` на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (`ulimit --help`)?

***Как настроен sysctl `fs.nr_open` на системе по-умолчанию?***
```bash
root@vagrant:~# /sbin/sysctl -n fs.nr_open
1048576
```

***Узнайте, что означает этот параметр.***

[Documentation for /proc/sys/fs/](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/fs.html)


>**nr_open**  
>  
>*This denotes the maximum number of file-handles a process can allocate. Default value is 1024x1024 (1048576) which should be enough for most machines. Actual limit depends on RLIMIT_NOFILE resource limit.*

***Какой другой существующий лимит не позволит достичь такого числа (`ulimit --help`)***

Параметр `Soft limit` на `open files` (по умолчанию = 1024, просмотреть можно командой `ulimit -Sn`) не позволит достичь лимита заданного в `/proc/sys/fs/`. При необходимости `Soft limit` может быть увеличен в процессе работы, но не больше `Hard limit` (`ulimit -Hn`) .

```bash
root@vagrant:~# ulimit --help
ulimit: ulimit [-SHabcdefiklmnpqrstuvxPT] [limit]
    Modify shell resource limits.

    Provides control over the resources available to the shell and processes
    it creates, on systems that allow such control.

    Options:
      -S        use the `soft' resource limit
      -H        use the `hard' resource limit
    ...
      -n        the maximum number of open file descriptors
    ...

    If LIMIT is given, it is the new value of the specified resource; the
    special LIMIT values `soft', `hard', and `unlimited` stand for the
    current soft limit, the current hard limit, and no limit, respectively.
    Otherwise, the current value of the specified resource is printed.  If
    no option is given, then -f is assumed.

    Values are in 1024-byte increments, except for -t, which is in seconds,
    -p, which is in increments of 512 bytes, and -u, which is an unscaled
    number of processes.
...
root@vagrant:~# ulimit -Sn
1024
root@vagrant:~# ulimit -Hn
1048576
```

## 6. Запустите любой долгоживущий процесс (не `ls`, который отработает мгновенно, а, например, `sleep 1h`) в отдельном неймспейсе процессов; покажите, что ваш процесс работает под PID 1 через `nsenter`. Для простоты работайте в данном задании под root (`sudo -i`). Под обычным пользователем требуются дополнительные опции (`--map-root-user`) и т.д.

**Командой `unshare` запустим процесс `sleep` в отдельном namespace**

```bash
vagrant@vagrant:~$ sudo unshare -u -fp --mount-proc sleep 1h
```

**Из другого сеанса найдем PID запущенного процесса `sleep` (здесь PID=1339), подключимся к нему с использованием `nsenter` (в приглашении изменится рабочий каталог) и выведем список процессов в этом изолированном namespace. Процесс `sleep` имеет PID=1 и PPID=0. Второе подключение имеет PID=2 и PPID=0 для командной оболочки `/bin/bash`, которая является родителем для процесса `ps` с PID=54**

```bash
root@vagrant:~# ps -e| grep sleep
   1339 pts/1    00:00:00 sleep
root@vagrant:~# nsenter -p -m -t 1339
root@vagrant:/# ps -al
F S   UID     PID    PPID  C PRI  NI ADDR SZ WCHAN  TTY          TIME CMD
4 S     0       1       0  0  80   0 -  2019 hrtime pts/1    00:00:00 sleep
0 S     0       2       0  0  80   0 -  2459 do_wai pts/0    00:00:00 bash
0 R     0      54       2  0  80   0 -  2853 -      pts/0    00:00:00 ps
```

## 7. Найдите информацию о том, что такое `:(){ :|:& };:`. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04 (**это важно, поведение в других ОС не проверялось**). Некоторое время все будет "плохо", после чего (минуты) – ОС должна стабилизироваться. 

***`:(){ :|:& };:` - Логическая бомба (известная также как "fork bomb"), забивающая память системы, что в итоге приводит к её зависанию.***  

**Другая запись (не "односторочник"):**

```bash
    fncton() {
        fncton | fncton &
        };
    fncton
```
**Этот код создаёт функцию, которая запускает два своих экземпляра, которые снова запускают эту функцию до тех пор, пока не закончится память.**  

**Другие варианты "бомбы" на сайте Википедии:** [**Fork-бомба**](https://ru.wikipedia.org/wiki/Fork-%D0%B1%D0%BE%D0%BC%D0%B1%D0%B0)

## Вызов `dmesg` расскажет, какой механизм помог автоматической стабилизации. 

```bash
vagrant@vagrant:~$ dmesg | grep fork
[ 1655.040067] cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-3.scope
```

## Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?

**Управление максимальным количеством одновременно запущенных пользователем процессов выполняется командой `ulimit`:**

```bash
root@vagrant:/# ulimit --help
...
      -u        the maximum number of user processes
...
```

**Определим значение по-умолчанию**

```bash
root@vagrant:/# ulimit -u
3571
```

**Установим ограничение для пользователя в 1000 процессов:**

```bash
root@vagrant:/# ulimit -u 1000
root@vagrant:/# ulimit -u
1000
```
