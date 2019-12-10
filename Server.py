#!/usr/bin/env python

import socket
import threading
import sys
import paramiko

# host rsa key
host_key = paramiko.RSAKey(filename='test_rsa.key');


# class server
class Server(paramiko.ServerInterface):

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        print('kind: ' + kind)
        print('chain id: ' + str(chanid))
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        print('user: ' + username)
        print('password ' + password)
        if (username == 'hxs') and (password == 'dio'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print('[*] Listening for connection...')
    client, addr = sock.accept()
except Exception as e:
    print('[!!] Listen failed: ' + str(e))
    sys.exit(1)

print('[*] Got connection!!!')
print('client: ' + str(client))
print('addr: ' + str(addr))

try:
    session = paramiko.Transport(client)
    session.add_server_key(host_key)
    server = Server()

    try:
        session.start_server(server=server)
    except paramiko.SSHException as e:
        print('[!!] SSH negotiation failed.')

    chan = session.accept(20)
    print('[*] AUTHENTICATED')
    print(str(chan))
    chan.send('Welcome to SSH server')
except Exception as e:
    print('[!!] Caught exception: ' + str(e))
    try:
        session.close()
    except IndexError:
        pass
    sys.exit(1)
