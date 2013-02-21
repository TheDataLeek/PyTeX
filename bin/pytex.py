#!/usr/bin/env python
"""
LaTeX API
William Farmer
2013
"""

import os
import re


def raw_latex(latex, content):
    '''
    Allows the user to write raw LaTeX to the document
    :param latex:
    :param content:
    '''
    content += latex


def picture(filename, content, scale=0.5, label=None, caption=None):
    '''
    Insert a picture. Needs to be png
    :param filename:
    :param content:
    :param scale:
    :param label:
    :param caption:
    '''
    content += ('\\begin{figure}[ht]\n' +
                '\\centering\n' +
                '\\includegraphics[scale=%f]{%s}\n' % (scale, filename))
    if label:
        content += '\\label{fig:%s}\n' % label
    if caption:
        content += '\\caption{%s}\n' % caption
    content += '\\end{figure}\n'


def table(array, content):
    '''
    Writes a table
    :param array:
    :param content:
    '''
    size = len(array[0])
    content += ('\\begin{tabular}{l%s}\n' % ((size - 1) * ' | l'))
    for entry in array:
        formatted_array = detect_math(entry)
        content += (str(formatted_array[0]))
        for number in range(1, len(formatted_array)):
            content += (' & %s' % (formatted_array[number]))
        content += ('\\\\\n')
    content += ('\\end{tabular}\n')


def math(math, content, newline=False):
    '''
    Inserts inline math. Math must be in LaTeX form.
    :param math:
    :param content:
    :param newline:
    '''
    if newline:
        content += ('\\[\n')
        content += ('\\begin{aligned}\n')
        raw_latex(math)
        content += ('\\end{aligned}\n')
        content += ('\\]\n')
    else:
        content += ('$ %s $' % math)


def detect_math(entry):
    '''
    When given a list of strings, it detects any math bits and returns.
    :param entry:
    '''
    formatted_list = []
    for item in entry:
        if re.search('[0-9\+\-\=\*\^]', str(item)):
            formatted_list.append('$%s$' % item)
        else:
            formatted_list.append(item)
    return formatted_list


def equation(latex_math, content, label=None):
    '''
    Insert a new equation. Equation must be in LaTeX Form.
    :param latex_math:
    :param content:
    :param label:
    '''
    if label:
        label.replace(' ', '')
        content += ('\\begin{equation}\\label{eq:%s}\n' % label)
    else:
        content += ('\\begin{equation}\n')
    content += ('\\begin{aligned}\n')
    raw_latex(latex_math)
    content += ('\\end{aligned}\n')
    content += ('\\end{equation}\n')


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
        self.contents     = ''
        self.sections = []
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
        self.content += ('\\title{%s}\n\\author{%s}\n\\date{%s}\n\\maketitle\n' % (title, author, date))

    def write(self):
        '''
        End the document, close the file, and compile the pdf
        '''
        self.outfile.write(self.contents)
        for item in self.sections:
            self.outfile.write(item.contents)
        self.outfile.write('\\end{document}')
        self.outfile.close()
        os.system('pdflatex --shell-escape %s' % self.name)

    def create_section(self, title=None, numbered=True):
        '''
        Adds a new section to the document.
        :param title:
        :param numbered:
        '''
        self.sections.append(PyTexDocument.Section(title, numbered))

    def add_section(self, section_object):
        '''
        Adds a section to the list
        :param section_object:
        '''
        self.sections.append(section_object)

    class Section(PyTexDocument):
        '''
        Creates a new section
        '''

        def __init__(self, title=None, numbered=True):
            '''
            Initializes Class for usage
            :param title:
            :param numbered:
            '''
            self.contents    = ''
            self.subsections = []
            if numbered:
                sec = ''
            else:
                sec = '*'
            self.contents += ('\\section%s{%s}\n' % (title, sec))
