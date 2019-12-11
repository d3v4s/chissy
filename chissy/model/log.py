import datetime
import os


class Log:
    __instance = None
    __conf_log = None

    # singleton
    def __new__(cls, conf_log):
        return object.__new__(cls) if Log.__instance is None else Log.__instance

    def __init__(self, conf_log):
        Log.__instance = self
        self.__conf_log = conf_log

        # create log directory if not exists
        if not os.path.exists(conf_log['path']):
            os.makedirs(conf_log['path'])

    # function to write log
    def write_log(self, username, password, address):
        # set view for address
        address = ':'.join([address[0], str(address[1])])

        # get log name and write on it
        filename = "{date}.log".format(date=datetime.date.today())
        with open('/'.join([self.__conf_log['path'], filename]), 'a') as file:
            file.write(self.__conf_log['format'].format(datetime=datetime.datetime.now(), username=username,
                                                        password=password, address=address) + "\n")

    # function to rotate the logs
    def __rotate__(self):
        return
