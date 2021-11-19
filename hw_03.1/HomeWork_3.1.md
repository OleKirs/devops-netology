# Домашнее задание к занятию "3.1. Работа в терминале, лекция 1"

## 1. Установите средство виртуализации [Oracle VirtualBox](https://www.virtualbox.org/).
 *Установил*
## 2. Установите средство автоматизации [Hashicorp Vagrant](https://www.vagrantup.com/).
 *Установил*
 
![Установлено VirtualBox + Vagrant](https://github.com/OleKirs/devops-netology/raw/main/hw_03.1/1.png "Установлено VirtualBox + Vagrant")
## 3. В вашем основном окружении подготовьте удобный для дальнейшей работы терминал. Можно предложить:
 *Установлено -* ***Putty.exe***

![Установлено - Putty](https://github.com/OleKirs/devops-netology/raw/main/hw_03.1/2.png "Установлено - Putty")

## 4. С помощью базового файла конфигурации запустите Ubuntu 20.04 в VirtualBox посредством Vagrant:
 *Выполнено*
```powershell
PS C:\Users\Administrator> cd C:\HashiCorp\Vagrant\etc\
PS C:\HashiCorp\Vagrant\etc> vagrant init
A `Vagrantfile` has been placed in this directory. You are now
ready to `vagrant up` your first virtual environment! Please read
the comments in the Vagrantfile as well as documentation on
`vagrantup.com` for more information on using Vagrant.
PS C:\HashiCorp\Vagrant\etc> move .\Vagrantfile .\Vagrantfile.OLD
PS C:\HashiCorp\Vagrant\etc> notepad .\Vagrantfile
PS C:\HashiCorp\Vagrant\etc> vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Box 'bento/ubuntu-20.04' could not be found. Attempting to find and install...
    default: Box Provider: virtualbox
    default: Box Version: >= 0
==> default: Loading metadata for box 'bento/ubuntu-20.04'
    default: URL: https://vagrantcloud.com/bento/ubuntu-20.04
==> default: Adding box 'bento/ubuntu-20.04' (v202107.28.0) for provider: virtualbox
    default: Downloading: https://vagrantcloud.com/bento/boxes/ubuntu-20.04/versions/202107.28.0/providers/virtualbox.box
    default:
==> default: Successfully added box 'bento/ubuntu-20.04' (v202107.28.0) for 'virtualbox'!
==> default: Importing base box 'bento/ubuntu-20.04'...
==> default: Matching MAC address for NAT networking...
==> default: Checking if box 'bento/ubuntu-20.04' version '202107.28.0' is up to date...
==> default: Setting the name of the VM: etc_default_1637316535403_80112
Vagrant is currently configured to create VirtualBox synced folders with
the `SharedFoldersEnableSymlinksCreate` option enabled. If the Vagrant
guest is not trusted, you may want to disable this option. For more
information on this option, please refer to the VirtualBox manual:

  https://www.virtualbox.org/manual/ch04.html#sharedfolders

This option can be disabled globally with an environment variable:

  VAGRANT_DISABLE_VBOXSYMLINKCREATE=1

or on a per folder basis within the Vagrantfile:

  config.vm.synced_folder '/host/path', '/guest/path', SharedFoldersEnableSymlinksCreate: false
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
Timed out while waiting for the machine to boot. This means that
Vagrant was unable to communicate with the guest machine within
the configured ("config.vm.boot_timeout" value) time period.

If you look above, you should be able to see the error(s) that
Vagrant had when attempting to connect to the machine. These errors
are usually good hints as to what may be wrong.

If you're using a custom box, make sure that networking is properly
working and you're able to connect to the machine. It is a common
problem that networking isn't setup properly in these boxes.
Verify that authentication configurations are also setup properly,
as well.

If the box appears to be booting properly, you may want to increase
the timeout ("config.vm.boot_timeout") value.
PS C:\HashiCorp\Vagrant\etc>
```
## 5. Ознакомьтесь с графическим интерфейсом VirtualBox, посмотрите как выглядит виртуальная машина, которую создал для вас Vagrant, какие аппаратные ресурсы ей выделены. Какие ресурсы выделены по-умолчанию?
	CPU:2 cpu, RAM:1024mb, Video:4mb, HDD:64gb
![Параметры ВМ по-умолчанию](https://github.com/OleKirs/devops-netology/raw/main/hw_03.1/2.png "Параметры ВМ по-умолчанию" )


## 6. Ознакомьтесь с возможностями конфигурации VirtualBox через Vagrantfile: [документация](https://www.vagrantup.com/docs/providers/virtualbox/configuration.html). Как добавить оперативной памяти или ресурсов процессора виртуальной машине?
```bash
	   config.vm.provider "virtualbox" do |vb|
		 vb.memory = "1024"
		 vb.cpu = "2"
	   end
```

## 7. Команда `vagrant ssh` из директории, в которой содержится Vagrantfile, позволит вам оказаться внутри виртуальной машины без каких-либо дополнительных настроек. Попрактикуйтесь в выполнении обсуждаемых команд в терминале Ubuntu.
 *Выполнено*

## 8. Ознакомиться с разделами `man bash`, почитать о настройках самого bash:
 **какой переменной можно задать длину журнала `history`, и на какой строчке manual это описывается?**

**(line 596)**
```bash
       HISTFILESIZE
              The maximum number of lines contained in the history file.  When this variable is assigned a value, the history file is truncated, if necessary, to contain no more than that number of lines by removing the  old‐
              est entries.  The history file is also truncated to this size after writing it when a shell exits.  If the value is 0, the history file is truncated to zero size.  Non-numeric values and numeric values less than
              zero inhibit truncation.  The shell sets the default value to the value of HISTSIZE after reading any startup files.
```

```bash
       HISTSIZE
              The  number  of commands to remember in the command history (see HISTORY below).  If the value is 0, commands are not saved in the history list.  Numeric values less than zero result in every command being saved
              on the history list (there is no limit).  The shell sets the default value to 500 after reading any startup files.
```
	
 **что делает директива `ignoreboth` в bash?**
 ***ignoreboth*** -> *"не сохранять команды начинающиеся с пробела и не сохранять, если такая команда уже имеется в истории"*

## 9. В каких сценариях использования применимы скобки `{}` и на какой строчке `man bash` это описано?
 ***{}*** *- зарезервированные слова, список, в т.ч. список команд команд в отличии от "(...)" исполнятся в текущем инстансе, используется в различных условных циклах, условных операторах, или ограничивает тело функции, В командах выполняет подстановку элементов из списка , если упрощенно то  цикличное выполнение команд с подстановкой например mkdir ./DIR_{A..Z} - создаст каталоги сименами DIR_A, DIR_B и т.д. до DIR_Z *
 **(line 343)**

## 10. Основываясь на предыдущем вопросе, как создать однократным вызовом `touch` 100000 файлов? А получилось ли создать 300000? Если нет, то почему?
 *touch {000001..100000}.txt - создаст в текущей директории соответсвющее число фалов*
 *300000 - создать не удасться, это слишком дилинный список аргументов, максимальное число получил экспериментально - 110188*

## 11. В man bash поищите по `/\[\[`. Что делает конструкция `[[ -d /tmp ]]`
 *проверяет условие -d /tmp и возвращает ее статус (0 или 1), наличие директории /tmp*

## 12. Основываясь на знаниях о просмотре текущих (например, PATH) и установке новых переменных; командах, которые мы рассматривали, добейтесь в выводе type -a bash в виртуальной машине наличия первым пунктом в списке:
```bash
vagrant@vagrant:~$ mkdir /tmp/new_path_dir/
vagrant@vagrant:~$ cp /bin/bash /tmp/new_path_dir/
vagrant@vagrant:~$ PATH=/tmp/new_path_dir/:$PATH
vagrant@vagrant:~$ type -a bash

bash is /tmp/new_path_dir/bash
bash is /usr/bin/bash
bash is /bin/bash
```

## 13. Чем отличается планирование команд с помощью `batch` и `at`?
**at** *- команда запускается в указанное время \(в параметре\)*
**batch** *- запускается когда уровень загрузки системы снизится ниже 1.5.*

## 14. Завершите работу виртуальной машины чтобы не расходовать ресурсы компьютера и/или батарею ноутбука.
```PowerShell
PS> vagrant suspend
```
