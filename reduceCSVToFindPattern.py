#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-06-15 17:46:35
# @Last Modified 2015-06-17
# @Last Modified time: 2015-06-17 04:35:26

# This script will open a csv file and go through it
# cell-by-cell, row-by-row and count the number of characters
# in each cell.  If the cell is empty, it will put a zero.
# If there is content in the cell, it will put a 1
#  This can then be opened in excel using conditional formatting
# to get a color coded, visual representation of where data is in the file.


import csv

infilename='products.csv'
outfilename='productsBin.csv'
def leavefieldnames():
    with open(infilename) as infile:
        reader=csv.DictReader(infile, restkey="valuesOutsideOfTable")
        with open(outfilename, 'wb') as outfile:
            writer=csv.DictWriter(outfile, reader.fieldnames + ["valuesOutsideOfTable"])
            writer.writeheader()
            for eachrow in reader:
                tempthing={}
                for eachcol in eachrow.keys():
                    if len(eachrow[eachcol])>0:
                        tempthing[eachcol]="1"
                    else:
                        tempthing[eachcol]="0"
                writer.writerow(tempthing)
def replacefieldnames():
    with open(infilename) as infile:
        reader=csv.DictReader(infile, restkey="valuesOutsideOfTable")
        allfields=reader.fieldnames + ["valuesOutsideOfTable"]
        for fieldloc, fieldname in enumerate(allfields):
            allfields[fieldloc]=fieldloc
        with open(outfilename, 'wb') as outfile:
            writer=csv.DictWriter(outfile, allfields, restval='0')
            writer.writeheader()
            for eachrow in reader:
                tempthing={}
                for eachloc, eachcol in enumerate(eachrow.keys()):
                    if len(eachrow[eachcol])>0:
                        tempthing[eachloc]="1"
                    else:
                        tempthing[eachloc]="0"
                writer.writerow(tempthing)

def checkrowtypes():
    import csv
    infilename='./droppings/products.csv'
    outfilename='./droppings/productsBin.csv'
    with open(infilename) as infile:
        reader=csv.DictReader(infile, restkey="valuesOutsideOfTable")
        allfields=reader.fieldnames + ["valuesOutsideOfTable"]
        fieldsasnums=allfields[:]
        for fieldloc, fieldname in enumerate(fieldsasnums):
            fieldsasnums[fieldloc]=fieldloc
        with open(outfilename, 'wb') as outfile:
            rowtypes=set() # This will be used to ensure that 
            # we keep track of unique sets. 
            filekeeper={} # This will hold various file process
            # that each rowtype will need.
            names=set()
            patternnames={}
            writer=csv.DictWriter(outfile, fieldsasnums, restval='0')
            writer.writeheader()
            ataglancefile=open('./droppings/ataglance.csv.txt', 'w+')
            filekeeper['ataglance']=ataglancefile
            writerkeeper={}
            for eachrow in reader:
                linenum=reader.line_num
                tempthing={}
                for eachloc, eachcol in enumerate(eachrow.keys()):
                    if len(eachrow[eachcol])>0:
                        tempthing[eachloc]="1"
                    else:
                        tempthing[eachloc]="0"
                if fieldsasnums[-1] not in tempthing.keys():
                    tempthing[fieldsasnums[-1]]="0"
                thisPattern=''.join([tempthing[k] for k in fieldsasnums])
                if thisPattern not in rowtypes:
                    rowtypes.add(thisPattern)
                    filekeeper[thisPattern]=open("./droppings/" + thisPattern + ".csv", 'wb')
                    thiswriter=csv.DictWriter(filekeeper[thisPattern], allfields, restval='0')
                    thiswriter.writeheader()
                    writerkeeper[thisPattern]=thiswriter
                    print "\nName this type of row: \n"
                    print eachrow
                    patternname=raw_input("Please use something like product, option, or contact\n").strip(" \n")
                    if patternname not in names:
                        names.add(patternname)
                        filekeeper[patternname]=open("./droppings/" + patternname + ".csv", 'wb')
                        thispatternwriter=csv.DictWriter(filekeeper[patternname], allfields, restval='0')
                        thispatternwriter.writeheader()
                        writerkeeper[patternname]=thispatternwriter
                    patternnames[thisPattern]=patternname
                writer.writerow(tempthing)
                writerkeeper[patternnames[thisPattern]].writerow(eachrow)
                writerkeeper[thisPattern].writerow(eachrow)
                ataglancefile.write(str(linenum) + "," + patternnames[thisPattern] + "," + thisPattern + "\n")
    return [k.close() for k in filekeeper.values()]


def expandcells():
    """This method will add whitespace to every cell until 
    every cell in the column is the same width. 
    """
    import csv
    infilename='./droppings/products.csv'
    outfilename='./droppings/productsBin.csv'
    fillchar=' '
    longestcell={}
    with open(infilename) as infile:
        reader=csv.DictReader(infile)
        for eachrow in reader:
            for eachcell in reader.fieldnames:
                celllength=len(eachcell)
                if eachcell not in longestcell.keys():
                    longestcell[eachcell]=celllength
                if celllength > longestcell[eachcell]:
                    longestcell[eachcell]=celllength
    with open(infilename) as infile:
        reader=csv.DictReader(infile)
        with open(outfilename, 'wb') as outfile:
            thesefieldnames=reader.fieldnames
            for nameloc, afieldname in enumerate(thesefieldnames):
                offset=longestcell[afieldname]
                thesefieldnames[nameloc]=thesefieldnames[nameloc].ljust(offset)
            writer=csv.DictWriter(outfile, thesefieldnames)
            writer.writeheader()
            for eachline in reader:
                thisline={}
                for eachfname in thesefieldnames:
                    thisline[eachfname]=eachline[eachfname.strip(' ')]
                writer.writerow(thisline)






