#!/usr/bin/env python

import pytex
import os
import unittest
import logging

open('./logs/test.log', mode='a').close()
logging.basicConfig(filename='./logs/test.log',
                    level=logging.DEBUG,
                    format='%(asctime)s\t-\t%(message)s')
logging.info('Start Test Sequence\n')

class TestPyTeX(unittest.TestCase):
    '''
    Unittest for PyTeX
    Tests currently implemented functions
    '''

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        self.document1 = pytex.PyTexDocument(name='1.tex',
                                                packages=[['geometry', 'margin=1in'],['times']])
        self.document2 = pytex.PyTexDocument(name='2.tex')
        self.document3 = pytex.PyTexDocument(name='3.tex',
                                                doc_class='article',
                                                packages=[['geometry', 'margin=1in'],['times']])

    def tearDown(self):
        os.system("for FILE in `find . -maxdepth 1 -type f | grep -e 'aux\|log'`; do mv $FILE ./logs/; done")
        os.system("for FILE in `find . -maxdepth 1 -type f | grep -e 'pdf\|tex'`; do mv $FILE ./old/; done")

    def test_basic_document(self):
        self.document1.raw_latex('test string\n')
        self.document1.write()
        lines = self.get_line_list('1.tex')
        assert(lines == ['\\documentclass[10pt]{report}\n',
                        '\\usepackage[margin=1in]{geometry}\n',
                        '\\usepackage{times}\n',
                        '\\begin{document}\n',
                        'test string\n',
                        '\\end{document}'])

    def test_title(self):
        self.document2.title(title='Test Document', author='William Farmer')
        self.document2.write()
        lines = self.get_line_list('2.tex')
        assert(lines == ['\\documentclass[10pt]{report}\n',
                        '\\usepackage[margin=1in]{geometry}\n',
                        '\\begin{document}\n',
                        '\\title{Test Document}\n',
                        '\\author{William Farmer}\n',
                        '\\date{\\today}\n',
                        '\\maketitle\n',
                        '\\end{document}'])

    def test_table(self):
        self.document3.title()
        array = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.document3.table(array)
        self.document3.write()
        lines = self.get_line_list('3.tex')
        logging.info(lines)
        assert(lines == ['\\documentclass[10pt]{article}\n',
                        '\\usepackage[margin=1in]{geometry}\n',
                        '\\usepackage{times}\n',
                        '\\begin{document}\n',
                        '\\title{Insert Title Here}\n',
                        '\\author{Insert Name Here}\n',
                        '\\date{\\today}\n',
                        '\\maketitle\n',
                        '\\begin{tabular}{l | l | l}\n',
                        '1 & 2 & 3\\\\\n',
                        '4 & 5 & 6\\\\\n',
                        '7 & 8 & 9\\\\\n',
                        '\\end{tabular}\n',
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
