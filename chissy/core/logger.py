import datetime
import os
import re

from os import walk
from chissy.enum.log import LogEnum


class Logger:
    __instance = None
    __conf_log = None
    __from_date = None
    __to_date = None
    __address = None

    # singleton
    def __new__(cls, conf_log=None):
        return object.__new__(cls) if Logger.__instance is None else Logger.__instance

    def __init__(self, conf_log=None):
        if Logger.__instance is not None:
            return

        Logger.__instance = self
        self.__conf_log = conf_log
        # create log directory if not exists
        if not os.path.exists(conf_log['path']):
            os.makedirs(conf_log['path'])

    ###########################
    # SETTER
    ###########################

    def set_from_date(self, from_date):
        self.__from_date = from_date

    def set_to_date(self, to_date):
        self.__to_date = to_date

    def set_address(self, address):
        self.__address = address

    # def get_from_date(self):
    #     return self.__from_date
    #
    # def get_to_date(self):
    #     return self.__to_date
    #
    # def get_address(self):
    #     return self.__address

    # function to write log
    def write_log(self, username, password, address):
        # set view for address
        address = ':'.join([address[0], str(address[1])])

        # get log name and write on it
        filename = "{date}.log".format(date=datetime.date.today())
        with open('/'.join([self.__conf_log[LogEnum.PATH], filename]), 'a') as file:
            file.write(self.__conf_log[LogEnum.FORMAT].format(datetime=datetime.datetime.now(), username=username,
                                                              password=password, address=address) + "\n")

    # function to read the logs
    def read_log(self):
        # logDir = open(self.__conf_log[LogEnum.PATH])
        files = []
        for (dirpath, dirnames, filenames) in walk(self.__conf_log['path']):
            files.extend(filenames)
            break
        logFiles = []
        for file in files:
            res = re.findall("^([\d]{4}-[\d]{2}-[\d]{2})\.log$", file)
            if not len(res) == 0:
                logFiles.append(res[0])
        print(str(logFiles))

    # function to rotate the logs
    def __rotate__(self):
        return
