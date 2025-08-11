"""
Основная функция для обновления прошивки.

"""
# -*- coding: utf-8 -*-

import re
import csv  # модуль для работы с CSV‑файлами
import os  # функции ОС: пути, каталоги
from datetime import datetime  # получение текущего времени
from netmiko import (Netmiko, NetmikoBaseException, NetmikoAuthenticationException)


def send_show_command(device, command):
    try:
        with Netmiko(**device) as ssh:
            #inspect(ssh)
            print(ssh.enable())
            print(command)
            out = ssh.send_command(command)
            ssh.exit_enable_mode()
        return out
    except (NetmikoBaseException, NetmikoAuthenticationException, SSHException) as error:
            #print(error)
            print(dev['host'] + ' device_ip ' + ' not avaliable')
            return str("~ " + command + " ~ " + "UNDONE")

def main():
    headers = ['device_type', 'host', 'username', 'password', 'secret','timeout']
    #match = r'Active-image:[^\n]*\n\s*Version:\s*(\d+\.\d+\.\d+\.\d+)'
    
    with open('dev_list.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, fieldnames=headers)  # задаём ключи вручную
        devices = [row for row in reader]

    for dev in devices:
        #print(dev)
        if dev['device_type'] == 'eltex':
            print(dev["host"])
            ver_out = send_show_command(dev, 'show version')
            #print(ver_out)
            ver_num = (re.search(r'Active-image:[^\n]*\n\s*Version:\s*(\d+\.\d+\.\d+\.\d+)', ver_out)).group(1)
            if(ver_num):
                print(ver_num)

if __name__ == '__main__':
    main()  # точка входа при запуске скрипта напрямую