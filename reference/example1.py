#!/usr/bin/env python

import sys
import random
import pytex

def main():
    # Initialize Document
    report = pytex.PyTexDocument('out.tex',
                                 'report',
                                  None,
                                  [['geometry', 'margin=1in'],
                                   ['times'],
                                   ['graphicx']
                                  ])
    # Set Title
    report.title('Reference Document One', 'Will Farmer')
    report.text('This is an example document used to show the features of PyTeX. As PyTeX offers more and more functionality, I will continue to add to this document as a showcase for its features.')
    report.text('Feel free to take and use this document with whatever projects you are currently working on. There is one restriction with this method of creating documents however, and that is the pdflatex dependency. Pdflatex is the compiler that is used to generate the end pdf from the raw tex file. If you do not have pdflatex installed (with the right packages) you will not be able to compile this document.')
    report.text('Below is a sample Table that has been generated in the code and included on the fly. Functionality is rather limited currently, however it is easily expanded upon')
    data_array = get_data() # Get array of data
    report.table(data_array) # Write a table
    report.write() # Write and close the document

def get_data():
    '''
    Generates an array of data to be tabled
    '''
    array = []
    for row in range(18):
        row = []
        for column in range(4):
            num_sum = 0
            for number in range(100):
                num_sum += random.randint(0, 1000)
            row.append(num_sum / 99.0)
        array.append(row)
    return array





if __name__ == "__main__":
    sys.exit(main())
