#!/usr/bin/env python
'''
LaTeX API
William Farmer
2013
'''

import subprocess

class PyTexDocument(doc_class='report', options=['10pt'], packages=[['geometry', 'margin=1in']]):
    '''
    LaTeX API Document Class Object
    '''

    def __init__(self):
        '''
        Defines the file to work on as well as options
        '''
        self.name = 'out.tex'
        self.outfile = open(self.name, mode='w')

        self.outfile.write('\\begin[')
        for number in range(len(options) - 2):
            self.outfile.write('%s, ' %options[number])
        self.outfile.write('%s]{%s}\n' %(options[len(options) - 1], doc_class))

        for array in packages:
            for item in array:
                if item[1]:
                    self.outfile.wite('\\usepackage[%s]{%s}\n' %(item[1], item[0]))
                else:
                    self.outfile.wite('\\usepackage{%s}\n' %item[0])
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
        self.outfile.close()
        subprocess.Popen('pdflatex')

