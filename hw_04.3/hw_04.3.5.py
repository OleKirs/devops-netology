# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Variables
# Список сервисов:

checking_services = {
    'drive.google.com': 'NoIP',
    'mail.google.com': 'NoIP',
    'google.com': 'NoIP'
}

test_delay = 5  # Задержка между проверками
tz_offset = 3.0  # Временная зона (MSK Time (UTC+03:00))

# Префиксы названий файлов конфигурации сервисов:
services_working_dir = "/home/vagrant/checking_services/"
services_conf_file_prefix = "checked_services"


# Classes

class TestedService:
    """ Проверяемый сервис """

    def __init__(self, name: str, srvaddr):  # Свойства класса
        self.__name = name
        self.__srvaddress = srvaddr

    def changeip(self):  # Метод для проверки изменеия IP-адреса объекта

        from socket import gethostbyname

        ip = gethostbyname(self.__name)

        if ip != self.__srvaddress:
            return [True, ip]
        else:
            return [False, ip]


# Functions

def print_head(services_name_n_ip: dict):
    """ Печать заголовка в начале работы скрипта """

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

    tzinfo = timezone(timedelta(hours=tz_offset))  # Записать в `tzinfo` информацию о временной зоне.

    print(str(datetime.now(tzinfo).strftime("%Y-%m-%d %H:%M:%S")) + ' [ERROR] ' + str(host)
          + ' IP mistmatch: ' + host_old_ip + ' ' + host_new_ip)  # Вывести сообщение об "ошибке" в `stdout`


def check_services_working_dir(services_working_dir: str):
    """
    Процедура проверки и создания рабочего каталога
    :param services_working_dir: Путь к рабочему каталогу.
    """

    from pathlib import Path

    try:
        p = Path(services_working_dir)
        if not p.exists():
            p.mkdir()
    except FileExistsError as fe:  # Если каталог уже есть, то записать и продолжить работу.
        print(f'Warning: Directory already exist  {services_working_dir}', {fe})

    except OSError as oe:  # Если другие ошибки доступа -> EXIT (51).
        print(f'Error: Creating directory. {services_working_dir}', {oe})
        exit(51)


def export_to_json(services_working_dir: str, services_conf_file_prefix: str, service: str, serviceip):
    """
    Процедура выгрузки (десериализации) словарей в JSON
    :param services_working_dir: Путь к раабочему каталогу
    :param services_conf_file_prefix: Префикс имени файла конфига для всех "сервисов"
    :param service: Имя сервиса
    :param serviceip: IP-адрес сервиса
    """

    import json

    try:
        json_conf_filename = services_working_dir + services_conf_file_prefix + '.json'
        file = open(json_conf_filename, "w")
    except IOError as e:
        print([u'не удалось открыть файл JSON', json_conf_filename], {e})  # Файл есть, но нет доступа. -> EXIT (52)
        exit(52)
    else:
        with file:
            data = {service: serviceip}  # создадим запись словаря с ключом `service` и значением `serviceip`
            with open(services_working_dir + service + ".json",
                      "w") as write_file:  # Откроем на запиь файл с именем сервиса
                json.dump(data, write_file)  # Десериализуем (выгрузим в формате JSON) в него переменную `data`
            data2 = checking_services  # Скопируем содержимое `checking_services` в `data2`
            with open(json_conf_filename, "w") as write_file:  # Откроем на запиь файл для всех "сервисов"
                json.dump(data2, write_file)  # Десериализуем (выгрузим в формате JSON) в него переменную `data2`


def export_to_yaml(services_working_dir: str, services_conf_file_prefix: str, service: str, serviceip):
    """
    Процедура выгрузки (десериализации) словарей в YAML
    :param services_working_dir: Путь к раабочему каталогу
    :param services_conf_file_prefix: Префикс имени файла конфига для всех "сервисов"
    :param service: Имя сервиса
    :param serviceip: IP-адрес сервиса
    """

    import yaml

    try:
        yaml_conf_filename = services_working_dir + services_conf_file_prefix + '.yml'  # Полный путь до конфигурационного файла YAML для всех "сервисов"
        file = open(yaml_conf_filename, "w")  # Проверим доступ к файлу попыткой открыть файл на запись.
    except IOError as e:
        print([u'не удалось открыть файл YAML', yaml_conf_filename], {e})  # Файл есть, но нет доступа -> EXIT (52)
        exit(52)
    else:
        with file:

            data = [{service: serviceip}]  # создадим запись словаря с ключом `service` и значением `serviceip`
            with open(services_working_dir + service + ".yml",
                      "w") as write_file:  # Откроем на запиь файл с именем сервиса
                yaml.dump(data, write_file)  # Десериализуем (выгрузим в формате YAML) в него переменную `data`

            data2 = (checking_services)  # Скопируем содержимое `checking_services` в `data2`
            with open(yaml_conf_filename, "w") as write_file:  # Откроем на запиь файл для всех "сервисов"
                yaml.dump(data2, write_file, explicit_start=True, \
                          sort_keys=True,
                          default_flow_style=False)  # Десериализуем (выгрузим в формате YAML) в него переменную `data2`


# Main

from time import sleep

# Выведем заголовок и начальные значения для сервисов:
print_head(checking_services)

# Запустим проверку:
try:

    check_services_working_dir(
        services_working_dir)  # Проверим наличие рабочего каталога. залданного переменной `services_working_dir`

    while True:

        for host in checking_services:  # Для хаждого host из словаря `checking_services`

            tested_serv = TestedService(host, checking_services[
                host])  # Создадим объект `TestedService` с именем и ip из словаря `checking_services`
            ipchange = tested_serv.changeip()[
                0]  # Методом tested_serv.changeip() определим, изменился ли IP-адрес и запишем рез-т в "ipchange"
            newip = tested_serv.changeip()[1]  # Полученный адрес сохраним в "newip"

            # если адрес менялся (ipchange = True)
            if ipchange:
                print_error(host, checking_services[host], newip, tz_offset)  # Выведем сообщение в `stdout`
                checking_services[host] = newip  # Запишем новое значение в словарь `checking_services` по ключу `host`
                export_to_json(services_working_dir, services_conf_file_prefix, host,
                               checking_services[host])  # Запишем изменения в JSON-файлы
                export_to_yaml(services_working_dir, services_conf_file_prefix, host,
                               checking_services[host])  # Запишем изменения в YAML-файлы

        sleep(test_delay)  # Пауза до следующей проверки на `test_delay` секунд

except KeyboardInterrupt:  # Обработка нажатия `Ctrl-C`
    print(" Keyboard Interrupt by \'Ctrl-C\'")
    exit(50)

exit(0)
# EOF
