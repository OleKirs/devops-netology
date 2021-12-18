#!/usr/bin/env python3
import socket
import time
from datetime import datetime, timezone, timedelta

# Variables

# Список серверов:
hosts = {
    'drive.google.com': '8.8.8.8',
    'mail.google.com': '8.8.8.8',
    'google.com': '8.8.8.8'
}

# Задержка между проверками
test_delay = 5
timezone_offset = 3.0  # MSK Time (UTC+03:00)

# Переменные для отладки
#debug_key = True
#test_count = 15
#i = 0


# Main block
try:
    tzinfo = timezone(timedelta(hours=timezone_offset))

    print('\n*******************************\nStart host settings:\n')
    print(str(hosts).replace('{', '').replace('}', '').replace(', ', '\n'))
    print('\n*******************************\nBegin host ip-address testing:\n')

    while 1 == 1:
        for host in hosts:
            ip = socket.gethostbyname(host)
            if ip != hosts[host]:
                print(str(datetime.now(tzinfo).strftime("%Y-%m-%d %H:%M:%S")) + ' [ERROR] ' + str(host)
                      + ' IP mistmatch: ' + hosts[host] + ' ' + ip)
                hosts[host] = ip
        time.sleep(test_delay)

        # Проверка счётчика и инкремент.
        #if debug_key:
        #    i += 1 if i < test_count else [print("All test repeat is done!"), exit(51)]

except KeyboardInterrupt:
  print(" Keyboard Interrupt by \'Ctrl-C\'")
  exit(50)

exit(0)
# EOF
