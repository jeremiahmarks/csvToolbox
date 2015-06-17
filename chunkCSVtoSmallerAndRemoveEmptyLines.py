#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-06-17 09:13:38
# @Last Modified by:   jeremiah.marks
# @Last Modified time: 2015-06-17 09:13:44

import csv
pathtooutfile="C:\\Users\\jeremiah.marks\\Desktop\\Research\\om111Chunked.csv"
centerfile="C:\\Users\\jeremiah.marks\\Desktop\\Research\\om111onlyaffecteddomains.csv"
def chunkdown(inputfile=centerfile, outputfilepath=pathtooutfile):
    filecounter=1
    maxsize=5000000
    currentsize=0
    filename = lambda x: outputfilepath[:-4] + str(x) + outputfilepath[-4:]
    with open(inputfile) as originalfile:
        #This basically opens the file in read mode.
        inputreader=csv.DictReader(originalfile)
        # This takes the newly opened file and opens it with a dictionary reader.
        # Passing the various specific details needed to deal with this file.
        totalcolumns=inputreader.fieldnames
        currentfile=open(filename(filecounter),'w+')
        currentwriter=csv.DictWriter(currentfile, totalcolumns)
        currentwriter.writeheader()
        currentsize=0
        print totalcolumns
        for eachrow in inputreader:
            thislength=0
            rowsub={}
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

def removeblanklines(outputpath):
    outputfilepath = outputpath
    filename = lambda x: outputfilepath[:-4] + str(x) + outputfilepath[-4:]
    alllines=[]
    with open(outputpath) as reading:
        for eachline in reading.readlines():
            eachline=eachline.strip(' \n')
            if len(eachline)>3:
                alllines.append(eachline)
    with open(outputpath, 'w+') as writing:
        writing.writelines(alllines)