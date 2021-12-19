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
