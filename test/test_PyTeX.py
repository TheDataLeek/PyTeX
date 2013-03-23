#!/usr/bin/env python

import pytex
import unittest
import logging

open('test.log', mode='w').close()
logging.basicConfig(filename='test.log',
                    level=logging.DEBUG,
                    format='%(asctime)s\t-%(message)s')
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
                                             packages=[['geometry', 'margin=1in'], ['times']])
        self.document2 = pytex.PyTexDocument(name='2.tex')
        self.document3 = pytex.PyTexDocument(name='3.tex',
                                             doc_class='article',
                                             packages=[['geometry', 'margin=1in'], ['times']])

    def test_basic_document(self):
        logging.info('TESTING BASIC DOCUMENT')

        self.document1.write()
        self.document2.write()
        self.document3.write()
        logging.info('\n			' + self.document1.content.replace('\n', '\n			'))
        logging.info('\n			' + self.document2.content.replace('\n', '\n			'))
        logging.info('\n			' + self.document3.content.replace('\n', '\n			'))
        assert(self.document1.content == ('\\documentclass[10pt]{report}\n' +
                                          '\\usepackage[margin=1in]{geometry}\n' +
                                          '\\usepackage{times}\n' +
                                          '\\begin{document}\n' +
                                          '\n\\end{document}'))
        assert(self.document2.content == ('\\documentclass[10pt]{report}\n' +
                                          '\\usepackage[margin=1in]{geometry}\n' +
                                          '\\begin{document}\n' +
                                          '\n\\end{document}'))
        assert(self.document3.content == ('\\documentclass[10pt]{article}\n' +
                                          '\\usepackage[margin=1in]{geometry}\n' +
                                          '\\usepackage{times}\n' +
                                          '\\begin{document}\n' +
                                          '\n\\end{document}'))

    def test_doc_math(self):
        logging.info('Testing Math Functionality')

        self.document1.title('Test Document', 'Will Farmer')
        self.document1.math('5x^2 + 4x = 0')
        self.document1.write()
        self.document2.title()
        self.document2.write()
        self.document3.title('Test Document', 'Will Farmer', '2013/03/20')
        self.document3.write()

        logging.info('\n			' + self.document1.content.replace('\n', '\n			'))
        logging.info('\n			' + self.document2.content.replace('\n', '\n			'))
        logging.info('\n			' + self.document3.content.replace('\n', '\n			'))

        assert(self.document1.content == ('\\documentclass[10pt]{report}\n' +
                                          '\\usepackage[margin=1in]{geometry}\n' +
                                          '\\usepackage{times}\n' +
                                          '\\begin{document}\n' +
                                          '\\title{Test Document}\n' +
                                          '\\author{Will Farmer}\n' +
                                          '\\date{\\today}\n' +
                                          '\\maketitle\n' +
                                          '$ 5x^2 + 4x = 0 $\n' +
                                          '\\end{document}'))
        assert(self.document2.content == ('\\documentclass[10pt]{report}\n' +
                                          '\\usepackage[margin=1in]{geometry}\n' +
                                          '\\begin{document}\n' +
                                          '\\title{Insert Title Here}\n' +
                                          '\\author{Insert Name Here}\n' +
                                          '\\date{\\today}\n' +
                                          '\\maketitle\n' +
                                          '\n\\end{document}'))
        assert(self.document3.content == ('\\documentclass[10pt]{article}\n' +
                                          '\\usepackage[margin=1in]{geometry}\n' +
                                          '\\usepackage{times}\n' +
                                          '\\begin{document}\n' +
                                          '\\title{Test Document}\n' +
                                          '\\author{Will Farmer}\n' +
                                          '\\date{2013/03/20}\n' +
                                          '\\maketitle\n' +
                                          '\n\\end{document}'))

    def test_title(self):
        logging.info('Testing Title Functionality')
        self.document1.title('Test Document', 'Will Farmer')
        self.document1.write()
        self.document2.title()
        self.document2.write()
        self.document3.title('Test Document', 'Will Farmer', '2013/03/20')
        self.document3.write()

        logging.info('\n			' + self.document1.content.replace('\n', '\n			'))
        logging.info('\n			' + self.document2.content.replace('\n', '\n			'))
        logging.info('\n			' + self.document3.content.replace('\n', '\n			'))

        assert(self.document1.content == ('\\documentclass[10pt]{report}\n' +
                                          '\\usepackage[margin=1in]{geometry}\n' +
                                          '\\usepackage{times}\n' +
                                          '\\begin{document}\n' +
                                          '\\title{Test Document}\n' +
                                          '\\author{Will Farmer}\n' +
                                          '\\date{\\today}\n' +
                                          '\\maketitle\n' +
                                          '\n\\end{document}'))
        assert(self.document2.content == ('\\documentclass[10pt]{report}\n' +
                                          '\\usepackage[margin=1in]{geometry}\n' +
                                          '\\begin{document}\n' +
                                          '\\title{Insert Title Here}\n' +
                                          '\\author{Insert Name Here}\n' +
                                          '\\date{\\today}\n' +
                                          '\\maketitle\n' +
                                          '\n\\end{document}'))
        assert(self.document3.content == ('\\documentclass[10pt]{article}\n' +
                                          '\\usepackage[margin=1in]{geometry}\n' +
                                          '\\usepackage{times}\n' +
                                          '\\begin{document}\n' +
                                          '\\title{Test Document}\n' +
                                          '\\author{Will Farmer}\n' +
                                          '\\date{2013/03/20}\n' +
                                          '\\maketitle\n' +
                                          '\n\\end{document}'))

    def test_section(self):
        logging.info('TESTING SECTION CREATION')
        self.document1.title('Test Document', 'Will Farmer')

        section1 = self.document1.section('This is a section', True)
        section1.equation('5x^2 = 6x')
        section1.write()

        self.document1.write()
        self.document2.title()
        self.document2.write()
        self.document3.title('Test Document', 'Will Farmer', '2013/03/20')
        self.document3.write()

        logging.info('\n			' + self.document1.content.replace('\n', '\n			'))
        logging.info('\n			' + self.document2.content.replace('\n', '\n			'))
        logging.info('\n			' + self.document3.content.replace('\n', '\n			'))

        assert(self.document1.content == ('\\documentclass[10pt]{report}\n' +
                                          '\\usepackage[margin=1in]{geometry}\n' +
                                          '\\usepackage{times}\n' +
                                          '\\begin{document}\n' +
                                          '\\title{Test Document}\n' +
                                          '\\author{Will Farmer}\n' +
                                          '\\date{\\today}\n' +
                                          '\\maketitle\n' +
                                          '\\input{section_0.tex}\n' +
                                          '\n\\end{document}'))
        assert(self.document2.content == ('\\documentclass[10pt]{report}\n' +
                                          '\\usepackage[margin=1in]{geometry}\n' +
                                          '\\begin{document}\n' +
                                          '\\title{Insert Title Here}\n' +
                                          '\\author{Insert Name Here}\n' +
                                          '\\date{\\today}\n' +
                                          '\\maketitle\n' +
                                          '\n\\end{document}'))
        assert(self.document3.content == ('\\documentclass[10pt]{article}\n' +
                                          '\\usepackage[margin=1in]{geometry}\n' +
                                          '\\usepackage{times}\n' +
                                          '\\begin{document}\n' +
                                          '\\title{Test Document}\n' +
                                          '\\author{Will Farmer}\n' +
                                          '\\date{2013/03/20}\n' +
                                          '\\maketitle\n' +
                                          '\n\\end{document}'))

if __name__ == "__main__":
    unittest.main()
