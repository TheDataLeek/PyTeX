#!/usr/bin/env python
"""
LaTeX API
William Farmer
2013
"""

import os


class PyTexDocument:
    '''
    LaTeX API Document Class Object
    '''

    def __init__(self, name='out.tex', doc_class='report', options=None, packages=None):
        '''
        Defines the file to work on as well as options
        :param name:
        :param doc_class:
        :param options:
        :param packages:
        '''
        if not packages:
            packages = [['geometry', 'margin=1in']]
        if not options:
            options = ['10pt']
        self.name = name
        self.outfile = open(self.name, mode='w')

        self.outfile.write('\\documentclass[')
        for number in range(len(options) - 2):
            self.outfile.write('%s, ' % options[number])
        self.outfile.write('%s]{%s}\n' % (options[len(options) - 1], doc_class))

        for item in packages:
            try:
                self.outfile.write('\\usepackage[%s]{%s}\n' % (item[1], item[0]))
            except IndexError:
                self.outfile.write('\\usepackage{%s}\n' % item[0])
        self.outfile.write('\\begin{document}\n')

    def title(self, title='Insert Title Here', author='Insert Name Here', date='\\today'):
        '''
        Define and make the title
        :param title:
        :param author:
        :param date:
        '''
        self.outfile.write('''\\title{%s}\n\\author{%s}\n\\date{%s}\n\\maketitle\n''' % (title, author, date))

    def raw_latex(self, latex):
        '''
        Allows the user to write raw LaTeX to the document
        :param latex:
        '''
        self.outfile.write(latex)

    def table(self, array):
        '''
        Writes a table
        :param array:
        '''
        size = len(array[0])
        self.outfile.write('\\begin{tabular}{l%s}\n' % ((size - 1) * ' | l'))
        for entry in array:
            self.outfile.write(str(entry[0]))
            for number in range(1, len(entry)):
                self.outfile.write(' & %s' % (entry[number]))
            self.outfile.write('\\\\\n')
        self.outfile.write('\\end{tabular}\n')

    def graph(self, array, options=None):
        '''
        Creates graph of given data
        :param array:
        :param options:
        '''
        if not options:
            options = [[]]
        print(array)

    def write(self):
        '''
        End the document, close the file, and compile the pdf
        '''
        self.outfile.write('\\end{document}')
        self.outfile.close()
        #subprocess.Popen(['pdflatex', '--shell-escape', self.name])
        os.system('pdflatex --shell-escape %s' % self.name)

