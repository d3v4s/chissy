import threading
import paramiko


# class server for paramiko
class Server(paramiko.ServerInterface):
    log = None
    address = None

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        print('[+] Username: ' + username)
        print('[+] Password: ' + password)
        self.log.write_log(username, password, self.address)
        return paramiko.AUTH_FAILED
