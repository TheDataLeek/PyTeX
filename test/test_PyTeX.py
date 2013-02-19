#!/usr/bin/env python

import pytex
import os
import unittest
import sys
import logging

open('./logs/test.log', mode='a').close()
logging.basicConfig(filename='./logs/test.log',
                    level=logging.DEBUG,
                    format='%(asctime)s\t-\t%(message)s')
logging.info('Start Test Sequence\n')

class TestPyTeX(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        self.testDocument1 = pytex.PyTexDocument(name='1.tex',
                                                packages=[['geometry', 'margin=1in'],['times']])
        self.testDocument2 = pytex.PyTexDocument(name='2.tex')
        self.testDocument3 = pytex.PyTexDocument(name='3.tex',
                                                doc_class='article',
                                                packages=[['geometry', 'margin=1in'],['times']])

    def tearDown(self):
        os.system("for FILE in `find . -maxdepth 1 -type f | grep -e 'aux\|log'`; do mv $FILE ./logs/; done")

    def test_basic_document(self):
        self.testDocument1.raw_latex('test string\n')
        self.testDocument1.write()
        lines = self.get_line_list('1.tex')
        assert(lines == ['\\documentclass[10pt]{report}\n',
                        '\\usepackage[margin=1in]{geometry}\n',
                        '\\usepackage{times}\n',
                        '\\begin{document}\n',
                        'test string\n',
                        '\\end{document}'])

    def test_title(self):
        self.testDocument2.title(title='Test Document', author='William Farmer')
        self.testDocument2.write()
        lines = self.get_line_list('2.tex')
        assert(lines == ['\\documentclass[10pt]{report}\n',
                        '\\usepackage[margin=1in]{geometry}\n',
                        '\\begin{document}\n',
                        '\\title{Test Document}\n',
                        '\\author{William Farmer}\n',
                        '\\date{\\today}\n',
                        '\\maketitle\n',
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
