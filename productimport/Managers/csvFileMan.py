#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-06-22 12:15:57
# @Last Modified 2015-06-22>
# @Last Modified time: 2015-06-22 19:43:24
import csv
from productimport import my_pw as pw

############################################################
##                                                         #
##    This is a work around to deal with csv files that use#
##      unicode chars.                                     #
##                                                         #
############################################################


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def getAllLinesAsDict(pathtofile):
    """This method will read a unicode csv file and return a
    dictionary containing the line numbers as keys and a
    dictionary relating the fieldnames to the contents of the
    line.
    """
    allrowsbynumber = {}
    thisfile = open(pathtofile)
    thisreader = unicode_csv_reader(thisfile)
    for eachrownumber, eachrow in enumerate(thisreader):
        if eachrownumber == 0:
            headings = eachrow
        thisrowsheadings = headings[:]
        extracols = []
        for eachheading in range(len(eachrow) - len(thisrowsheadings)):
            extracols.append(str(eachheading))
        thisrowdict = {}
        for eachcolset in zip(thisrowsheadings + extracols, eachrow):
            thisrowdict[eachcolset[0]] = eachcolset[1]
        thisrowdict['extra'] = [thisrowdict.pop(k) for k in
                                thisrowdict.keys() if k in extracols]
        allrowsbynumber[eachrownumber] = thisrowdict
    return allrowsbynumber


class csvFile(object):

    def __init__(self, pathtofile):
        self.rowCounter = 0
        self.rows = getAllLinesAsDict(pathtofile)
        self.readerfieldnames = self.rows[0]
        self.parserows()

    def getrowtype(self, row):
        if len(row["Name"]) is 0:
            return "SkuPricing"
        elif (row["Name"][0] != "["):
            return "Product"
        elif (len(row["SKU"]) == 0) or len(row["Price"]) > 0:
            return "PricingRule"
        else:
            return "Option"

    def parserows(self):
        self.rowsbytype = {}
        for eachline in self.rows.keys():
            if len(self.rows[eachline]) > 1:
                linetype = self.getrowtype(self.rows[eachline])
                if linetype not in self.rowsbytype.keys():
                    self.rowsbytype[linetype] = []
                self.rowsbytype[linetype].append(eachline)

    def getNextLine(self):
        self.rowCounter += 1

        if self.rowCounter in self.rowsbytype["Product"]:
            thisrowtyle = "Product"
        elif self.rowCounter in self.rowsbytype["SkuPricing"]:
            thisrowtyle = "SkuPricing"
        elif self.rowCounter in self.rowsbytype["PricingRule"]:
            thisrowtyle = "PricingRule"
        elif self.rowCounter in self.rowsbytype["Option"]:
            thisrowtyle = "Option"
        else:
            thisrowtyle = "Unknown"

        return [thisrowtyle, self.rows[self.rowCounter]]

    def __iter__(self):
        return self

    def next(self):
        if self.rowCounter >= len(self.rows.keys())-1:
            raise StopIteration
        else:
            self.rowCounter += 1
            if self.rowCounter in self.rowsbytype["Product"]:
                thisrowtyle = "Product"
            elif self.rowCounter in self.rowsbytype["SkuPricing"]:
                thisrowtyle = "SkuPricing"
            elif self.rowCounter in self.rowsbytype["PricingRule"]:
                thisrowtyle = "PricingRule"
            elif self.rowCounter in self.rowsbytype["Option"]:
                thisrowtyle = "Option"
            else:
                thisrowtyle = "Unknown"
            return [thisrowtyle, self.rows[self.rowCounter]]
