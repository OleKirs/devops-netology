# Домашнее задание к занятию "3.2. Работа в терминале, лекция 2"

## 1. Какого типа команда `cd`? Попробуйте объяснить, почему она именно такого типа; опишите ход своих мыслей, если считаете что она могла бы быть другого типа.
`cd` - встроенная команда командной оболочки (например, "bash"). Она обеспечивает базовую функциональность оболочки (навигацию по файловой системе) и на всех системах с данной командной оболочкой должна работать одинаково. Поэтому нет смысла делать её внешней. Если нужен расширенный или изменённый функционал - можно сменить оболочку.
```bash
root@vagrant:~# man bash
...
SHELL BUILTIN COMMANDS
...
       cd [-L|[-P [-e]] [-@]] [dir]
              Change  the  current  directory  to dir.  if dir is not supplied, the value of the HOME shell variable is the default.  Any additional arguments following dir are ignored.  ...
```
## 2. Какая альтернатива без pipe команде `grep <some_string> <some_file> | wc -l`? `man grep` поможет в ответе на этот вопрос. Ознакомьтесь с [документом](http://www.smallo.ruhr.de/award.html) о других подобных некорректных вариантах использования pipe.
```bash
root@vagrant:~# man bash >> man_bash
root@vagrant:~# grep cd man_bash | wc -l
21
root@vagrant:~# grep -c cd man_bash
21
```
## 3. Какой процесс с PID `1` является родителем для всех процессов в вашей виртуальной машине Ubuntu 20.04?
```bash
root@vagrant:~# ps -p 1
    PID TTY          TIME CMD
      1 ?        00:00:05 systemd
```
## 4. Как будет выглядеть команда, которая перенаправит вывод stderr `ls` на другую сессию терминала?
**Session 1 (user: root)** Определение номера рабочей сесии (`pts/0`) и запрос вывода команды `ls` для несуществующего каталога `/testdir` 
```bash
root@vagrant:~# who
vagrant  pts/0        2021-11-19 13:06 (10.0.2.2)
vagrant  pts/1        2021-11-21 08:53 (10.0.2.2)
root@vagrant:~# tty
/dev/pts/0
root@vagrant:~# ls -la /testdir 2> /dev/pts/1
```
**Session 2 (user: vagrant)** Определение номера рабочей сесии (`pts/1`) и вывод сообщения об ошибке из потока `stderr` сессии `pts/0`
```bash
vagrant@vagrant:~$ tty
/dev/pts/1
vagrant@vagrant:~$ ls: cannot access '/testdir': No such file or directory

```
## 5. Получится ли одновременно передать команде файл на stdin и вывести ее stdout в другой файл? Приведите работающий пример.
**Создадим тестовый файл перенаправив вывод косманды `cat` в файл `/root/test1`:**
```bash
root@vagrant:~# cat > /root/test1
#Source: /root/test1
Line 1
Line 2
# EOF
```
**Направим на вход команды `cat` тестовый файл `/root/test1` и выход команды в файл `/root/test2`. При успешном выполнении команды выведем содержимое файла `/root/test2` командой `tail`:**
```bash
root@vagrant:~# cat </root/test1 >/root/test2 && tail /root/test2
#Source: /root/test1
Line 1
Line 2
# EOF
root@vagrant:~#
```

## 6. Получится ли находясь в графическом режиме, вывести данные из PTY в какой-либо из эмуляторов TTY? Сможете ли вы наблюдать выводимые данные?
```bash
root@Deb10-Lab:~# echo "Test message" > /dev/tty1
root@Deb10-Lab:~# tty
/dev/pts/0
root@Deb10-Lab:~#
```
**Сможете ли вы наблюдать выводимые данные?** - *Да, вывод виден в консоли `TTY1`:*

