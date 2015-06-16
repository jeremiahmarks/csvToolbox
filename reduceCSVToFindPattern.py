#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-06-15 17:46:35
# @Last Modified by:   jeremiah.marks
# @Last Modified time: 2015-06-15 17:52:51

import csv

infilename='products.csv'
outfilename='productsBin.csv'

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