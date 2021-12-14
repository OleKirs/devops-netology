# Домашнее задание к занятию "4.1. Командная оболочка Bash: Практические навыки"

## Обязательная задача 1

### Есть скрипт:
```bash
a=1
b=2
c=a+b
d=$a+$b
e=$(($a+$b))
```

### Какие значения переменным c,d,e будут присвоены? Почему?

| Переменная  | Значение | Обоснование |
| ------------- | ------------- | ------------- |
| `c`  | a+b  | переменной строкового типа 'с' присвоено значение 'a+b', т.к. 'a', '+' и 'b' здесь являются просто символами ASCII, которые перечислены в последовательности, определённой в правой части оператора присвоения значения  |
| `d`  | 1+2  | переменной строкового типа 'd' присвоено значение '1+2', т.к. '$a' и '$b' здесь являются строчными переменными со значениями '1' и '2' соответственно, и они сцепляются с символом '+' в указанном порядке |
| `e`  | 3  | переменной строкового типа 'e' присвоено значение '3', т.к. при данной форме записи (в данном контексте) двойные скобки выступают как оператор bash, который производит арифметические операции с переменными внутри скобок. Так,  в указанном примере, происходит неявное преобразование переменных '$a' и '$b' в целочисленные (integer) и с их значениями производится операция сложения и, затем, значение вычисленного выражения присваевается переменной 'e' |


## Обязательная задача 2
На нашем локальном сервере упал сервис и мы написали скрипт, который постоянно проверяет его доступность, записывая дату проверок до тех пор, пока сервис не станет доступным (после чего скрипт должен завершиться). В скрипте допущена ошибка, из-за которой выполнение не может завершиться, при этом место на Жёстком Диске постоянно уменьшается. Что необходимо сделать, чтобы его исправить:
```bash
while ((1==1)
do
	curl https://localhost:4757
	if (($? != 0))
	then
		date >> curl.log
	fi
done
```

Необходимо написать скрипт, который проверяет доступность трёх IP: `192.168.0.1`, `173.194.222.113`, `87.250.250.242` по `80` порту и записывает результат в файл `log`. Проверять доступность необходимо пять раз для каждого узла.

### Ваш скрипт:  

```bash
#!/usr/bin/env bash
#Location: /root/test.sh
#Version: v0.19 (2021-12-13)
#Author: OleKirs (ok.****t@ya.ru)
#Description: 
#  Проверяет по IP и порту с помощью CURL доступность узлов в сети несколько раз для каждого узла
#  и записывает неудачные попытки в лог-файл.

###########################################
#              Variables                  #
###########################################
logdir='/var/log/testcurl'                                    # set directory for logfile placement
logfile=$logdir'/curl.log'                                    # set logfile full name
array_ip=( '192.168.0.1' '173.194.222.113' '87.250.250.242' ) # set ip addresses for testing
port=80                                                       # TCP port for test
protocol='http'                                               # protocol for CURL testing
testdelay=1                                                   # Delay between test retry
trycount=5                                                    # Number reply of test CURL request
dtformat='%Y/%m/%d %H:%M:%S:'                                 # date format fot timestamp


###########################################
#              Functions                  #
###########################################
testcurl()
  {

	curl -I $1://$2:$3 &> /dev/null                     # get page from $1 address port $2 by protocol $3
	if (($? != 0))                                      # If exit code not equal zero?
	then
	  return 53                                         # exit from func with error code 53
	fi
  }

###########################################
# Check and create log directory and file #
###########################################

if [ ! -d $logdir ]                                                    # If no $logdir
then 
  mkdir $logdir                                                        # create $logdir
  if [ $? -ne 0 ]; then echo "Can\`t create logdir" >&2; exit 50; fi   # Check exit code from "mkdir"
fi


if [ -e $logfile ]                                                            # If $logfile exist?
  then
    logfiles=($(ls $logfile*))                                                     # Get filenames like $logfile in log directory
    tar -czvf $logfile.$(( ${#logfiles[@]} + 1 )).tar.gz curl.log >/dev/null       # Archive old logs into next "tar.gz" arch
    if [ $? -ne 0 ]; then echo "Can\`t create arch from logfile" >&2; exit 51; fi  # Check exit code from "tar", if exit code <> 0, then exit with error code 51
    echo "$(date +"$dtformat") - Test start in $(pwd)" > $logfile                  # Clear & send message to logfile
    echo "Old log file is $logfile.$(( ${#logfiles[@]})).tar.gz" >> $logfile       # Write name created arch in logfile
  else
    touch $logfile > /dev/null   # Create empty logfile
    if [ $? -eq 0 ]              # If exit code equal zero?
      then
        echo "$(date +"$dtformat") - Log file created: $logfile" > $logfile        # Clear & send message to logfile
        echo "$(date +"$dtformat") - Test start in $(pwd)" >> $logfile             # Send another message to logfile
      else
        echo "Can\`t create log file ($logfile)." >&2                              # Write message to stderr
        exit 52	                                                                   # Exit with error code 52
    fi
fi


###########################################
#        Test ip addresses by curl        #
###########################################

while ((1==1))
  do
    for ip in ${array_ip[@]}                                         # for every ip address in $array_ip
      do
	for ((i=1; i <= $trycount ; i++))
	  do
            #echo "$ip, try num = $i"                                # diagnostic operator, remove '#' to debag

            sleep $testdelay                                         # delay between test CURL exec
	  
            testcurl $protocol $ip $port                             # Exec func `testcurl`
	  
            if [ $? -eq 53 ]                                         # If exit code from func equal 53
              then
                echo "$(date +"$dtformat") - Can\`t get pages from $ip" >> $logfile  # write log message with $ip to log-file
                break                                                # break this cycle
            fi
          done
      done
  done

exit 0
 
# EOF  
```

