# Домашнее задание к занятию "3.3. Операционные системы, лекция 1"

## 1. Какой системный вызов делает команда `cd`? В прошлом ДЗ мы выяснили, что `cd` не является самостоятельной  программой, это `shell builtin`, поэтому запустить `strace` непосредственно на `cd` не получится. Тем не менее, вы можете запустить `strace` на `/bin/bash -c 'cd /tmp'`. В этом случае вы увидите полный список системных вызовов, которые делает сам `bash` при старте. Вам нужно найти тот единственный, который относится именно к `cd`.
```bash
chdir("/tmp")
```

## 2. Попробуйте использовать команду `file` на объекты разных типов на файловой системе. Например:
    ```bash
    vagrant@netology1:~$ file /dev/tty
    /dev/tty: character special (5/0)
    vagrant@netology1:~$ file /dev/sda
    /dev/sda: block special (8/0)
    vagrant@netology1:~$ file /bin/bash
    /bin/bash: ELF 64-bit LSB shared object, x86-64
    ```
## Используя `strace` выясните, где находится база данных `file` на основании которой она делает свои догадки.
### *Искомая база - `/usr/share/misc/magic.mgc`*

Из описания команды  `file` известно, что она для хранения типов использует базу `magic.mgc`. Для получения её местонахождения найдём упоминания `magig.mgc` в выводе `strace`:

```bash
root@vagrant:~# strace file /dev/sda 2>&1 | grep magic.mgc
stat("/root/.magic.mgc", 0x7ffc6ffd9760) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
```

Есть попытки чтения из домашней директории файла `/root/.magic.mgc` и из `/etc/magic.mgc`  но там такого файла нет : 
    `stat(`***"/root/.magic.mgc"***`, 0x7ffc6ffd9760) = -1 ENOENT` ***(No such file or directory)***
    `openat(AT_FDCWD,` ***"/etc/magic.mgc"***`, O_RDONLY) = -1 ENOENT` ***(No such file or directory)***

Также читается файл `/etc/magic` и база `/usr/share/misc/magic.mgc`:
    `openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3`

## 3. Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).

Как вариант, можно перенаправить вывод из `/dev/null` на файловый дескриптор удалённого файла:
`cat /dev/null >/proc/<#PID>/fd/<#FD>`

