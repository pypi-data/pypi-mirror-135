import logging
import os
import sys


class Logger(object):
    def __init__(self, folder='logs', name='pcs_scraper'):
        log_folder = os.path.abspath(folder)
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        log_filename = os.path.join(log_folder, name + '.log')
        logging.basicConfig(filename=log_filename,
                            filemode='a',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)
        # create logger
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(logging.DEBUG)

        # create console handler and add to logger (STDOUT)
        ch1 = logging.StreamHandler(sys.stdout)
        ch1.setLevel(logging.DEBUG)
        ch1.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.__logger.addHandler(ch1)

        # create console handler and add to logger (STDERR)
        ch2 = logging.StreamHandler(sys.stderr)
        ch2.setLevel(logging.ERROR)
        ch2.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.__logger.addHandler(ch2)

    def info(self, msg, *args, **kwargs):
        self.__logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.__logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.__logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.__logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.__logger.critical(msg, *args, **kwargs)
