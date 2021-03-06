# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## Обязательная задача 1

Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```
1. будет ошибка, т.к. типы не соответсвуют для операции , int и str
2. привести a к строке:       c=str(a)+b
3. привести b к целому числу: c=a+int(b)
### Вопросы:
| Вопрос  | Ответ                                                              |
| ------------- |--------------------------------------------------------------------|
| Какое значение будет присвоено переменной `c`?  | ошибка, т.к.  используются разные типы переменных (int и str)      |
| Как получить для переменной `c` значение 12?  | преобразовать тип переменной "a" в строку: `c = str(a) + b`        |
| Как получить для переменной `c` значение 3?  | преобразовать тип переменной "b" в целочисленный: `c = a + int(b)` |

## Обязательная задача 2
Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

### Ваш скрипт:
```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]  # Зададим список команд для получения статуса GIT 
result_os = os.popen(' && '.join(bash_command)).read()  # Выполним команды и запишем результат выполнения в переменную result_os
cwd = os.getcwd()                        # Получим путь к текущему каталогу и поместим его в переменную cwd (current working dir)
# is_change = False                      # Не используемая переменная, можно убрать.
for result in result_os.split('\n'):     # Для каждого элемента с разделителем \n выполним:
    if result.find('modified') != -1:    # Если 'modified' найдено, то:
                                         # Записать в переменную prepare_result результат из result 
                                         # Заменив '\tmodified' на полный путь (из cwd)
        prepare_result = result.replace('\tmodified:   ', cwd) 
        print(prepare_result)            # Вывести значение  prepare_result
#        break # Лишнее, т.к. прерывает обработку на первой итерации

```

### Вывод скрипта при запуске при тестировании:
```bash
vagrant@netology1:~/netology/sysadm-homeworks$ python3 ~/hw_04.2.1.py
/home/vagrant/netology/sysadm-homeworks01-intro-01/README.md
/home/vagrant/netology/sysadm-homeworks02-git-01-vcs/README.md
/home/vagrant/netology/sysadm-homeworksREADME.md

```

## Обязательная задача 3
1. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

### Ваш скрипт:
```python
#!/usr/bin/env python3
import os
import sys
import subprocess

# Если есть аргументы при вызове скрипта:
if len(sys.argv) > 1:

    # Зададим команду "git" для получения "корня" репозитория с использованием аргумента.
    bash_command_1 = "/usr/bin/git -C " + sys.argv[1] + " rev-parse --show-toplevel"

    # Выполним команду в Shell и получим значение "cwd" с удалением переносов строк.
    cwd = (subprocess.Popen(bash_command_1, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)).stdout
    cwd = str(cwd.read().decode('ascii')).replace('\n', '')

    # Проверим присвоенное "cwd" значение:
    if cwd.find('fatal') != -1:  # если в выводе есть ошибка git ('fatal'), то:
        print(cwd)               # выведем текст ошибки
        sys.exit(50)             # прекратим работу с кодом "50"

# Если аргументы при вызове скрипта не указаны - используем текущий каталог для задания "cwd"
else:
    cwd = os.getcwd()

if cwd[-1] != "/":               # если переменная "cwd" заканчивается не на "/"
    cwd = cwd + "/"              # добавим "/" к ней

# Получим сведения об изменённых файлах:
                           # Используя полученное значение "cwd" зададим команду "git" для получения статуса репозитория:
bash_command_2 = "/usr/bin/git -C " + str(cwd) + " status"

result_os = os.popen(bash_command_2).read()  # Выполним команду Shell и получим результат в переменную "result_os"

for result in result_os.split('\n'):         # Для каждой строки в "result_os"  с разделением по "\n"
    if result.find('modified') != -1:        # Если найдено "modified"
        prepare_result = result.replace('\tmodified:   ', str(cwd))   # Добавим в начало вывода путь к корню репозитория
        print(prepare_result)                # Выведем полученный результат

sys.exit(0)
# EOF

```

### Вывод скрипта при запуске при тестировании:
```bash
# Перейдём в домашний каталог пользователя, в котором нет репозиториев и запустим скрипт без аргументов: 
vagrant@netology1:~$ cd 
vagrant@netology1:~$ python3 ~/hw_04.2.3.py
fatal: not a git repository (or any of the parent directories): .git

# Запустим скрипт, указав в аргументе каталог, в который у пользователя нет доступа (/root)
vagrant@netology1:~$ python3 ~/hw_04.2.3.py /root/
fatal: cannot change to '/root/': Permission denied
fatal: cannot change to 'status': No such file or directory

# Запустим скрипт, указав в аргументе корневой каталог репозитория "sysadm-homeworks"
vagrant@netology1:~$ python3 ~/hw_04.2.3.py ~/netology/sysadm-homeworks/
/home/vagrant/netology/sysadm-homeworks/01-intro-01/README.md
/home/vagrant/netology/sysadm-homeworks/02-git-01-vcs/README.md
/home/vagrant/netology/sysadm-homeworks/README.md


