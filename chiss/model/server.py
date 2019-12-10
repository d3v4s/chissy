import threading
import paramiko


# class server
class Server(paramiko.ServerInterface):
    __chiss = None
    address = None

    def __init__(self):
        from chiss.core.chiss import Chiss
        self.event = threading.Event()
        self.__chiss = Chiss()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        print('[+] Username: ' + username)
        print('[+] Password: ' + password)
        self.__chiss.write_log(username, password, self.address)
        return paramiko.AUTH_FAILED
