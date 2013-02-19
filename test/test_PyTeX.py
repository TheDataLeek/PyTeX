#!/usr/bin/env python

import pytex
import unittest
import sys
import logging

open('log.txt', mode='w').close()
logging.basicConfig(filename='log.txt',
                    level=logging.DEBUG,
                    format='%(asctime)s\t-\t%(message)s')
logging.info('Start Test Sequence\n')

class TestPyTeX(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        self.testDocument1 = pytex.PyTexDocument()
        self.testDocument2 = pytex.PyTexDocument()
        self.testDocument3 = pytex.PyTexDocument()

    def get_line_list(self):
        outfile = open('out.tex', mode='r')
        line_list = []
        print(outfile.readlines())
#        for item in outfile.readlines:
#            line_list.append(item)
        outfile.close()
        return line_list



if __name__ == "__main__":
    unittest.main()