Проверка:

Запустим скрипт несколько раз

```bash
root@netology1:~# ./test.sh &
[1] 27225
root@netology1:~# fg
./test.sh
^C
root@netology1:~# ./test.sh &
[1] 27266
root@netology1:~# kill 27266
root@netology1:~# fg
-bash: fg: job has terminated
[1]+  Terminated              ./test.sh
root@netology1:~# ./test.sh &
[1] 27330
root@netology1:~# kill -9 27330
root@netology1:~# fg
-bash: fg: job has terminated
[1]+  Killed                  ./test.sh
root@netology1:~# ./test.sh &
[1] 27389
root@netology1:~# fg
./test.sh
^C
```

Проверим записи в лог-файле и ротацию логов при перезапуске скриптов.

```bash
root@netology1:~# cat /var/log/testcurl/curl.log
2021/12/13 20:06:30: - Test start in /root
Old log file is /var/log/testcurl/curl.log.3.tar.gz
2021/12/13 20:06:32: - Can`t get pages from 192.168.0.1
2021/12/13 20:06:46: - Can`t get pages from 192.168.0.1
root@netology1:~# ls -la /var/log/testcurl/
total 24
drwxr-xr-x 2 root root   4096 Dec 13 20:06 .
drwxrwxr-x 8 root syslog 4096 Dec 13 20:03 ..
-rw-r--r-- 1 root root    207 Dec 13 20:06 curl.log
-rw-r--r-- 1 root root    227 Dec 13 20:04 curl.log.2.tar.gz
-rw-r--r-- 1 root root    227 Dec 13 20:05 curl.log.3.tar.gz
-rw-r--r-- 1 root root    227 Dec 13 20:06 curl.log.4.tar.gz

```

## Обязательная задача 3
Необходимо дописать скрипт из предыдущего задания так, чтобы он выполнялся до тех пор, пока один из узлов не окажется недоступным. Если любой из узлов недоступен - IP этого узла пишется в файл error, скрипт прерывается.

### Ваш скрипт:

* Установим и настроим на локальном узле тестовый web-сервер Apache2. 
* Изменим целевые узлы с `array_ip=( '192.168.0.1' '173.194.222.113' '87.250.250.242' )` на `array_ip=( '127.0.0.1' '173.194.222.113' '87.250.250.242' )`  

* Изменим строки в условии проверки exit code функции `testcurl`:  

```bash
# Test ip addresses by curl
while ((1==1))
  do
    for ip in ${array_ip[@]}  # for every ip address in $array_ip
      do
	for ((i=1; i <= $trycount ; i++))
	  do
            #echo "$ip, try num = $i"                                # diagnostic operator, remove '#' to debag

            sleep $testdelay                                         # delay between test CURL exec
	  
            testcurl $protocol $ip $port                             # Exec func `testcurl`
	  
            if [ $? -eq 53 ]                                         # If exit code from func equal 53
```

***Было***

```bash
              then
                echo "$(date +"$dtformat") - Can\`t get pages from $ip" >> $logfile  # write log message with $ip to log-file
                break                                                                # exit from cycle
            fi
```  

***Изменено на***  
**(закомментирован `break`, добавлены зыапись в канал `stderr` и выход с кодом ошибки `53`)**  

```bash
              then
                echo "$(date +"$dtformat") - Can\`t get pages from $ip" >> $logfile  # write log message with $ip to log-file
                #break                                                               # exit from cycle
                echo "Can\`t get pages from $ip" >&2                                 # write message in stderr
                exit 53                                                              # End script with error code 53
            fi
``` 

***И закроем циклы:***  

```bash
          done
      done
  done
```

**Проверка:**  

Запустим скрипт в фоновой задаче:
```bash
root@netology1:~# ./test.sh &
[1] 27475
```

Остановим локальный Apache, выведем скрипт из фоновой работы и дождёмся остановки скрипта с сообщением `Can`t get pages from 127.0.0.1`:

```bash
root@netology1:~# systemctl stop apache2
root@netology1:~# fg
./test.sh
Can`t get pages from 127.0.0.1
```

Проверим записи в лог-файле и увидим диагностическое сообщение о недоступности сервиса на узле 127.0.0.1:

```bash
root@netology1:~# cat /var/log/testcurl/curl.log
2021/12/13 20:21:48: - Test start in /root
Old log file is /var/log/testcurl/curl.log.5.tar.gz
2021/12/13 20:22:23: - Can`t get pages from 127.0.0.1
```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Мы хотим, чтобы у нас были красивые сообщения для коммитов в репозиторий. Для этого нужно написать локальный хук для git, который будет проверять, что сообщение в коммите содержит код текущего задания в квадратных скобках и количество символов в сообщении не превышает 30. Пример сообщения: \[04-script-01-bash\] сломал хук.

### Ваш скрипт:
```bash
???
```
