#!/usr/bin/env python
'''
LaTeX API
William Farmer
2013
'''

import subprocess

class PyTexDocument:
    '''
    LaTeX API Document Class Object
    '''

    def __init__(self, name='out.tex', doc_class='report', options=['10pt'], packages=[['geometry', 'margin=1in']]):
        '''
        Defines the file to work on as well as options
        '''
        self.name = name
        self.outfile = open(self.name, mode='w')

        self.outfile.write('\\begin[')
        for number in range(len(options) - 2):
            self.outfile.write('%s, ' %options[number])
        self.outfile.write('%s]{%s}\n' %(options[len(options) - 1], doc_class))

        for item in packages:
            try:
                self.outfile.write('\\usepackage[%s]{%s}\n' %(item[1], item[0]))
            except IndexError:
                self.outfile.write('\\usepackage{%s}\n' %item[0])
        self.outfile.write('\\begin{document}\n')

    def title(self, title='Insert Title Here', author='Insert Name Here', date='\\date'):
        '''
        Define and make the title
        '''
        self.outfile.write('''\\title{%s}\n
                            \\author{%s}\n
                            \\date{%s}\n
                            \\maketitle\n'''
                            %(title, author, date))

    def write(self):
        self.outfile.write('\\end{document}')
        self.outfile.close()
        subprocess.Popen('pdflatex')

