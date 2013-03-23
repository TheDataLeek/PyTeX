#!/usr/bin/env python
"""
LaTeX API
William Farmer
2013
"""

import os
import re


def raw_latex(latex, content):
    """
    Allows the user to write raw LaTeX to the document
    :param latex:
    :param content:
    """
    content += latex
    return content


def insert_text(text, content):
    '''
    Takes given text and appends it.
    '''
    formatted_list = detect_math(text.split(' '))
    string = ' '.join(formatted_list)
    content += string
    return content


def picture(filename, content, scale=0.5, label=None, caption=None):
    """
    Insert a picture. Needs to be png
    :param filename:
    :param content:
    :param scale:
    :param label:
    :param caption:
    """
    content += ('\\begin{figure}[ht]\n' +
                '\\centering\n' +
                '\\includegraphics[scale=%f]{%s}\n' % (scale, filename))
    if label:
        content += '\\label{fig:%s}\n' % label
    if caption:
        content += '\\caption{%s}\n' % caption
    content += '\\end{figure}\n'
    return content


def table(array, content):
    """
    Writes a table
    :param array:
    :param content:
    """
    size = len(array[0])
    content += ('\\begin{tabular}{l%s}\n' % ((size - 1) * ' | l'))
    for entry in array:
        formatted_array = detect_math(entry)
        content += (str(formatted_array[0]))
        for number in range(1, len(formatted_array)):
            content += (' & %s' % (formatted_array[number]))
        content += ('\\\\\n')
    content += ('\\end{tabular}\n')
    return content


def math(math, content, newline=False):
    """
    Inserts inline math. Math must be in LaTeX form.
    :param math:
    :param content:
    :param newline:
    """
    if newline:
        content += ('\\[\n')
        content += ('\\begin{aligned}\n')
        raw_latex(math)
        content += ('\\end{aligned}\n')
        content += ('\\]\n')
    else:
        content += ('$ %s $' % math)
    return content


def detect_math(entry):
    """
    When given a list of strings, it detects any math bits and returns.
    :param entry:
    """
    formatted_list = []
    for item in entry:
        if re.search('[0-9\+\-\=\*\^]', str(item)):
            formatted_list.append('$%s$' % item)
        else:
            formatted_list.append(item)
    return formatted_list


def equation(latex_math, content, label=None):
    """
    Insert a new equation. Equation must be in LaTeX Form.
    :param latex_math:
    :param content:
    :param label:
    """
    if label:
        label.replace(' ', '')
        content += ('\\begin{equation}\\label{eq:%s}\n' % label)
    else:
        content += ('\\begin{equation}\n')
    content += ('\\begin{aligned}\n')
    content += latex_math + '\n'
    content += ('\\end{aligned}\n')
    content += ('\\end{equation}\n')
    return content


class PyTexDocument:
    """
    LaTeX API Document Class Object
    """

    def __init__(self, name='out.tex', doc_class='report', options=None, packages=None):
        """
        Defines the file to work on as well as options
        :param name:
        :param doc_class:
        :param options:
        :param packages:
        """
        self.file_count = 0
        self.content    = ''
        self.sections   = []
        if not packages:
            packages  = [['geometry', 'margin=1in']]
        if not options:
            options   = ['10pt']
        self.name     = name

        self.content += '\\documentclass['
        for number in range(len(options) - 2):
            self.content += '%s, ' % options[number]
        self.content += '%s]{%s}\n' % (options[len(options) - 1], doc_class)

        for item in packages:
            try:
                self.content += '\\usepackage[%s]{%s}\n' % (item[1], item[0])
            except IndexError:
                self.content += '\\usepackage{%s}\n' % item[0]
        self.content += '\\begin{document}\n'

    def title(self, title='Insert Title Here', author='Insert Name Here', date='\\today'):
        """
        Define and make the title
        :param title:
        :param author:
        :param date:
        """
        self.content += ('\\title{%s}\n\\author{%s}\n\\date{%s}\n\\maketitle\n' % (title, author, date))

    def write(self, compile=False):
        """
        End the document, close the file, and compile the pdf
        """
        self.content += '\n\\end{document}'
        outfile = open(self.name, mode='w')
        outfile.write(self.content)
        if compile:
            os.system('pdflatex --shell-escape %s' % self.name)

    def raw_latex(self, latex):
        """
        Adds raw LaTeX code
        :param latex:
        """
        self.content = raw_latex(latex, self.content)

    def picture(self, filename, scale=0.5, label=None, caption=None):
        '''
        Adds a picture
        :param filename:
        :param scale:
        :param label:
        :param caption:
        '''
        self.content = picture(filename, self.content, scale, label, caption)

    def table(self, array):
        '''
        Adds a table
        :param array:
        '''
        self.content = table(array, self.content)

    def math(self, user_math, newline=False):
        '''
        Adds inline or basic math
        :param newline:
        '''
        self.content = math(user_math, self.content, newline)

    def latex(self, user_tex):
        '''
        Adds user LaTeX code to document
        '''
        self.content = raw_latex(user_tex, self.content)

    def equation(self, math, label=None):
        '''
        Adds an official equation
        :param math:
        :param label:
        '''
        self.content = equation(math, self.content, label)

    def text(self, user_text):
        '''
        Adds user content to the file.
        By nature this will be a new paragraph.
        '''
        self.content = insert_text(user_text, self.content)

    def section(self, title, numbered=True):
        '''
        Creates a new section with given title
        '''
        new_section = Section(title, numbered, self.file_count)
        self.sections.append(new_section)
        self.content += '\\input{%s}\n' %('section_%s.tex' %self.file_count)
        self.file_count += 1
        return new_section


class Section:
    '''
    Section class
    '''

    def __init__(self, title, numbered, name):
        if numbered:
            star = ''
        else:
            star = '*'
        self.new_section = open('section%i.tex' %name, 'w')
        name            += 1
        self.content     = '\section%s{%s}\n' %(star, title)

    def write(self):
        """
        Write the section and close file
        """
        self.new_section.write(self.content)
        self.new_section.close()

    def raw_latex(self, latex):
        """
        Adds raw LaTeX code
        :param latex:
        """
        self.content = raw_latex(latex, self.content)

    def picture(self, filename, scale=0.5, label=None, caption=None):
        '''
        Adds a picture
        :param filename:
        :param scale:
        :param label:
        :param caption:
        '''
        self.content = picture(filename, self.content, scale, label, caption)

    def table(self, array):
        '''
        Adds a table
        :param array:
        '''
        self.content = table(array, self.content)

    def math(self, math, newline=False):
        '''
        Adds inline or basic math
        :param newline:
        '''
        self.content = math(math, self.content, newline)

    def equation(self, math, label=None):
        '''
        Adds an official equation
        :param math:
        :param label:
        '''
        self.content = equation(math, self.content, label)
