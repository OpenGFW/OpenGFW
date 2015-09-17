#-*- coding: utf8 -*-

import requests
import base64
import traceback
import json
import sys


url = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'


def usage():
    print '\033[1;31;40m'
    print \
    '''
OpenGFW.py v1.0 - Generate proxy auto-config pac file.
                - Update pac rules from gfwlist.
                - Thanks gfwlist project. https://github.com/gfwlist/gfwlist

Usage: OpenGFW.py <type> <host> <port>

Examples:
    OpenGFW.py PROXY 127.0.0.1 8088
    OpenGFW.py SOCKS 127.0.0.1 1080
    OpenGFW.py SOCK5 127.0.0.1 1080
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
    #print data
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

def generate_pac(proxytype, host, port, rules):
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
    return pac


def main():
    data = get_data()
    save_path = 'OpenGFW.pac'
    if data:
        good_data = json.dumps(address_filter(data))
        pac = generate_pac(sys.argv[1], sys.argv[2], sys.argv[3], good_data)
        save_data(pac, save_path)
        print 'Created OpenGFW.pac successful !'

if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage()
    else:
        main()