![Вывод из TTY1](https://github.com/OleKirs/devops-netology/blob/main/hw_03.2/hw32-1.png "Вывод из TTY1")
## 7. Выполните команду `bash 5>&1`. К чему она приведет? Что будет, если вы выполните `echo netology > /proc/$$/fd/5`? Почему так происходит?
**Команда `bash 5>&1` создаст дескриптор с номером 5 и перенаправит его на `stdout`**
**При выполнении `echo netology > /proc/$$/fd/5` в консоль текущего сеанса bash будет выведен текст `netology`, тюкю результат команды `echo` будет направлен на поток текущего процесса с дексриптором 5, который перенаправлен на `stdout`**
```bash
root@vagrant:~# bash 5>&1
root@vagrant:~# lsof -a -p $$ -d 5
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
bash    2745 root    5u   CHR  136,0      0t0    3 /dev/pts/0
root@vagrant:~# echo netology > /proc/$$/fd/5
netology
```

## 8. Получится ли в качестве входного потока для pipe использовать только stderr команды, не потеряв при этом отображение stdout на pty? Напоминаем: по умолчанию через pipe передается только stdout команды слева от `|` на stdin команды справа. Это можно сделать, поменяв стандартные потоки местами через промежуточный новый дескриптор, который вы научились создавать в предыдущем вопросе.
Создадим тестовую директорию, тестовые файлы (1.tst, 3,tst и 5.tst) и уберём права доступа на файле 3.tst
```bash
vagrant@vagrant:~$ mkdir ~/tmp
vagrant@vagrant:~$ echo Test1 > ~/tmp/1.tst
vagrant@vagrant:~$ echo Test3 > ~/tmp/3.tst
vagrant@vagrant:~$ echo Test5 > ~/tmp/5.tst
vagrant@vagrant:~$ chmod 000 ~/tmp/3.tst
```
Попробуем прочитать содержимое файлов с 1.tst до 5.tst. Видны различные ошибки доступа ("нет файла" и "нет прав доступа")
```bash
vagrant@vagrant:~$ cat ~/tmp/{1..5}.tst
Test1
cat: /home/vagrant/tmp/2.tst: No such file or directory
cat: /home/vagrant/tmp/3.tst: Permission denied
cat: /home/vagrant/tmp/4.tst: No such file or directory
Test5
```
Перенаправим потоки с использованием доп. потока "3" :
* Перенаправим 1 (`stdout`) в 3 (доп.поток)
* Перенаправим 2 (`stderr`) в освободившийся 1 (`stdout`)
* Направим поток 3 в 2 (`stderr`), который отобразится в PTY (стороки "Test1" и "Test5")

Таким образом, направим поток ошибок команды `cat` на вход "pipe" к команде `grep`, которая подсчитает количество вхождений по шаблону 'No such' (часть вывода при ошибке "No such file or directory") и отобразит результат - "2". 
```bash
vagrant@vagrant:~$ cat ~/tmp/{1..5}.tst 3>&2 2>&1 1>&3 | grep -c 'No such'
Test1
Test5
2
vagrant@vagrant:~$
```

## 9. Что выведет команда `cat /proc/$$/environ`? Как еще можно получить аналогичный по содержанию вывод?
Команда выведет переменные окружения текущего процесса
Из прямых аналогов нашёл только такие конструкции:
```bash
grep -Fz '' /proc/$$/environ
```
Решает проблему 'Useless cat' при поиске конкретных переменных (например, нужно посмотреть только PATH для процесса, запущенного из-под cron)

Команды `env` и `printenv` тоже дают посмотреть переменные, но не нашёл как их ограничить конкретиныь PID

## 10. Используя `man`, опишите что доступно по адресам `/proc/<PID>/cmdline`, `/proc/<PID>/exe`.

```bash
       /proc/[pid]/cmdline
This read-only file holds the complete command line for process, unless the process is a zombie.  In the latter case, there is nothing in this file: that is, a on this file will return 0 characters.  The command-line arguments appear in this file as a set of strings by null bytes ('\0'), with a further null byte after the last string.
```
```bash
/proc/[pid]/exe
Under Linux 2.2 and later, this file is a symbolic link the actual pathname of the executed command.This symbolic link can be dereferenced normally; to open it will open the executable.  You can even type /proc/[pid]/exe to run another copy of the same that is being run by process [pid].  If the pathname has been unlinked, the symbolic link will contain string '(deleted)' appended to the original pathname. a multithreaded process, the contents of this symbolic are not available if the main thread has already (typically by calling pthread_exit(3)).
```
*Например, можно использовать так:*
```bash
vagrant@vagrant:~$ ls -l /proc/$$/{exe,cwd}
lrwxrwxrwx 1 vagrant vagrant 0 Nov 21 13:06 /proc/870/cwd -> /home/vagrant
lrwxrwxrwx 1 vagrant vagrant 0 Nov 21 13:06 /proc/870/exe -> /usr/bin/bash
```
## 11. Узнайте, какую наиболее старшую версию набора инструкций SSE поддерживает ваш процессор с помощью `/proc/cpuinfo`.
**sse4_2 (SSE 4.2)**
```bash
vagrant@vagrant:~$ grep -F sse /proc/cpuinfo
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl xtopology cpuid tsc_known_freq pni pclmulqdq ssse3 cx16 sse4_1 sse4_2 x2apic popcnt aes xsave avx hypervisor lahf_lm pti md_clear flush_l1d arch_capabilities
```
## 12. При открытии нового окна терминала и `vagrant ssh` создается новая сессия и выделяется pty. Это можно подтвердить командой `tty`, которая упоминалась в лекции 3.2. Однако:

    ```bash
	vagrant@netology1:~$ ssh localhost 'tty'
	not a tty
    ```

почитайте, почему так происходит, и как изменить поведение.
По умолчанию при соедиении через SSH с последующим запуском улалённых комманд TTY не используется. Для принудительного запуска с TTY используется ключ `-t` (см. ниже)
```bash
NAME
ssh
 - OpenSSH SSH client (remote login program)
...
-t
    Force pseudo-tty allocation. This can be used to execute arbitrary screen-based programs on a remote machine, which can be very useful, e.g., when implementing menu services. Multiple -t options force tty allocation, even if ssh has no local tty. 
```

## 13. Бывает, что есть необходимость переместить запущенный процесс из одной сессии в другую. Попробуйте сделать это, воспользовавшись `reptyr`. Например, так можно перенести в `screen` процесс, который вы запустили по ошибке в обычной SSH-сессии.
**Выполнено.**
Потребовалось переопределить параметры:
```bash
root@vagrant:~# echo 0 > /proc/sys/kernel/yama/ptrace_scope
```
## 14. `sudo echo string > /root/new_file` не даст выполнить перенаправление под обычным пользователем, так как перенаправлением занимается процесс shell'а, который запущен без `sudo` под вашим пользователем. Для решения данной проблемы можно использовать конструкцию `echo string | sudo tee /root/new_file`. Узнайте что делает команда `tee` и почему в отличие от `sudo echo` команда с `sudo tee` будет работать.

Т.к. в конструкции  `echo string | sudo tee /root/new_file` команда `tee` не использует перенаправления, то для неё работают разрешения суперпользователя (заданные командой `sudo`) с правом записи в каталог `/root`. При этом она может получать через `pipe` данные из потока стандартного вывода команды `echo`, даже если `echo` запущена без повышенных прав. 

```bash
TEE(1)                                                                                                    User Commands                                                                                                    TEE(1)

NAME
       tee - read from standard input and write to standard output and files
```
