#!/bin/env python3

from shutil import copytree, copy, rmtree

import os
import json

import sys

import chissy


# check if is root user
if os.getuid() != 0:
    print("[!!] WTF!!! Are you drunk???")
    print("[!!] This script need root user")
    exit(-1)

# read arg if it passed
command = ""
if len(sys.argv) > 1:
    command = sys.argv[1]

# path to be insert the bash completions
completions_path = '/usr/share/bash-completion/completions'

# installation paths
install_path = "/opt/chissy/{version}".format(version=chissy.__version__)
service_path = '/usr/lib/systemd/system/chissy.service'
symlink_bin = '/usr/bin/chissy'
symlink_etc = '/etc/chissy'


# path used for logs
logs_path = '/var/log/chissy'

# files to be copied
install_files = [
    'chissy',
    'conf',
    'chissy.sh',
    'chissy.py',
    'install.py'
]

# files to be applied 'chmod +x'
exec_files = [
    'chissy.sh',
    'chissy.py',
    'install.py'
]

helpers = """
Usage: {name} [install|remove]
"""


def show_help():
    print(helpers.format(name=sys.argv[0]))


# function to install chissy
def install():
    print("[*] Install starting...")
    try:
        # copy file on installation path
        os.makedirs(install_path)
        for file in install_files:
            to = '/'.join([install_path, file])
            if os.path.isfile(file):
                copy(file, to)
            else:
                copytree(file, to)

        # add execution permission
        for file in exec_files:
            os.system("chmod +x {path}/{file}".format(path=install_path, file=file))

        # change log directory
        path = '/'.join([install_path, 'conf', 'log.json'])
        log_json_file = open(path, 'r')
        conf_log = json.load(log_json_file)
        log_json_file.close()
        conf_log['path'] = logs_path
        json_out = json.dumps(conf_log, sort_keys=True, indent=4, separators=(',', ': '))
        log_json_file = open(path, 'w')
        log_json_file.write(json_out)
        log_json_file.close()

        # add bash complete
        if os.path.isdir(completions_path):
            file = open('/'.join([completions_path, 'chissy']), 'w')
            file.write("complete -W 'start get-log version help' chissy")
            file.close()

        # create logs dir /var/log/chissy
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)

        print('[*] Files copied')

        # create symbolic link on /usr/bin to chissy
        os.symlink('/'.join([install_path, "chissy.sh"]), symlink_bin)
        # create symlink on /etc/chissy to conf
        os.symlink('/'.join([install_path, 'conf']), symlink_etc)
        print('[*] Symbolic link created')

        # add settings for daemon
        service_file = open('template/systemd/chissy.service', 'r')
        chiss_service = service_file.read()
        service_file.close()
        chiss_service = chiss_service.format(workdir=install_path, version=chissy.__version__)
        file = open(service_path, 'w')
        file.write(chiss_service)
        file.close()
        os.system('systemctl daemon-reload')

        print('[*] Daemon created')
        print('[*] Installation complete')
        print()
        print('[*] Usage: chissy start|get-log|version|help [options]')
        print('[*] Usage daemon: systemctl {start|stop|restart} chissy')
        print()
    except Exception as e:
        print('[!!] Caught a exception while installing. ' + str(e))
        sys.exit(-1)


# function to uninstall chessy
def uninstall():
    print()
    print("[*] Uninstall starting...")
    try:
        # remove service and symlink
        if os.path.exists(service_path):
            os.remove(service_path)
        if os.path.exists(symlink_bin):
            os.remove(symlink_bin)
        if os.path.exists(symlink_etc):
            os.remove(symlink_etc)

        # remove autocomplete
        chissy_compl = '/'.join([completions_path, 'chissy'])
        if os.path.exists(chissy_compl):
            os.remove(chissy_compl)

        print('[*] All installation files have been deleted')

        # remove log files
        while 1:
            resp = input('[?] Remove all log files? (y/N)')
            resp = resp.lower()
            if resp == 'y' or resp == 'ye' or resp == 'yes':
                if os.path.exists(logs_path):
                    rmtree(logs_path)
                    break
            elif resp == "" or resp == "n" or resp == 'no':
                break

        # remove installation path
        rmtree(install_path)
        print("[*] Uninstall complete")
        print()
    except Exception as e:
        print('[!!] Caught a exception while uninstalling. ' + str(e))
        sys.exit(-1)


# function to check if chissy is already installed and install it
def check_install():
    if os.path.isdir(install_path):
        print('[!!] Chissy is already installed')
        while 1:
            resp = input('[?] You want to reinstall it? (y/N): ')
            resp = resp.lower()
            if resp == "y" or resp == "ye" or resp == "yes":
                uninstall()
                break
            elif resp == "" or resp == "n" or resp == "no" or resp == "not":
                sys.exit(0)

    # remove service and symlink
    if os.path.exists(service_path):
        os.remove(service_path)
    if os.path.exists(symlink_bin):
        os.remove(symlink_bin)
    # start install
    install()


# function to check if chissy is already installed
def check_uninstall():
    if os.path.isdir(install_path):
        while 1:
            resp = input('[?] Remove Chissy? (y/N): ')
            resp = resp.lower()
            if resp == "y" or resp == "ye" or resp == "yes":
                uninstall()
                break
            elif resp == "" or resp == "n" or resp == "no" or resp == "not":
                sys.exit(0)
    else:
        print()


# main
if __name__ == '__main__':
    switcher = {
        "": check_install,
        "install": check_install,
        "remove": check_uninstall,
        "help": show_help
    }
    func = switcher.get(command, show_help)
    func()
