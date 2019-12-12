#!/bin/env python3
from shutil import copytree, copy, rmtree

import os
import sys
import json
import chissy
import pkg_resources

# read config from file
file = open('install.json')
install_config = json.load(file)
file.close()

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
install_path = "{path}/{version}".format(path=install_config['installation-path'], version=chissy.__version__)
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
    # 'install.py'
]

# files to be applied 'chmod +x'
exec_files = [
    'chissy.sh',
    'chissy.py',
    # 'install.py'
]

# read need packages from requirements.txt
file = open('requirements.txt')
req_packages = file.read()
file.close()
req_packages = req_packages.split('\n')
try:
    req_packages.remove('')
except ValueError:
    pass

# help
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
        for f in install_files:
            to = '/'.join([install_path, f])
            if os.path.isfile(f):
                copy(f, to)
            else:
                copytree(f, to)

        # add execution permission
        for f in exec_files:
            os.system("chmod +x {path}/{file}".format(path=install_path, file=f))

        # change log directory
        path = '/'.join([install_path, 'conf', 'log.json'])
        f = open(path, 'r')
        conf_log = json.load(f)
        f.close()
        conf_log['path'] = logs_path
        json_out = json.dumps(conf_log, sort_keys=True, indent=4, separators=(',', ': '))
        f = open(path, 'w')
        f.write(json_out)
        f.close()

        # create new key
        while 1:
            resp = input('[?] Generate new private key? (Y/n)')
            resp = resp.lower()
            if resp == '' or resp == 'y' or resp == 'ye' or resp == 'yes':
                # generate RSA key
                exc = 'openssl req -new -x509 -nodes -keyout {path}/conf/key/rsa.key'.format(path=install_path)
                os.system(exc)
                exc = 'ssh-keygen -p -m PEM -f {path}/conf/key/rsa.key'.format(path=install_path)
                os.system(exc)

                # change key on configurations
                path = '/'.join([install_path, 'conf', 'server.json'])
                f = open(path, 'r')
                conf_server = json.load(f)
                f.close()
                conf_server['host_key_filename'] = '{path}/conf/key/rsa.key'.format(path=install_path)
                json_out = json.dumps(conf_server, sort_keys=True, indent=4, separators=(',', ': '))
                f = open(path, 'w')
                f.write(json_out)
                f.close()
                break
            elif resp == 'n' or resp == 'no':
                break


        # add bash complete
        if os.path.isdir(completions_path):
            f = open('/'.join([completions_path, 'chissy']), 'w')
            f.write("complete -W 'start get-log version help' chissy")
            f.close()

        # create logs dir /var/log/chissy
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)

        print('[*] Files copied')

        # create symbolic link on /usr/bin to chissy
        os.symlink('/'.join([install_path, "chissy.sh"]), symlink_bin)
        # create symlink on /etc/chissy to conf
        os.symlink('/'.join([install_path, 'conf']), symlink_etc)
        print('[*] Symbolic links created')

        # add settings for daemon
        if install_config['systemd-service']:
            service_file = open('template/systemd/chissy.service', 'r')
            chiss_service = service_file.read()
            service_file.close()
            chiss_service = chiss_service.format(workdir=install_path, version=chissy.__version__)
            f = open(service_path, 'w')
            f.write(chiss_service)
            f.close()
            os.system('systemctl daemon-reload')
            print('[*] Systemd service created')

        # install require packages
        installed_pckgs = pkg_resources.working_set
        installed_pckgs = sorted(["%s" % i.key for i in installed_pckgs])
        for pckg in req_packages:
            if pckg not in installed_pckgs:
                install_package(pckg)

        print('[*] Installation complete')
        print()
        print('[*] Usage: chissy {start|get-log|version|help} [options]')
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
        if os.path.islink(symlink_bin):
            os.remove(symlink_bin)
        if os.path.islink(symlink_etc):
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
            resp = input('[?] Do you want to reinstall it? (y/N): ')
            resp = resp.lower()
            if resp == "y" or resp == "ye" or resp == "yes":
                uninstall()
                break
            elif resp == "" or resp == "n" or resp == "no" or resp == "not":
                sys.exit(0)

    # remove service and symlink
    if os.path.exists(service_path):
        os.remove(service_path)
    if os.path.islink(symlink_bin):
        os.remove(symlink_bin)
    if os.path.islink(symlink_etc):
        os.remove(symlink_etc)

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


def install_package(pckg):
    print('[!!] Chissy application need ' + pckg)
    while 1:
        resp = input("[?] Install it now with pip? (Y/n)")
        resp = resp.lower()
        if resp == '' or resp == 'y' or resp == 'ye' or resp == 'yes':
            if os.path.exists('/usr/bin/pip3'):
                os.system('pip3 install ' + pckg)
            else:
                print('[!!] You don\'t have pip3 installed!!!')
            break
        elif resp == 'n' or resp == 'no':
            break


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
