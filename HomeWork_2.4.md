## Домашнее задание к занятию «2.4. Инструменты Git»

Для выполнения заданий в этом разделе давайте склонируем репозиторий с исходным кодом терраформа https://github.com/hashicorp/terraform

В виде результата напишите текстом ответы на вопросы и каким образом эти ответы были получены.

# 1. Найдите полный хеш и комментарий коммита, хеш которого начинается на aefea.

#Команда: 
olekirs@Deb10-Lab:~/terraform$ git show aefea --pretty=format:'Hash = %H %nComment: %s' -q

#Результат:
Hash = aefead2207ef7e2aa5dc81a34aedf0cad4c32545 
Comment: Update CHANGELOG.md

# 2. Какому тегу соответствует коммит 85024d3?
Тэг v0.12.23

#Команда: 
olekirs@Deb10-Lab:~/terraform$ git show 85024d3 --oneline -q

#Результат:
85024d310 (tag: v0.12.23) v0.12.23

# 3. Сколько родителей у коммита b8d720? Напишите их хеши.
У коммита 2 родителя.
Хэши родителей: 56cd7859e 9ea88f22f

#Команда: 
olekirs@Deb10-Lab:~/terraform$ git show --source b8d720 --pretty=short 

#Результат:
commit b8d720f8340221f2146e4e4870bf2ee0bc48f2d5 b8d720
Merge: 56cd7859e 9ea88f22f
Author: Chris Griggs <cgriggs@hashicorp.com>

    Merge pull request #23916 from hashicorp/cgriggs01-stable

# 4. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24.
#Команда (все хеши начиная, но не включая с v0.12.23 до до родителя коммита v0.12.24): 
olekirs@Deb10-Lab:~/terraform$ git log v0.12.23..v0.12.24^ --pretty=oneline 

#Результат:
b14b74c4939dcab573326f4e3ee2a62e23e12f89 [Website] vmc provider links
3f235065b9347a758efadc92295b540ee0a5e26e Update CHANGELOG.md
6ae64e247b332925b872447e9ce869657281c2bf registry: Fix panic when server is unreachable
5c619ca1baf2e21a155fcdb4c264cc9e24a2a353 website: Remove links to the getting started guide's old location
06275647e2b53d97d4f0a19a0fec11f6d69820b5 Update CHANGELOG.md
d5f9411f5108260320064349b757f55c09bc4b80 command: Fix bug when using terraform login on Windows
4b6d06cc5dcb78af637bbb19c198faff37a066ed Update CHANGELOG.md
dd01a35078f040ca984cdd349f18d0b67e486c35 Update CHANGELOG.md
225466bc3e5f35baa5d07197bbc079345b77525e Cleanup after v0.12.23 release

# 5. Найдите коммит в котором была создана функция func providerSource, ее определение в коде выглядит так func providerSource(...) (вместо троеточего перечислены аргументы).
#Команда: 
olekirs@Deb10-Lab:~/terraform$ git log -S'func providerSource(' --pretty=oneline 

#Результат:
8c928e83589d90a031f811fae52a81be7153e82f main: Consult local directories as potential mirrors of providers

# 6. Найдите все коммиты в которых была изменена функция globalPluginDirs.
# 6.1 Определим файлы содержащие функцию:
#Команда: 
olekirs@Deb10-Lab:~/terraform$ git grep -o --heading --break -e 'func globalPluginDirs'
#Результат:
plugins.go
func globalPluginDirs
# 6.2. Найдем коммиты с изменениями функции (включая первоначальное создание)
#Команда: 
olekirs@Deb10-Lab:~/terraform$ git log -L:'globalPluginDirs':plugins.go --oneline  -q

#Результат:
78b122055 Remove config.go and update things using its aliases
52dbf9483 keep .terraform.d/plugins for discovery
41ab0aef7 Add missing OS_ARCH dir to global plugin paths
66ebff90c move some more plugin search path logic to command
8364383c3 Push plugin discovery down into command package

# 7. Кто автор функции synchronizedWriters?
#Команда: 
olekirs@Deb10-Lab:~/terraform$ git log -S'func synchronizedWriters' --first-parent --pretty=format:'%an "%ae"'

#Результат:
Martin Atkins "mart@degeneration.co.uk"


