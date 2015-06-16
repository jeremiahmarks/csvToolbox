#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-06-15 15:25:32
# @Last Modified by:   jeremiah.marks
# @Last Modified time: 2015-06-15 18:13:50

import csv

filepath="products.csv"

with open(filepath) as productsFile:
    thisReader=csv.DictReader(filepath, restkey="valuesOutsideOfTable")
    for eachrow in thisReader:
        if len(eachrow["GPS Enabled"])>0:
            #This will indicate that this is a product that we are dealing with.
            pass
        else:
            #If it is not a product, then it is some form of an option row.