#!/usr/bin/env python
"""
LaTeX API
William Farmer
2013
"""

IMPORT_FLAG = True
import os
import subprocess
import re
try:
    import numpy
    import scipy
    import pylab
except RuntimeError:
    IMPORT_FLAG = False
    print('Python 3.2.3 Not Supported')


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
            formatted_array = self.detect_math(entry)
            self.outfile.write(str(formatted_array[0]))
            for number in range(1, len(formatted_array)):
                self.outfile.write(' & %s' % (formatted_array[number]))
            self.outfile.write('\\\\\n')
        self.outfile.write('\\end{tabular}\n')

    def detect_math(self, entry):
        '''
        When given a list of strings, it detects any math bits and returns.
        :param entry:
        '''
        formatted_list = []
        for item in entry:
            if re.search('[0-9\+\-\=\*\^]', str(item)):
                formatted_list.append('$%s$' %item)
            else:
                formatted_list.append(item)
        return formatted_list

    def equation(self, latex_math, label=None):
        '''        self.outfile.write('\\subsubsection{%s}\n' %title)
        Insert a new equation. Equation must be in LaTeX Form.
        :param latex_math:
        '''
        if label:
            label.replace(' ', '')
            self.outfile.write('\\begin{equation}\\label{eq:%s}\n' %label)
        else:
            self.outfile.write('\\begin{equation}\n')
        self.outfile.write('\\begin{aligned}\n')
        self.raw_latex(latex_math)
        self.outfile.write('\\end{aligned}\n')
        self.outfile.write('\\end{equation}\n')

    def math(self, math, newline=False):
        '''
        Inserts inline math. Math must be in LaTeX form.
        :param math:
        :param newline:
        '''
        if newline:
            self.outfile.write('\\[\n')
            self.outfile.write('\\begin{aligned}\n')
            self.raw_latex(math)
            self.outfile.write('\\end{aligned}\n')
            self.outfile.write('\\]\n')
        else:
            self.outfile.write('$ %s $' %math)

    def graph(self, array, options=None):
        '''
        Creates graph of given data
        :param array:
        :param options:
        '''
        if IMPORT_FLAG:
            if not options:
                options = [[]]
            print(array)
            pylab.plot(array[0], array[1])
            pylab.show()


    def write(self):
        '''
        End the document, close the file, and compile the pdf
        '''
        self.outfile.write('\\end{document}')
        self.outfile.close()
        #subprocess.Popen(['pdflatex', '--shell-escape', self.name])
        os.system('pdflatex --shell-escape %s' % self.name)

    def picture(self, filename, scale=0.5, label=None, caption=None):
        '''
        Insert a picture. Needs to be png
        :param filename:
        :param label:
        :param caption:
        '''
        self.outfile.write('\\begin{figure}[ht]\n')
        self.outfile.write('\\centering\n')
        self.outfile.write('\\includegraphics[scale=%f]{%s}\n' %(scale, filename))
        if label:
            self.outfile.write('\\label{fig:%s}\n' %label)
        if caption:
            self.outfile.write('\\caption{%s}\n' %caption)
        self.outfile.write('\\end{figure}\n')

    def section(self, title='Section Title', contents=None):
        '''
        Creates a new section and writes contents
        If no new sections are created, it will have everything in this one.
        Note, contents are added in the order of the list.
        :param title:
        :param contents:
        '''
        self.outfile.write('\\section{%s}\n' %title)

    def subsection(self, title='Subsection Title', contents=None):
        '''
        Creates a new subsection and writes contents
        If no new subsections are created, it will have everything in this one.
        Note, contents are added in the order of the list.
        :param title:
        :param contents:
        '''
        self.outfile.write('\\subsection{%s}\n' %title)

    def subsubsection(self, title='Subsubsection Title', contents=None):
        '''
        Creates a new subsubsection and writes contents
        If no new subsubsections are created, it will have everything in this one.
        Note, contents are added in the order of the list.
        :param title:
        :param contents:
        '''
        self.outfile.write('\\subsubsection{%s}\n' %title)

    def appendix(self, contents):
        '''
        Creates a new appendix. Note, the appendix needs sections.
        :param contents:
        '''
        self.outfile.write('\\begin{appendix}\n' %title)
