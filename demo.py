#!/usr/bin/env python
# Note, works with both python 2.7 and 3

import random
import socket
import ssl
import string
import time

from metasploit import module

metadata = {
    'name': 'metasploit python module demo',
    # module descript
    'description': '''
    hello world
    ''',
    # module authors
    'authors': [
        'bluebird'
    ],
    # module write time
    'date': '2018-02-02',
    # bug reference
    'references': [
     ],
    # bug type
    'type': 'dos',
    'options': {
        'rhost': {'type': 'address', 'description': 'The target address', 'required': True, 'default': None},
        'rport': {'type': 'port', 'description': 'The target port', 'required': True, 'default': 80},
     }}


def run(args):
    module.log('hello world')


if __name__ == "__main__":
    module.run(metadata, run)
