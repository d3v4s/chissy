import datetime
import os


class Log:
    __instance = None
    __conf_log = None

    def __new__(cls, conf_log):
        return object.__new__(cls) if Log.__instance is None else Log.__instance

    def __init__(self, conf_log):
        if not os.path.exists(conf_log['path']):
            os.makedirs(conf_log['path'])
        self.__conf_log = conf_log

    def write_log(self, username, password, address):
        address = "{address}:{port}".format(address=address[0], port=address[1])
        filename = "{date}.log".format(date=datetime.date.today())
        with open("{path}/{file}".format(path=self.__conf_log['path'], file=filename), 'a') as file:
            file.write(self.__conf_log['format'].format(datetime=datetime.datetime.now(), username=username,
                                                        password=password, address=address) + "\n")


