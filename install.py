#!/bin/env python3

from shutil import copytree, copy, rmtree

import os
import json
import chissy


# check if is root user
if os.getuid() != 0:
    print("[!!] WTF!!! Are you drunk???")
    print("[!!] This script need root user")
    exit(-1)

# installation path
install_path = "/opt/chissy/{version}".format(version=chissy.__version__)
symlink_path = '/usr/bin/chissy'
service_path = '/usr/lib/systemd/system/chissy.service'

# path used for logs
logs_path = '/var/log/chissy'

# files to be copied
install_files = [
    'chissy',
    'conf',
    'chissy.sh',
    'chissy.py'
]

# files to be applied 'chmod +x'
exec_files = [
    "chissy.sh",
    "chissy.py"
]


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

        print('[*] Files copied')

        # create symbolic link on /usr/bin to chissy
        os.symlink('/'.join([install_path, "chissy.sh"]), symlink_path)
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
        print('[*] Usage: systemctl {start|stop|restart} chissy')
        print()
    except Exception as e:
        print('[!!] Caught a exception while installing. ' + str(e))
        exit(-1)


# function to uninstall chessy
def uninstall():
    print()
    print("[*] Uninstall starting...")
    try:
        # remove service and symlink
        if os.path.exists(service_path):
            os.remove(service_path)
        if os.path.exists(symlink_path):
            os.remove(symlink_path)

        # remove installation path
        rmtree(install_path)
        print("[*] Uninstall complete")
        print()
    except Exception as e:
        print('[!!] Caught a exception while uninstalling. ' + str(e))
        exit(-1)


# function to check if chissy is already installed
def check_install():
    if os.path.isdir(install_path):
        print('[!!] Chissy is already installed')
        print()
        while 1:
            resp = input('[?] You want to reinstall it? (y/N): ')
            resp = resp.lower()
            if resp == "y" or resp == "ye" or resp == "yes":
                uninstall()
                break
            elif resp == "" or resp == "n" or resp == "no" or resp == "not":
                exit(0)


# main
if __name__ == '__main__':
    check_install()
    install()