# coding=utf-8
# funnylab.org
#
import logging
import os
import pymongo
from onecore.model import Model

__author__ = 'valorzhong'

def get_logger(identifier='valorzhong'):
    p = '/var/log/%s/' % identifier
    if not os.path.exists(p):
        os.mkdir(p)
    logging.basicConfig(filename=os.path.join(p, '%s_spider.log' % identifier),
                        format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(identifier)
    logger.setLevel(logging.INFO)
    return logger


class Repository(object):

    connection = None

    def __enter__(self):
        try:
            self.connection = pymongo.Connection()
        except Exception, err:
            print err.message
            get_logger().error(err.message)
        return self

    def __exit__(self, *args):
        self.connection.end_request()

    def disconnect(self):
        self.connection.disconnect()