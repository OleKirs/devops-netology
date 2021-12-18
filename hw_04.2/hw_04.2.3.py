#!/usr/bin/env python3
import os
import sys

if len(sys.argv) > 1:

    cmd1 = "/usr/bin/git -C " + sys.argv[1] + " rev-parse --show-toplevel"

    cwd = (os.popen(cmd1).read()).replace('\n','/')

    if cwd.find('fatal') != -1:
        print(cwd)
        exit(50)

else:
    cwd = os.getcwd()

bash_command = "/usr/bin/git -C " + str(cwd) + " status"
result_os = os.popen(bash_command).read()

for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', str(cwd))
        print(prepare_result)

# EOF
