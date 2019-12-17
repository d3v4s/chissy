#!/bin/env python3

from chissy.core.controller import Controller

import chissy
import os
import sys
import json

name = sys.argv[0]

helpers = """
Chissy {version} -- Fake SSH Server
Developed by {author}

Usage: {name} start|get-log|remove-log|version|help|install [option]

Arguments:

    start
        starting a fake ssh server.

    get-log [options]
        show the logs create. You can specify the get-log options.

    remove-log [options]
        remove the logs. You can specify the get-log options.

    version
        get the version of {name}.

    help
        show this helps.


Options:

    get-log:
        -a --address ADDRESS
            specify the IP address
    
        -f --from-date DATE
            get only the logs before the date specified. DATE format yyyy-mm-dd.
    
        -t --to-date DATE
            get only the logs after the date specified. Use the same DATE format to -f.

    remove-log:
        -f --from-date DATE
            get only the logs before the date specified. Use the same DATE format to get-log options.
    
        -t --to-date DATE
            get only the logs after the date specified. Use the same DATE format to get-log options.

Examples:
    {name} start
    {name} get-log -a 127.0.0.1

"""

helpers = helpers.format(name=sys.argv[0], version=chissy.__version__, author=chissy.__author__)


def show_help():
    print(helpers)
    sys.exit(0)


def show_version():
    print('Chessy {version} - Fake SSH server - Developed by {author}'.
          format(version=chissy.__version__, author=chissy.__author__))
    sys.exit(0)


def install():
    os.system('./install.py')
    return


def exec_controller():
    with open('conf/server.json') as file:
        conf_server = json.load(file)

    with open('conf/log.json') as file:
        conf_log = json.load(file)

    ctrl = Controller(command, conf_server, conf_log)
    ctrl.execute()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[!!] Chissy need a argument')
        print(helpers)
        sys.exit(-1)

    command = sys.argv[1]

    # switcher to show help or version and install chissy
    # to default execute controller
    switcher = {
        'help': show_help,
        'version': show_version,
        'install': install
    }
    exc = switcher.get(command, exec_controller)
    exc()
