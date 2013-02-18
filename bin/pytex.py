#!/usr/bin/env python
'''
LaTeX API
William Farmer
2013
'''

class PyTexDocument:
    '''
    LaTeX API Document Class Object
    '''

    def __init__(self):
        '''
        Defines the file to work on
        '''
        self.name = 'out.tex'
        self.outfile = open(self.name, mode='w')

    def doc_type(self, doc_class='report', options=['10pt']):
        '''
        Initializes the document with given options
        '''
        self.outfile.write('\\begin[')
        for number in range(len(options) - 2):
            self.outfile.write('%s, ' %options[number])
        self.outfile.write('%s]{%s}\n' %(options[len(options) - 1], doc_class))



