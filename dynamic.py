#!./venv/bin/python3
import json
import argparse
from pyzabbix import ZabbixAPI
from config import *


# CREATE OBJECTS
z = ZabbixAPI(ZABBIX_SERVER)
z.login(api_token=ZABBIX_API_TOKEN)
pars = argparse.ArgumentParser()
pars.add_argument("--list", action="store_true", default=False)
pars.add_argument("--host", action="store_true", default=False)
args = pars.parse_args()


# CREATE WORK VARIABLES
hostList: dict = z.host.get(selectHostGroups="extend")
hostInterface: dict = z.hostinterface.get()
hostGroup: dict = z.hostgroup.get()
JSONList = {}

# Формируем JSON-файл с данными из заббикса
for host in hostList:
    try:
        i = next(
            item for item in hostInterface if item["hostid"] == host['hostid'])
        JSONList.update(
            {
                host["name"]: {
                    "metadata": {
                        "ansible_host": i['ip'],
                        "group_list": [g['name'] for g in host['hostgroups']]
                    }
                }
            }
        )
    except:
        next


def get_host_vars(host: str):
    # Определяем значения по умолчанию
    data = {
        "ansible_user": DEFAULT_ANSIBLE_USER,
        "ansible_host": host,
        "group_list": [GROUP_DEFAULT_NAME]
    }
    # Если в JSON файле есть записи отличающиейся от значений по умолчанию меняем их
    if host in JSONList:
        metadata = JSONList[host].get('metadata', {}) or {}
        if metadata.get("group_list"):
            data["group_list"] = metadata["group_list"]
        if 'users' in metadata:
            data['ansible_user'] = metadata['users'][0]
        data.update(metadata)
    return data

# Формируем список согласно требованиям стандарта ANSIBLE


def get_list():
    hostvars = {}
    data = {}
    for host in JSONList:
        hostvars[host] = get_host_vars(host)
        data.update({
            '_meta': {'hostvars': hostvars},
        })
        for group in hostvars[host]["group_list"]:
            groupName = GROUP_PREFIX + group + GROUP_POSTFIX
            if groupName not in data.keys():
                data.update({groupName: {'hosts': []}})
            data[groupName]['hosts'].append(host)

    return json.dumps(data)


# Проверяем с каким ключом запущено приложение.
if args.list:
    print(get_list())
