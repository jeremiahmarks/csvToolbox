#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-06-15 14:01:14
# @Last Modified by:   jeremiah.marks
# @Last Modified time: 2015-06-16 18:06:43
##
##  This file will open a file that has non-normal delimiters, and then save the file to
##  To a properly structured csv file.

import csv

pathtoinputfile='C:\\Users\\jeremiah.marks\\Desktop\\portable Python 2.7.6.1\\CONTHIST.txt'
centerfile='C:\\Users\\jeremiah.marks\\Desktop\\portable Python 2.7.6.1\\CONTHIST.txt.tmp'
pathtooutfile='C:\\Users\\jeremiah.marks\\Desktop\\portable Python 2.7.6.1\\CONTHIST.out.csv'

cellDelimiterInUse="|"
# This is what the file is currently using to seperate cells.
# Most times you would expect this be a comma


quotecharInUse='^'
# This is what the file is using to encapsulate the cells.


addendumcolumnname='outsideOfTables'
# This is a column that will be added to the file to handle
# data in columns without headings.

def removeInvalidChars(inputfile=pathtoinputfile, outputfilepath=centerfile):
    with open(inputfile) as originalfile:
        with open(outputfilepath, 'wb') as centfile:
            for eachline in originalfile:
                thisout=str(''.join([k for k in eachline if ord(k)<127 and ord(k)>10]))
                thisout.replace(quotecharInUse+cellDelimiterInUse, quotecharInUse+' '+cellDelimiterInUse).strip(" \n")
                thisout.replace(cellDelimiterInUse+quotecharInUse, cellDelimiterInUse+' '+quotecharInUse)
                if len(thisout)>0:
                    centfile.writelines(thisout+'\n')


def changedelims(inputfile=centerfile, outputfilepath=pathtooutfile):
    with open(inputfile) as originalfile:
        #This basically opens the file in read mode.
        inputreader=csv.DictReader(originalfile, delimiter=cellDelimiterInUse, quotechar=quotecharInUse, restkey=addendumcolumnname)
        # This takes the newly opened file and opens it with a dictionary reader.
        # Passing the various specific details needed to deal with this file.
        totalcolumns=inputreader.fieldnames + [addendumcolumnname]
        with open(outputfilepath, 'wb') as outputfile:
            # Here we open the output file in write mode.
            outputwriter=csv.DictWriter(outputfile, totalcolumns)
            # This assigns an DictWriter to the newly open file.
            #  When using an output writer, the file and the field names need to be passed on creation.
            #   you can see that we are adding a list cotaining the added column to the list of field names so that t
            # the writer expects it and does not freak out when it sees extra columns.
            outputwriter.writeheader()
            # This writes the header for the csv file
            for eachrow in inputreader:
                tempthing={}
                for eachcolumn in totalcolumns:
                    if eachcolumn in eachrow.keys() and len(eachrow[eachcolumn])>0:
                        tempthing[eachcolumn]=eachrow[eachcolumn]
                    else:
                        tempthing[eachcolumn]=""
                outputwriter.writerow(tempthing)


def changedelimsandchunk(inputfile=centerfile, outputfilepath=pathtooutfile):
    filecounter=1
    maxsize=15000000
    currentsize=0
    filename = lambda x: outputfilepath[:-4] + str(x) + outputfilepath[-4:]
    with open(inputfile) as originalfile:
        #This basically opens the file in read mode.
        inputreader=csv.DictReader(originalfile, delimiter=cellDelimiterInUse, quotechar=quotecharInUse, restkey=addendumcolumnname)
        # This takes the newly opened file and opens it with a dictionary reader.
        # Passing the various specific details needed to deal with this file.
        totalcolumns=inputreader.fieldnames+[addendumcolumnname, ]
        currentfile=open(filename(filecounter),'w+')
        currentwriter=csv.DictWriter(currentfile, totalcolumns)
        currentwriter.writeheader()
        currentsize=0
        print totalcolumns
        for eachrow in inputreader:
            thislength=0
            rowsub={}
            if addendumcolumnname not in eachrow.keys():
                rowsub[addendumcolumnname]=""
            for eachcolumn in totalcolumns:
                if eachcolumn not in eachrow.keys() or type(eachrow[eachcolumn]) == type(None):
                    rowsub[eachcolumn]=''
                else:
                    rowsub[eachcolumn]=eachrow[eachcolumn]
                thislength+=len(rowsub[eachcolumn])
            if maxsize-currentsize > thislength:
                currentsize+=thislength
                currentwriter.writerow(rowsub)
            else:
                currentfile.close()
                removeblanklines(filename(filecounter))
                filecounter+=1
                currentfile=open(filename(filecounter),'w+')
                currentwriter=csv.DictWriter(currentfile, totalcolumns)
                currentwriter.writeheader()
                currentsize=thislength
                currentwriter.writerow(rowsub)
    currentfile.close()

def removeblanklines():
    outputfilepath = 'C:\\Users\\jeremiah.marks\\Desktop\\portable Python 2.7.6.1\\CONTHIST.out.csv'
    filename = lambda x: outputfilepath[:-4] + str(x) + outputfilepath[-4:]
    for x in range(1,51):
        alllines=[]
        with open(filename(x)) as reading:
            for eachline in reading.readlines():
                if len(eachline)>3:
                    alllines.append(eachline)
        with open(filename(x), 'w+') as writing:
            writing.writelines(alllines)