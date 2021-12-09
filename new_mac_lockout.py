# -*- coding: utf-8 -*-

import re
import getpass
import netmiko
from mac_transform import mac_transform

login = input('login: ')
password = getpass.getpass()
mac = input('Enter mac-address: ')
mac = mac_transform(mac)

krd_brases = { 
        '1': '178.34.128.4',
        '2': '178.34.128.5',
        '3': '178.34.128.6',
        '9': '178.34.128.21',
        '13': '178.34.128.28',
        '14': '178.34.128.29',
        '15': '178.34.128.30'
             }

def juniper_mac_lockout(host, login, password, mac_address):
    juniper_router = {'device_type': 'juniper', 'host':bras, 'username':login, 'password':password }
    with netmiko.ConnectHandler(**juniper_router) as ssh:
        output = ssh.send_command(f'show pppoe lockout | match {mac_address}')
        mac_addr = re.search(r'\s+(?P<mac>\S+:\S+)', output)
        if mac_addr:
            print(f"KRDR-BRAS{bras_num} {mac_addr.group('mac')}")
            ssh.send_command(f'clear pppoe lockout mac-address {mac_address}')
            print('Мак удален из локаута')
        else:
            print(f'KRDR-BRAS{bras_num} Мак не в локауте!')


def nokia_mac_lockout(host, login, password, mac_address):
    nokia_router = {'device_type': 'nokia_sros', 'host':bras, 'username':login, 'password':password }
    with netmiko.ConnectHandler(**nokia_router) as ssh:
        output = ssh.send_command(f'show subscriber-mgmt host-lockout-policy "rtk" active mac {mac_address}')
        lag_nums = re.findall(r'Currently Active Lockouts for SAP: lag-(?P<lagnum>\d+)', output)
        if lag_nums:
            for lag_num in lag_nums:
                print(f"KRDR-BRAS{bras_num} lag-{lag_num} {mac_address}")
                ssh.send_command(f'clear subscriber-mgmt host-lockout-policy sap lag-{lag_num}:*.* mac {mac_address}')
                print('Мак удален из локаута')
        else:
            print(f'KRDR-BRAS{bras_num} Мак не в локауте!')


for bras_num, bras in krd_brases.items():
    if int(bras_num) < 13:
        juniper_mac_lockout(bras, login, password, mac)
    else:
        nokia_mac_lockout(bras, login, password, mac)
