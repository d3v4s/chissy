#!/bin/env python3

from chissy.core.controller import Controller

import chissy
import sys
import json

name = sys.argv[0]

helpers = """
Usage: {name} start|get-log|version|help|install [option]

Arguments:

    start
        starting a fake ssh server

    get-log
        show the logs create. You can specify the get-log options

    version
        get the version of {name}

    help
        show this helps


get-log options:
    -a --address ADDRESS
        specify the address

    -b --before-date DATE
        get only the logs before the date specified

    -d --after-date DATE
        get only the logs after the date specified

Examples:
    {name} start
    {name} get-log -a 127.0.0.1

"""

helpers = helpers.format(name=sys.argv[0])

if len(sys.argv) < 2:
    print('[!!] Chissy need a argument')
    print(helpers)
    sys.exit(-1)

command = sys.argv[1]

if command == 'help':
    print(helpers)
    sys.exit(0)

with open('conf/server.json') as file:
    conf_server = json.load(file)

with open('conf/log.json') as file:
    conf_log = json.load(file)

ctrl = Controller(command, conf_server, conf_log)
ctrl.execute()
