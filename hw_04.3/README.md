### Как сдавать задания

Вы уже изучили блок «Системы управления версиями», и начиная с этого занятия все ваши работы будут приниматься ссылками на .md-файлы, размещённые в вашем публичном репозитории.

Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-03-yaml/README.md). Заполните недостающие части документа решением задач (заменяйте `???`, ОСТАЛЬНОЕ В ШАБЛОНЕ НЕ ТРОГАЙТЕ чтобы не сломать форматирование текста, подсветку синтаксиса и прочее, иначе можно отправиться на доработку) и отправляйте на проверку. Вместо логов можно вставить скриншоты по желани.

# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"


## Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
```
  Нужно найти и исправить все ошибки, которые допускает наш сервис:

**Исправлено:**  
- Проставлена запятая между первым и вторым элементом в "elements"  
- Добавлены закрывающие двойные кавычки в поле `"ip` во втором элементе в "elements"
- Поставлены кавычки для значений в поле `"ip"` в "elements" для интерпретации ip-адреса в качестве строки
  
**Не исправлено:**  
- Неверное значение `"ip"` в первом элементе в "elements". Не исправлено, т.к. из условия значение IP не ясны (`7175` - это не валидный ip-адрес ни в IPv4, ни в IPv6 нотации).  

```json
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : "7175" 
            },
            { "name" : "second",
            "type" : "proxy",
            "ip" : "71.78.22.43"
            }
        ]
    }
```

## Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Variables
# Список серверов:

checking_services = {
    'drive.google.com': 'NoIP',
    'mail.google.com': 'NoIP',
    'google.com': 'NoIP'
}

test_delay = 5  # Задержка между проверками
tz_offset = 3.0  # MSK Time (UTC+03:00)

# Префикс названия файлов конфигурации сервисов:
services_working_dir = "/home/vagrant/checking_services/"
services_conf_file_prefix = "checked_services"


# Classes

class TestedService:
    """ Проверяемый сервис """

    def __init__(self, name: str, srvaddr):
        self.__name = name
        self.__srvaddress = srvaddr

    def changeip(self):

        from socket import gethostbyname

        ip = gethostbyname(self.__name)

        if ip != self.__srvaddress:
            return [True, ip]
        else:
            return [False, ip]


# Functions

def print_head(services_name_n_ip: dict):
    print('\n*******************************\nStart host settings:\n')
    print(str(services_name_n_ip).replace('{', '').replace('}', '').replace(', ', '\n'))
    print('\n*******************************\nBegin host ip-address testing:\n')


def print_error(host: str, host_old_ip, host_new_ip, tz_offset: float):
    """
    Выводит в stdout сообщение об ошибке
    :param host: Имя сервиса
    :param host_old_ip: Старое значение IP
    :param host_new_ip: Новое значение IP
    :param tz_offset: Смещение локального времени от UTC
    """

    from datetime import datetime, timezone, timedelta

    tzinfo = timezone(timedelta(hours=tz_offset))

    print(str(datetime.now(tzinfo).strftime("%Y-%m-%d %H:%M:%S")) + ' [ERROR] ' + str(host)
          + ' IP mistmatch: ' + host_old_ip + ' ' + host_new_ip)


def check_services_working_dir(services_working_dir: str):
    from pathlib import Path

    p = Path(services_working_dir)
    print('path=', p)

    try:
        if not p.exists():
            p.mkdir()
    except FileExistsError as fe:
        print(f'Warning: Directory already exist  {services_working_dir}', {fe})

    except OSError as oe:
        print(f'Error: Creating directory. {services_working_dir}', {oe})
        exit(51)


def export_to_json(services_working_dir: str, services_conf_file_prefix: str, service: str, serviceip):
    from pathlib import Path
    import json

    try:
        json_conf_filename = services_working_dir + services_conf_file_prefix + '.json'
        file = open(json_conf_filename, "w")
    except IOError as e:
        print([u'не удалось открыть файл JSON', json_conf_filename])
    else:
        with file:
            data = {service: serviceip}
            with open(services_working_dir + service + ".json", "w") as write_file:
                json.dump(data, write_file)
            data2 = checking_services
            with open(json_conf_filename, "w") as write_file:
                json.dump(data2, write_file)