# Запустим скрипт, указав в аргументе дочерний каталог в репозитории "sysadm-homeworks"
vagrant@netology1:~$ python3 ~/hw_04.2.3.py ~/netology/sysadm-homeworks/01-intro-01/
/home/vagrant/netology/sysadm-homeworks/01-intro-01/README.md
/home/vagrant/netology/sysadm-homeworks/02-git-01-vcs/README.md
/home/vagrant/netology/sysadm-homeworks/README.md

```

## Обязательная задача 4
1. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:
```python
#!/usr/bin/env python3
import socket
import time
from datetime import datetime, timezone, timedelta

# VARS:
# Список серверов:
hosts = {
    'drive.google.com': '8.8.8.8',
    'mail.google.com': '8.8.8.8',
    'google.com': '8.8.8.8'
    }
# Задержка между проверками (в секундах):
test_delay = 5
# Смещение от UTC для корректного отображения локального времени в Timestamp:
timezone_offset = 3.0  # MSK Time (UTC+03:00)

# MAIN
try:
    tzinfo = timezone(timedelta(hours=timezone_offset))    # Установим TZ
    
    # Вывод стартовой информации и заголовков 
    print('\n*******************************\nStart host settings:\n')
    print(str(hosts).replace('{', '').replace('}', '').replace(', ', '\n'))
    print('\n*******************************\nBegin host ip-address testing:\n')

    while 1 == 1:
        for host in hosts:                         # Для каждого host из hosts
            ip = socket.gethostbyname(host)        # Получить IP-адрес и записать в "ip"

            if ip != hosts[host]:                  # Если "ip" отличается от значения в словаре "hosts"
                                                   # Вывести информацию об ошибке в 'stdout'
                print(str(datetime.now(tzinfo).strftime("%Y-%m-%d %H:%M:%S")) + ' [ERROR] ' + str(host)
                      + ' IP mistmatch: ' + hosts[host] + ' ' + ip)

                hosts[host] = ip                   # Присвоить значение "ip" ключу 'host' в словаре "hosts"

        time.sleep(test_delay)                     # Пауза между проверками на величину "test_delay" сек.
       
except KeyboardInterrupt                           # Обработка нажатия Ctrl-C при работе скрипта.
  print(" Keyboard Interrupt by \'Ctrl-C\'")
  exit(50)

exit(0)
# EOF

```

### Вывод скрипта при запуске при тестировании:
```
vagrant@netology1:~$ python3 ~/hw_04.2.4.py

*******************************
Start host settings:

'drive.google.com': '8.8.8.8'
'mail.google.com': '8.8.8.8'
'google.com': '8.8.8.8'

*******************************
Begin host ip-address testing:

2021-12-18 21:52:42 [ERROR] drive.google.com IP mistmatch: 8.8.8.8 173.194.220.194
2021-12-18 21:52:42 [ERROR] mail.google.com IP mistmatch: 8.8.8.8 142.250.201.69
2021-12-18 21:52:42 [ERROR] google.com IP mistmatch: 8.8.8.8 209.85.233.100
2021-12-18 21:52:47 [ERROR] google.com IP mistmatch: 209.85.233.100 209.85.233.102
2021-12-18 21:55:38 [ERROR] mail.google.com IP mistmatch: 142.250.201.69 74.125.131.19
2021-12-18 21:55:43 [ERROR] mail.google.com IP mistmatch: 74.125.131.19 74.125.131.83
^C Keyboard Interrupt by 'Ctrl-C'
vagrant@netology1:~$

```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так получилось, что мы очень часто вносим правки в конфигурацию своей системы прямо на сервере. Но так как вся наша команда разработки держит файлы конфигурации в github и пользуется gitflow, то нам приходится каждый раз переносить архив с нашими изменениями с сервера на наш локальный компьютер, формировать новую ветку, коммитить в неё изменения, создавать pull request (PR) и только после выполнения Merge мы наконец можем официально подтвердить, что новая конфигурация применена. Мы хотим максимально автоматизировать всю цепочку действий. Для этого нам нужно написать скрипт, который будет в директории с локальным репозиторием обращаться по API к github, создавать PR для вливания текущей выбранной ветки в master с сообщением, которое мы вписываем в первый параметр при обращении к py-файлу (сообщение не может быть пустым). При желании, можно добавить к указанному функционалу создание новой ветки, commit и push в неё изменений конфигурации. С директорией локального репозитория можно делать всё, что угодно. Также, принимаем во внимание, что Merge Conflict у нас отсутствуют и их точно не будет при push, как в свою ветку, так и при слиянии в master. Важно получить конечный результат с созданным PR, в котором применяются наши изменения. 

### Ваш скрипт:
```python
???
```

### Вывод скрипта при запуске при тестировании:
```
???
```
