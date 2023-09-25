# Описание
Скрипт позволяет использовать базу Zabbix в качестве динамического inventory для системы управления конфигурациями Ansible.

# Требования
1. Python version > 3.7 <pre>python --version</pre>
2. Установленный модуль pyzabbix <pre>pip install pyzabbix</pre>

# Установка
1. Скопировать файлы dynamic.py и config.py в рабочий каталог Ansible
2. Опеределить в файле ansible.cfg параметр INVENTORY
<pre>
[defaults]
INVENTORY = dynamic.py
....
</pre>
3. Определить переменные в файле config.py
```python
# Пользователь по умолчанию под которым происходит подключение к удаленным хостам
DEFAULT_ANSIBLE_USER = "ansible" 
# Префикс группы
# Eсли определено то имя группы в Ansible будет GROUP_PREFIX+<Имя группы Zabbix>
GROUP_PREFIX = "GR_"
# Постфикс группы
# Eсли определено то имя группы в Ansible будет <Имя группы Zabbix>+GROUP_POSTFIX
GROUP_POSTFIX = ""
# Группа по умолчанию
GROUP_DEFAULT_NAME = "ungrouped"
# Адрес Zabbix-сервера
ZABBIX_SERVER = "http://zabbix.my.host"
# API-токен для подключения к Zabbix-серверу
ZABBIX_API_TOKEN = "Insert you token here"
```
4. Проверить работу
<pre>
ansible-inventory --graph
или 
ansible-inventory --list

ansible-inventory --host <Имя узла в заббиксе>
</pre>