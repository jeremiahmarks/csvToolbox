#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-06-15 17:46:35
# @Last Modified 2015-06-15
# @Last Modified time: 2015-06-15 19:27:35

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
            writer=csv.DictWriter(outfile, allfields)
            writer.writeheader()
            for eachrow in reader:
                tempthing={}
                for eachloc, eachcol in enumerate(eachrow.keys()):
                    if len(eachrow[eachcol])>0:
                        tempthing[eachloc]="1"
                    else:
                        tempthing[eachloc]="0"
                writer.writerow(tempthing)