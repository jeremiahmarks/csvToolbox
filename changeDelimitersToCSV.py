#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-06-15 14:01:14
# @Last Modified by:   jeremiah.marks
# @Last Modified time: 2015-06-15 14:33:08
##
##  This file will open a file that has non-normal delimiters, and then save the file to
##  To a properly structured csv file.

import csv

pathtoinputfile='C:\\User\\user.name\\file.txt'
pathtooutfile='C:\\User\\user.name\\fileout.csv'

cellDelimiterInUse="|"
# This is what the file is currently using to seperate cells.
# Most times you would expect this be a comma


quotecharInUse='^'
# This is what the file is using to encapsulate the cells.


addendumcolumnname='outsideOfTables'
# This is a column that will be added to the file to handle
# data in columns without headings.



with open(pathtoinputfile) as originalfile:
    #This basically opens the file in read mode.
    inputreader=csv.DictReader(originalfile, delimiter=cellDelimiterInUse, quotechar=quotecharInUse, restkey=addendumcolumnname)
    # This takes the newly opened file and opens it with a dictionary reader.
    # Passing the various specific details needed to deal with this file.
    with open(pathtooutfile, 'wb') as outputfile:
        # Here we open the output file in write mode.
        outputwriter=csv.DictWriter(outputfile, inputreader.fieldnames + [addendumcolumnname])
        # This assigns an DictWriter to the newly open file.
        #  When using an output writer, the file and the field names need to be passed on creation.
        #   you can see that we are adding a list cotaining the added column to the list of field names so that t
        # the writer expects it and does not freak out when it sees extra columns.
        outputwriter.writeheader()
        # This writes the header for the csv file
        for eachrow in inputreader:
            outputwriter.writerow(eachrow)