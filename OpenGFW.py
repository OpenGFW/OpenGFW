#-*- coding: utf8 -*-

import requests
import base64
import traceback
import json
import sys
import wmi
import _winreg


url = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'


def usage():
    print '\033[1;31;40m'
    print \
    '''
OpenGFW.py v1.1 - Generate proxy auto-config pac file.
                - Update pac rules from gfwlist.
                - Thanks gfwlist project. https://github.com/gfwlist/gfwlist

Usage: OpenGFW.py <type> <host> <port> <system>

Windows = 1

Linux = 0

Examples:
    OpenGFW.py PROXY 127.0.0.1 8088 1
    OpenGFW.py SOCKS 127.0.0.1 1080 1
    OpenGFW.py SOCK5 127.0.0.1 1080 1
'''
    print '\033[0m'


def get_data():
    try:
        res = requests.get(url).text
        decode_data = base64.b64decode(res)
        return decode_data
    except BaseException, e:
        print traceback.format_exc()
        return None


def save_data(good_data, save_path):
    f = open(save_path, 'w')
    try:
        f.write(good_data)
        f.close()
    except BaseException, e:
        print traceback.format_exc()
        f.close()


def address_filter(data):
    raw_list = data.split('\n')
    res = []
    for addr in raw_list:
        if 'Whitelist' in addr:
            break
        elif addr.startswith('[') or addr.startswith('!')\
                or addr.startswith('%') or addr.startswith('search')\
                or addr.strip() == '':
            continue
        else:
            _addr = addr.strip('|').strip('.').strip('@').strip('/')
            _addr = _addr.strip('|')
            res.append(_addr)
    return res


def changeIEproxy(keyValue):
    pathInReg = 'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
    pathInRegPac = 'SOFTWARE\Policies\Microsoft\Windows\CurrentVersion\Internet Settings'
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,pathInReg, 0, _winreg.KEY_ALL_ACCESS)
    pac = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,pathInRegPac, 0, _winreg.KEY_ALL_ACCESS)
    _winreg.SetValueEx(key, 'AutoConfigURL', 0, _winreg.REG_SZ, keyValue)
    _winreg.SetValueEx(pac,'EnableLegacyAutoProxyFeatures', 0, _winreg.REG_DWORD, 0x00000001)
    _winreg.CloseKey(key)
    _winreg.CloseKey(pac)


def generate_pac(proxytype, host, port, system, rules):
    pac = '''function isMatchProxy(url, pattern) {
    try {
        return new RegExp(pattern.replace('.', '\\.')).test(url);
    } catch (e) {
        return false;
    }
}

function FindProxyForURL(url, host) {
    var Proxy = '%s %s:%s; DIRECT;';

    var list = %s;


    for(var i=0, l=list.length; i<l; i++) {
        if (isMatchProxy(url, list[i])) {
            return Proxy;
        }
    }
    return 'DIRECT';
}
''' % (proxytype, host, port, rules)
    if system =='1':
        path = sys.path[0]
        pacPath = 'file://' + path +'\OpenGFW.pac'
        changeIEproxy(pacPath)
    return pac


def main():
    data = get_data()
    save_path = 'OpenGFW.pac'
    if data:
        good_data = json.dumps(address_filter(data))
        pac = generate_pac(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], good_data)
        save_data(pac, save_path)
        print 'Created OpenGFW.pac successful !'

if __name__ == '__main__':
    if len(sys.argv) != 5:
        usage()
    else:
        main()
