# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep

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

    def __init__(self, name: str, srv_address):  # Свойства класса
        self.__name = name
        self.__srv_address = srv_address

    def change_ip(self):  # Метод для проверки изменения IP-адреса объекта

        from socket import gethostbyname

        ip = gethostbyname(self.__name)

        if ip != self.__srv_address:
            return [True, ip]
        else:
            return [False, ip]


# Functions

def print_head(services_name_n_ip: dict):
    """ Печать заголовка в начале работы скрипта """

    print('\n*******************************\nStart host settings:\n')
    print(str(services_name_n_ip).replace('{', '').replace('}', '').replace(', ', '\n'))
    print('\n*******************************\nBegin host ip-address testing:\n')


def print_error(srv_host: str, host_old_ip, host_new_ip, time_zone_offset: float):
    """
    Выводит в stdout сообщение об ошибке
    :param srv_host: Имя сервиса
    :param host_old_ip: Старое значение IP
    :param host_new_ip: Новое значение IP
    :param time_zone_offset: Смещение локального времени от UTC
    """

    from datetime import datetime, timezone, timedelta

    time_zone_info = timezone(timedelta(hours=time_zone_offset))  # Записать в `time_zone_info` инф-ю о временной зоне.

    print(str(datetime.now(time_zone_info).strftime("%Y-%m-%d %H:%M:%S")) + ' [ERROR] ' + str(srv_host)
          + ' IP mismatch: ' + host_old_ip + ' ' + host_new_ip)  # Вывести сообщение об "ошибке" в `stdout`


def check_services_working_dir(checking_dir: str):
    """
    Процедура проверки и создания рабочего каталога.
    :param checking_dir: Путь к проверяемому каталогу.
    """

    from pathlib import Path

    try:
        p = Path(checking_dir)
        if not p.exists():
            p.mkdir()
    except FileExistsError as fe:  # Если каталог уже есть, то записать и продолжить работу.
        print(f'Warning: Directory already exist  {checking_dir}', {fe})

    except OSError as oe:  # Если другие ошибки доступа -> EXIT (51).
        print(f'Error: Creating directory. {checking_dir}', {oe})
        exit(51)


def export_to_json(working_dir: str, conf_file_prefix: str, service: str, service_ip):
    """
    Процедура выгрузки (сериализации) словарей в JSON
    :param working_dir: Путь к рабочему каталогу
    :param conf_file_prefix: Префикс имени файла конфига для всех "сервисов"
    :param service: Имя сервиса
    :param service_ip: IP-адрес сервиса
    """

    import json

    # Полный путь до конф-файла JSON для всех "сервисов"
    json_conf_filename = working_dir + conf_file_prefix + '.json'

    try:
        file = open(json_conf_filename, "w")
    except IOError as e:
        print([u'не удалось открыть файл JSON', json_conf_filename], {e})  # Файл есть, но нет доступа. -> EXIT (52)
        exit(52)
    else:
        with file:
            data = {service: service_ip}  # создадим запись словаря с ключом `service` и значением `service_ip`
            with open(working_dir + service + ".json",
                      "w") as write_file:  # Откроем на запись файл с именем сервиса
                json.dump(data, write_file)  # Сериализуем (выгрузим в формате JSON) в него переменную `data`
            data2 = checking_services  # Скопируем содержимое `checking_services` в `data2`
            with open(json_conf_filename, "w") as write_file:  # Откроем на запись файл для всех "сервисов"
                json.dump(data2, write_file)  # Сериализуем (выгрузим в формате JSON) в него переменную `data2`


def export_to_yaml(working_dir: str, conf_file_prefix: str, service: str, service_ip):
    """
    Процедура выгрузки (сериализации) словарей в YAML
    :param working_dir: Путь к рабочему каталогу
    :param conf_file_prefix: Префикс имени файла конфига для всех "сервисов"
    :param service: Имя сервиса
    :param service_ip: IP-адрес сервиса
    """

    import yaml

    # Полный путь до конф-файла YAML для всех "сервисов"
    yaml_conf_filename = working_dir + conf_file_prefix + '.yml'

    try:
        file = open(yaml_conf_filename, "w")  # Проверим доступ к файлу попыткой открыть файл на запись.
    except IOError as e:
        print([u'не удалось открыть файл YAML', yaml_conf_filename], {e})  # Файл есть, но нет доступа -> EXIT (52)
        exit(52)
    else:
        with file:

            data = [{service: service_ip}]  # создадим запись словаря с ключом `service` и значением `service_ip`
            with open(working_dir + service + ".yml",
                      "w") as write_file:  # Откроем на запись файл с именем сервиса
                yaml.dump(data, write_file)  # Сериализуем (выгрузим в формате YAML) в него переменную `data`

            data2 = checking_services  # Скопируем содержимое `checking_services` в `data2`
            with open(yaml_conf_filename, "w") as write_file:  # Откроем на запись файл для всех "сервисов"
                yaml.dump(data2, write_file,
                          explicit_start=True,
                          sort_keys=True,
                          default_flow_style=False)  # Сериализуем (выгрузим в формате YAML) в него переменную `data2`


# Main

# Выведем заголовок и начальные значения для сервисов:
print_head(checking_services)

# Запустим проверку:
try:

    check_services_working_dir(
        services_working_dir)  # Проверим наличие рабочего каталога. заданного переменной `services_working_dir`

    while True:

        for host in checking_services:  # Для каждого host из словаря `checking_services`

            tested_serv = TestedService(host, checking_services[
                host])  # Создадим объект `TestedService` с именем и ip из словаря `checking_services`
            ip_change = tested_serv.change_ip()[
                0]  # Методом tested_serv.change_ip() определим, изменился ли IP-адрес и запишем рез-т в "ip_change"
            srv_ip = tested_serv.change_ip()[1]  # Полученный адрес сохраним в "srv_ip"

            # если адрес менялся (ip_change = True)
            if ip_change:
                print_error(host, checking_services[host], srv_ip, tz_offset)  # Выведем сообщение в `stdout`
                checking_services[host] = srv_ip  # Запишем новое значение в словарь `checking_services` по ключу `host`
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
