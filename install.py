#!/bin/env python3

import os
from shutil import copytree
import chissy


# check if is root user
if os.getuid() != 0:
    print("[!!] WTF!!! Are you drunk???")
    print("[!!] This script need root user")
    exit(-1)

# installation path
install_path = "/opt/chissy/{version}".format(version=chissy.__version__)

# files to be copied
install_files = {
    'chissy',
    'conf',
    'chissy.sh',
    'run.py'
}

# file to be applied 'chmod +x'
exec_files = {
    "chissy.sh",
    "run.py"
}


# function to install chissy
def install():
    print("[*] Install starting...")
    try:
        # copy file on installation path
        os.makedirs(install_path)
        for file in install_files:
            copytree(file, install_path)
        # add executable permission
        for file in exec_files:
            os.system("chmod +x {file}". format(file=file))

        print('[*] File copied')

        # create symbolic link on /usr/bin to chissy
        os.symlink("{path}/{file}".format(path=install_path, file="chissy.sh"), '/usr/bin/chissy')
        print('[*] Symbolic link created')

        # add settings for daemon
        service_file = open('template/systemd/chissy.service', 'r').read()
        service_file = service_file.format(workdir=install_path)
        print(service_file)
        file = open('/usr/lib/systemd/system/chessy.service', 'w')
        file.write(service_file)

        # # copy('template/init.d/chissy', '/etc/init.d/chissy')
        # # os.system('chmod +x /etc/init.d/chissy')
        print('[*] Daemon created')
        print('[*] Installation complete')
        print('[*] Usage: systemctl {start|stop|restart} chissy')
    except Exception as e:
        print('[!!] Caught a exception while installing. ' + str(e))


# function to uninstall chessy
def uninstall():
    print("[*] Uninstall starting...")

    os.removedirs(install_path)
    if os.path.isfile('/usr/lib/systemd/system/chessy.service'):
        os.remove('/usr/lib/systemd/system/chessy.service')
    if os.path.isfile('/usr/bin/chissy'):
        os.remove('/usr/bin/chissy')

    print("[*] Uninstall complete")


# function to check if chissy is already installed
def check_install():
    if os.path.exists(install_path):
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