def export_to_yaml(services_working_dir: str, services_conf_file_prefix: str, service: str, serviceip):
    from pathlib import Path
    import yaml

    try:
        yaml_conf_filename = services_working_dir + services_conf_file_prefix + '.yml'
        file = open(yaml_conf_filename, "w")
    except IOError as e:
        print([u'не удалось открыть файл YAML', yaml_conf_filename])
    else:
        with file:

            class NoAliasDumper(yaml.Dumper):
                def ignore_aliases(self, data):
                    return True

            data = [{service: serviceip}]
            with open(services_working_dir + service + ".yml", "w") as write_file:
                yaml.dump(data, write_file)

            data2 = (checking_services)
            with open(yaml_conf_filename, "w") as write_file:
                yaml.dump(data2, write_file, explicit_start=True, sort_keys=True, default_flow_style=False)


# Main

from time import sleep

# Выведем заголовок и начальные значения для сервисов:
print_head(checking_services)

# Запустим проверку:
try:

    check_services_working_dir(services_working_dir)

    while True:

        for host in checking_services:

            tested_serv = TestedService(host, checking_services[host])
            ipchange = tested_serv.changeip()[0]
            newip = tested_serv.changeip()[1]

            if ipchange:
                print_error(host, checking_services[host], newip, tz_offset)
                checking_services[host] = newip
                export_to_json(services_working_dir, services_conf_file_prefix, host, checking_services[host])
                export_to_yaml(services_working_dir, services_conf_file_prefix, host, checking_services[host])

        sleep(test_delay)

except KeyboardInterrupt:
    print(" Keyboard Interrupt by \'Ctrl-C\'")
    exit(50)

exit(0)
# EOF

```

### Вывод скрипта при запуске при тестировании:
```shell
vagrant@netology1:~$ cat ./checking_services/checked_services.yml
---
drive.google.com: 173.194.220.194
google.com: 209.85.233.102
mail.google.com: 74.125.131.18
vagrant@netology1:~$
vagrant@netology1:~$
vagrant@netology1:~$ python3 ./test2.py

*******************************
Start host settings:

'drive.google.com': 'NoIP'
'mail.google.com': 'NoIP'
'google.com': 'NoIP'

*******************************
Begin host ip-address testing:

path= /home/vagrant/checking_services
2021-12-20 20:50:35 [ERROR] drive.google.com IP mistmatch: NoIP 173.194.220.194
2021-12-20 20:50:35 [ERROR] mail.google.com IP mistmatch: NoIP 74.125.131.19
2021-12-20 20:50:35 [ERROR] google.com IP mistmatch: NoIP 209.85.233.138
2021-12-20 20:51:15 [ERROR] mail.google.com IP mistmatch: 74.125.131.19 74.125.131.17
2021-12-20 20:51:26 [ERROR] mail.google.com IP mistmatch: 74.125.131.17 74.125.131.18
^C Keyboard Interrupt by 'Ctrl-C'
vagrant@netology1:~$

```

### json-файл(ы), который(е) записал ваш скрипт:

`checked_services.json`
```json
{"drive.google.com": "173.194.220.194", "mail.google.com": "74.125.131.18", "google.com": "209.85.233.138"}

```
`mail.google.com.json`
```json
{"mail.google.com": "74.125.131.18"}
```
`google.com.json`
```json
{"google.com": "209.85.233.138"}
```
`drive.google.com.json`
```json
{"drive.google.com": "173.194.220.194"}
```

### yml-файл(ы), который(е) записал ваш скрипт:

`google.com.yml`
```yaml
- google.com: 209.85.233.138
```

`drive.google.com.yml`

```yaml
- drive.google.com: 173.194.220.194
```

`mail.google.com.yml`
```yaml
- mail.google.com: 74.125.131.18
```

`checked_services.yml`
```yaml
---
drive.google.com: 173.194.220.194
google.com: 209.85.233.138
mail.google.com: 74.125.131.18
```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

### Ваш скрипт:
```python
???
```

### Пример работы скрипта:
???
