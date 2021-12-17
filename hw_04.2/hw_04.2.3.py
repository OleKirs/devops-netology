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

for result in result_os.split('\n'):   # Для каждой строки в "result_os"  с разделением по "\n"
    if result.find('modified') != -1:  # Если найдено "modified"
        prepare_result = result.replace('\tmodified:   ', str(cwd))   # добавим в начало вывода путь к корню репозитория
        print(prepare_result)          # Выведем полученный результат

sys.exit(0)
# EOF
