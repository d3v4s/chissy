import os
import sys
import socket
import paramiko

from chissy.model.server import Server
from chissy.core.logger import Logger
from collections import defaultdict


class Controller:
    __instance = None
    __command = None
    __conf_server = None
    __conf_log = None
    __log = None

    def __new__(cls, command=None, conf_server=None, conf_log=None):
        # singleton
        return object.__new__(cls) if Controller.__instance is None else Controller.__instance

    def __init__(self, command=None, conf_server=None, conf_log=None):
        if Controller.__instance is not None:
            return
        Controller.__instance = self
        # set attributes
        self.__conf_server = conf_server
        self.__conf_log = conf_log
        self.__command = command
        self.__log = Logger(conf_log)

    #####################################
    # PRIVATE METHODS
    #####################################

    # method to start fake server
    def __startServer__(self):
        print('[*] Starting server...')
        # server loop
        while 1:
            # create socket and listen on it
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind((self.__conf_server['address'], self.__conf_server['port']))
                sock.listen(100)
                print()
                print('[*] Listening for connection...')
                client, address = sock.accept()
            except Exception as e:
                print('[!!] Listen failed: ' + str(e))
                sock.close()
                sys.exit(-1)

            # hacker is connected, now sniff it!!!
            print('[*] Caught the hacker!!!')
            print('[+] Address: ' + str(address))
            try:
                # set server
                session = paramiko.Transport(client)
                session.add_server_key(paramiko.RSAKey(filename=self.__conf_server['host-key-filename']))
                server = Server()
                server.address = address
                server.logger = self.__log

                # start session
                try:
                    session.start_server(server=server)
                except paramiko.SSHException as e:
                    print('[!!] SSH negotiation failed. Error: ' + str(e))

                # timeout maximum: 14
                # else throw paramiko exception
                session.accept(10)
                session.close()
                sock.close()
            except Exception as e:
                print('[!!] Caught exception: ' + str(e))
                try:
                    session.close()
                    sock.close()
                except IndexError:
                    pass
                try:
                    if e.args[0] != 104:
                        sys.exit(-1)
                except IndexError:
                    pass

    # method to read the logs
    def __readLog__(self):
        options = sys.argv[2:]

        # set options map
        switcher = {
            '--address': self.__log.set_address,
            '-a': self.__log.set_address,
            '--from-date': self.__log.set_from_date,
            '-f': self.__log.set_from_date,
            '--to-date': self.__log.set_to_date,
            '-t': self.__log.set_to_date
        }

        # iterate options
        for i, opt in enumerate(options):
            setter = switcher.get(opt, 0)
            if setter == 0:
                continue
            setter(options[i+1])

        print(self.__log.read_log())

    # method to remove the logs
    def __removeLog__(self):
        options = sys.argv[2:]

        # set options map fo switcher
        opt_map = {
            self.__log.set_from_date: ['-f', '--from-date'],
            self.__log.set_to_date: ['-t', '--to-date']
        }

        # invert kay and value of map to create switcher
        switcher = defaultdict(list)
        for key, value in opt_map.items():
            switcher[value].append(key)

        # iterate options
        for i, opt in enumerate(options):
            setter = switcher.get(opt, 0)
            if setter == 0:
                continue
            setter(options[i+1])

        self.__log.remove_log()

    # method for invalid command
    def __invalidCommand__(self):
        print('[!!] Invalid command ' + str(self.__command))
        print('[!!] Show the help with "{name} help"'.format(name=sys.argv[0]))
        sys.exit(1)

    #####################################
    # PUBLIC METHODS
    #####################################

    # method to execute the request command
    def execute(self):
        # switch command and call function
        switcher = {
            "start": self.__startServer__,
            "get-log": self.__readLog__,
            "remove-log": self.__removeLog__
        }
        func = switcher.get(self.__command, self.__invalidCommand__)
        func()
