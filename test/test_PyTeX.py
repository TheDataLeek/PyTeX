#!/usr/bin/env python

import unittest
import sys
import logging

import pytex

open('log.txt', mode='w').close()
logging.basicConfig(filename='log.txt',
                    level=logging.DEBUG,
                    format='%(asctime)s\t-\t%(message)s')
logging.info('Start Test Sequence\n')

class TestPyTeX(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)



if __name__ == "__main__":
    unittest.main()
