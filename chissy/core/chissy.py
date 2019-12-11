from chissy.model.server import Server
from chissy.model.log import Log

import socket
import sys

try:
    import paramiko
except IndexError:
    print('[!!] This application need paramiko.')
    print("[!!] To install it execute 'pip install paramiko'")
    exit(-1)


class Chissy:
    __instance = None
    __command = None
    __conf_server = None
    __conf_log = None
    __log = None

    def __new__(cls, command=None, conf_server=None, conf_log=None):
        # singleton
        return object.__new__(cls) if Chissy.__instance is None else Chissy.__instance

    def __init__(self, command=None, conf_server=None, conf_log=None):
        if command is None or conf_server is None or conf_log is None:
            return
        # singleton
        Chissy.__instance = self
        # set attribute
        self.__conf_server = conf_server
        self.__conf_log = conf_log
        self.__command = command
        self.__log = Log(conf_log)

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
                print('[*] Listening for connection...')
                client, address = sock.accept()
            except Exception as e:
                print('[!!] Listen failed: ' + str(e))
                sys.exit(-1)

            print()
            # accepted connection
            print('[*] Caught the hacker!!!')
            print('[+] Address: ' + str(address))
            try:
                # set server
                session = paramiko.Transport(client)
                session.add_server_key(paramiko.RSAKey(filename=self.__conf_server['host_key_filename']))
                server = Server()
                server.address = address
                server.log = self.__log

                # start session
                try:
                    session.start_server(server=server)
                except paramiko.SSHException as e:
                    print('[!!] SSH negotiation failed.')

                session.accept(60)
                session.close()
            except Exception as e:
                print('[!!] Caught exception: ' + str(e))
                try:
                    session.close()
                except IndexError:
                    pass
                sys.exit(-1)

    def __invalidCommand__(self):
        print('[!!] Invalid command ' + str(self.__command))
        sys.exit(1)

    def __readLog__(self):
        return

    def __install__(self):
        return

    #####################################
    # PUBLIC METHODS
    #####################################

    def execute(self):
        # switch command and call function
        switcher = {
            "start": self.__startServer__,
            "read-log": self.__readLog__,
            "install": self.__install__
        }
        func = switcher.get(self.__command, self.__invalidCommand__)
        func()
