#!/usr/bin/env bash
#Location: /root/test.sh
#Version: v0.20 (2021-12-13)
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
              echo "$(date +"$dtformat") - Can\`t get pages from $ip" >> $logfile  # write log message with $ip to log-file
              #break                                                               # exit from cycle
              echo "Can\`t get pages from $ip" >&2                                 # write message in stderr
              exit 53                                                              # End script with error code 53
            fi
          done
      done
  done

exit 0

# EOF