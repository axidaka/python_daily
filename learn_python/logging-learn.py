# coding: utf-8

import logging
import os.path
import sys


def Uselogging_test():
    log_file = os.path.realpath(sys.argv[0])[0:-3] + '.log'
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        filename=log_file,
                        filemode='w')

    logging.debug('logging.debg:this is a debug msg %s', 'by zhqsa')

    _logger = logging.getLogger(__name__)
    _logger.debug('logger.debug:this is a debug msg:%s', 'by zhqs')
    _logger.warning('this is a warning msg')

    # 将日志同时输出到文件和屏幕
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)

    _logger.addHandler(console)

    logging.debug('***Test: This is a debug msg')
    logging.info('***Test: This is a info msg')
    logging.warning('***Test: This is a warning msg')


def main():

    Uselogging_test()

if __name__ == '__main__':
    main()
