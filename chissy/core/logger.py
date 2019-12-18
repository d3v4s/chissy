import datetime
import os
import re

from os import walk


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
        if not self.__validate_date__(from_date):
            raise ValueError("[!!] Date format not valid")
        self.__from_date = from_date

    def set_to_date(self, to_date):
        if not self.__validate_date__(to_date):
            raise ValueError("[!!] Date format not valid")
        self.__to_date = to_date

    def set_address(self, address):
        if not self.__validate_address__(address):
            raise ValueError("[!!] Address format not valid")
        self.__address = address

    # def get_from_date(self):
    #     return self.__from_date
    #
    # def get_to_date(self):
    #     return self.__to_date
    #
    # def get_address(self):
    #     return self.__address

    # function to validate a IPv4 address
    @staticmethod
    def __validate_address__(address_str):
        regex = '^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.' \
                '(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.' \
                '(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.' \
                '(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'
        return True if re.search(regex, address_str) else False

    # function to validate a date
    @staticmethod
    def __validate_date__(date_str):
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    # function to write log
    def write_log(self, username, password, address):
        # set view for address
        address = ':'.join([address[0], str(address[1])])

        # get log name and write on it
        filename = "{date}.log".format(date=datetime.date.today())
        with open('/'.join([self.__conf_log['path'], filename]), 'a') as file:
            file.write(self.__conf_log['format'].format(datetime=datetime.datetime.now(), username=username,
                                                        password=password, address=address) + "\n")

    # function to read the logs
    def read_log(self):
        log_files = self.__get_log_files__()
        out = ''
        for log_file in log_files:
            path = '{logdir}/{file}'.format(logdir=self.__conf_log['path'], file=log_file)
            f = open(path, 'r')
            out += f.read() if self.__address is None else self.__grep_address__(f)
            f.close()

        return out

    def remove_log(self):
        log_files = self.__get_log_files__()
        print('[*] Log files that match:')
        print(' - '.join(log_files))
        while 1:
            resp = input('[?] Do you want to remove these log files? (Y/n) ')
            resp = resp.lower()
            if resp == '' or resp == 'y' or resp == 'ye' or resp == 'yes':
                for file in log_files:
                    os.remove('{logdir}/{file}'.format(logdir=self.__conf_log['path'], file=file))
                print('[*] All selected log files are removed successfully')
                break
            elif resp == 'n' or resp == 'no':
                break

    # function to get only the line with same ip address of attributes
    def __grep_address__(self, logFile):
        out = ''
        for line in logFile.readlines():
            if re.search(self.__address, line):
                out += line
        return out

    # function to get log files by class attributes
    def __get_log_files__(self):
        files = []
        # get file from log directory
        for (dirpath, dirnames, filenames) in walk(self.__conf_log['path']):
            files.extend(filenames)
            break
        logFiles = []
        # iterate files in log directory
        for file in files:
            # regex to find log files
            res = re.findall("^([\d]{4}-[\d]{2}-[\d]{2})\.log$", file)
            if len(res) == 0:
                continue
            # get date from log filename
            date = datetime.date.fromisoformat(res[0])
            # append log files that fall within the dates indicated
            # print('from: ' + str(datetime.datetime.strptime(self.__from_date, '%Y-%m-%d').date()))
            # print('to: ' + str(datetime.datetime.strptime(self.__to_date, '%Y-%m-%d').date()))
            if (self.__from_date is None or
                datetime.datetime.strptime(self.__from_date, '%Y-%m-%d').date() <= date) and \
                    (self.__to_date is None or
                     datetime.datetime.strptime(self.__to_date, '%Y-%m-%d').date() >= date):
                logFiles.append(res[0] + '.log')

        return logFiles
