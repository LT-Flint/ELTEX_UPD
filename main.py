"""
Основная функция для обновления прошивки.

"""
# -*- coding: utf-8 -*-

import time
import re
import csv  # модуль для работы с CSV‑файлами
import os  # функции ОС: пути, каталоги
from datetime import datetime  # получение текущего времени
from netmiko import (Netmiko, NetmikoBaseException, NetmikoAuthenticationException)
from paramiko.ssh_exception import SSHException

def mes_to_version(mes_string):
    _, mid, last = mes_string.split('-')
    return f"{mid[0]}.{mid[1]}.{mid[2]}.{last[0]}"

def convert_mes_to_version(mes_string):
    # Разделяем строку по дефисам
    parts = mes_string.split('-')
    if len(parts) != 3:
        raise ValueError("Некорректный формат строки. Ожидается 'mesXXXX-XXXX-XXX'")

    # Получаем вторую часть (4025) и третью (1R1)
    middle_part = parts[1]  # "4025"
    last_part = parts[2]    # "1R1"

    # Из второй части берем последние 2 цифры (25)
    version_minor = middle_part[-2:]  # "25"

    # Из третьей части берем первую цифру (1)
    version_patch = last_part[0]      # "1"

    # Формируем итоговую версию
    return f"4.0.{version_minor}.{version_patch}"

def send_conf_commands(device, commands, cmd_verify=True):
    try:
        with Netmiko(**device) as ssh:
            ssh.enable()
            out = ssh.send_config_set(commands, cmd_verify=cmd_verify)
            return out
    except (NetmikoBaseException, NetmikoAuthenticationException, SSHException) as error:
            #print(error)
            print(device['host'] + ' device_ip ' + ' not avaliable')

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
            print(device['host'] + ' device_ip ' + ' not avaliable')
            return str("~ " + command + " ~ " + "UNDONE")

def main():
    headers = ['device_type', 'host', 'username', 'password', 'secret','timeout']
    #match = r'Active-image:[^\n]*\n\s*Version:\s*(\d+\.\d+\.\d+\.\d+)'
 
    mes_str = "mes5500-668-2R3"
    version_str = mes_to_version(mes_str) 
 
    with open('dev_list.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, fieldnames=headers)  # задаём ключи вручную
        devices = [row for row in reader]

    for dev in devices:
        #print(dev)
        if dev['device_type'] == 'eltex':
            #print(dev["host"])
            ver_out = send_show_command(dev, 'show version')
            #print(ver_out)
            ver_num = (re.search(r'Active-image:[^\n]*\n\s*Version:\s*(\d+\.\d+\.\d+\.\d+)', ver_out)).group(1)
            if(ver_num):
                if (ver_num == version_str):
                    print("Same version")
                    return None
                else:
                    print(ver_num + " != " + version_str)
                    cmd = "copy tftp://192.168.103.222/" + mes_str + ".ros flash:"
                    #out = send_conf_commands(dev, cmd, cmd_verify=False)
                    send_show_command(dev, cmd)

            time.sleep(300)
            out = send_show_command(dev, "dir")
            if(ver_num and mes_str in out):
                #print(mes_str + "find in dir")
                print(send_show_command(dev, "boot system flash:" + mes_str + ".ros"))


if __name__ == '__main__':
    main()  # точка входа при запуске скрипта напрямую
    
    
    
    