# -*- coding: utf-8 -*-
#mac = input('Введите мак адрес: ')



def mac_convert(mac, separator):
    addr = ''.join(mac.strip().split(separator))
    if len(addr) != 12:
        return print("Мак адрес не корректной длины")
    else:
        mac_addr = f'{addr[0:2]}:{addr[2:4]}:{addr[4:6]}:{addr[6:8]}:{addr[8:10]}:{addr[10:12]}'
        return mac_addr
def mac_transform(mac):
    dot = '.'
    dash = '-'
    if dot in mac:
        return mac_convert(mac, dot)
    elif dash in mac:
        return mac_convert(mac, dash)
    else:
        return mac.strip()

if __name__ == '__main__':
    print(mac_transform(mac))
