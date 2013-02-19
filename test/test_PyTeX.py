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
        self.testDocument1 = pytex.PyTexDocument(name='1.tex', packages=[['geometry', 'margin=1in'],['times']])
        self.testDocument2 = pytex.PyTexDocument(name='2.tex')
        self.testDocument3 = pytex.PyTexDocument(name='3.tex', doc_class='article',
                                                packages=[['geometry', 'margin=1in'],['times']])

    def test_basic_document(self):
        self.testDocument1.write()
        lines = self.get_line_list('1.tex')
        assert(lines == ['\\begin[10pt]{report}\n',
                        '\\usepackage[margin=1in]{geometry}\n',
                        '\\usepackage{times}\n',
                        '\\begin{document}\n',
                        '\\end{document}'])

    def get_line_list(self, name):
        outfile = open(name, mode='r')
        line_list = []
        for item in outfile.readlines():
            line_list.append(item)
        outfile.close()
        return line_list



if __name__ == "__main__":
    unittest.main()