***Источники:***
- [**Восстановление открытых файлов но удаленных c файловой системы linux**](https://habr.com/ru/post/208104/)
- [**Как обнулить файл, открытый другим процессом**](https://www.opennet.ru/openforum/vsluhforumID1/84543.html?n=met3x)

***Основываясь на этих материалах выполнено:***  
  3.1. Создадим фоновую задачу `ping 127.0.0.1`, пишущую результат из `stdout` в файл `log1` и запомним её PID (здесь PID=2146):
```bash
    root@vagrant:~# ping 127.0.0.1 > log1 &
    [1] 2146
```
  3.2. Убедимся, что файл лога создан, а затем удалим его и обнаружим дескриптор удалённого файла (#FD = 1) командой `lsof` с PID фоновой задачи, отфильтровав вывод по шаблону `deleted`:
```bash
    root@vagrant:~# ll | grep log
    -rw-r--r--  1 root root   2186 Nov 23 18:30 log1
    root@vagrant:~# rm log1
    root@vagrant:~# lsof -p 2146 | grep deleted
    ping    2146 root    1w   REG  253,0     4158 3538960 /root/log1 (deleted)
```
3.3. Перед сбросом лога фоновой задачи для подтверждения работы команды сброса восстановим вывод лога но уже в другой файл (`log2`) и посчитаем общее количество строк в файле (получилось 105 строк), а затем удалим этот файл для восстановления исходного сосотояния:
```bash
    root@vagrant:~# cp /proc/2146/fd/1 /root/log2
    root@vagrant:~# cat /root/log2 | wc -l
    105
    root@vagrant:~# rm log2
```
3.4. Обнулим лог командой `cat /dev/null >/proc/2146/fd/1`, перенаправим вывод в файл `log3` и посчитаем в нем количество строк (получилось 5 строк), и остановим фоновую задачу.
```bash
    root@vagrant:~# cat /dev/null >/proc/2146/fd/1
    root@vagrant:~# cp /proc/2146/fd/1 /root/log3
    root@vagrant:~# cat /root/log3 | wc -l
    5
    root@vagrant:~# kill 2146
    [1]+  Terminated              ping 127.0.0.1 > log1
```
Таким образом установлено, что выполнение команды "сброса" в виде конструкции `cat /dev/null >/proc/2146/fd/1` "обрезало" лог со 105 до 5 строк. Не нулевой результат при подсчёте строк в логе после "обрезки" обусловлен продолжающейся работой фоновой задачи.

## 4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?
Процесс при завершении (как нормальном, так и в результате не обрабатываемого сигнала) освобождает все свои ресурсы (CPU, RAM, IO) и становится «зомби» — пустой записью в таблице процессов, хранящей статус завершения, предназначенный для чтения родительским процессом.  
Зомби не занимают памяти, но блокируют записи в таблице процессов, размер которой ограничен для каждого пользователя и системы в целом.

## 5. В iovisor BCC есть утилита `opensnoop`:
    ```bash
    root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
    /usr/sbin/opensnoop-bpfcc
    ```
## На какие файлы вы увидели вызовы группы `open` за первую секунду работы утилиты? Воспользуйтесь пакетом `bpfcc-tools` для Ubuntu 20.04. Дополнительные [сведения по установке](https://github.com/iovisor/bcc/blob/master/INSTALL.md).
```bash
    root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
    /usr/sbin/opensnoop-bpfcc
    root@vagrant:~# /usr/sbin/opensnoop-bpfcc
    PID    COMM               FD ERR PATH
    795    vminfo              4   0 /var/run/utmp
    581    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
    581    dbus-daemon        18   0 /usr/share/dbus-1/system-services
    581    dbus-daemon        -1   2 /lib/dbus-1/system-services
    581    dbus-daemon        18   0 /var/lib/snapd/dbus-1/system-services/
```
## 6. Какой системный вызов использует `uname -a`? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в `/proc`, где можно узнать версию ядра и релиз ОС.

*Какой системный вызов использует `uname -a`?* ***системный вызов `uname()`***

*Приведите цитату из `man`..:*
```bash
     Part of the utsname information is also accessible  via  /proc/sys/ker‐
       nel/{ostype, hostname, osrelease, version, domainname}.
```
## 7. Чем отличается последовательность команд через `;` и через `&&` в bash? Например:
    ```bash
    root@netology1:~# test -d /tmp/some_dir; echo Hi
    Hi
    root@netology1:~# test -d /tmp/some_dir && echo Hi
    root@netology1:~#
    ```
`;`  - простой разделитель команд в строке, последующая команда выполнится вне зависимости от результата предыдущей.  
`&&` -  условный оператор, при котором следующая команда выполнится только при условии успешного завершения предыдущей  
```bash
# Выполнить `test` а потом - `echo` 
    root@netology1:~# test -d /tmp/some_dir; echo Hi
    Hi
# Выполнить `test` и при успехе выполнить `echo` 
    root@netology1:~# test -d /tmp/some_dir && echo Hi
    root@netology1:~#
```
Т.к. каталога `/tmp/some_dir` не найдено, во втором случае команда `echo Hi` не выполняется.

##    Есть ли смысл использовать в bash `&&`, если применить `set -e`?

Опция `set -e` - инвертирует стадартное поведение shell (игнорирование ошибок и продолжение работы сценария) и прерывает выполнение команды (например, сценарий shell) с возвратом кода состояния выхода команды, которая завершилась неудачно. Может быть использована для передачи кода возврата из вложенных сценариев (например, при отладке).

`&&`  вместе с `set -e` не требуется, так как при установленном `set -e` при любых не нулевых кодах возврата команд выполнение сценария прекратится.

## 8. Из каких опций состоит режим bash `set -euxo pipefail` и почему его хорошо было бы использовать в сценариях?

`-e` Exit immediately if a pipeline (see Pipelines), which may consist of a single simple command (see Simple Commands), a list (see Lists), or a compound command (see Compound Commands) returns a non-zero status.  

`-u` Treat unset variables and parameters other than the special parameters ‘@’ or ‘*’ as an error when performing parameter expansion. An error message will be written to the standard error, and a non-interactive shell will exit.  

`-x` Print a trace of simple commands, for commands, case commands, select commands, and arithmetic for commands and their arguments or associated word lists after they are expanded and before they are executed.  

`-o pipefail` If set, the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status, or zero if all commands in the pipeline exit successfully. This option is disabled by default.  

**Набор повышает детализацию логирования и, при наличии ошибок (не нулевых кодах возврата), прекратит выполнение сценария с кодом возврата ошибки.**

## 9. Используя `-o stat` для `ps`, определите, какой наиболее часто встречающийся статус у процессов в системе. В `man ps` ознакомьтесь (`/PROCESS STATE CODES`) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).

*...какой наиболее часто встречающийся статус у процессов в системе.*:  
- `I*(I,I<)` - фоновые (Idle) процессы ядра
- `S*(S,S+,Ss,Ss+,Ssl)` - Процессы ожидающие завершения (Sleeping)  

*что значат дополнительные к основной заглавной буквы статуса процессов* - это дополнительные характеристики процесса (приоритет и т.д.)
