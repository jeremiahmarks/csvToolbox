#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-21 20:43:10
# @Last Modified 2015-06-21>
# @Last Modified time: 2015-06-21 20:43:30
import csv

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
  allrowsbynumber={}
  thisfile=open(pathtofile)
  thisreader=unicode_csv_reader(thisfile)
  for eachrownumber, eachrow in enumerate(thisreader):
    if eachrownumber==0:
      headings=eachrow
    thisrowsheadings=headings[:]
    extracols=[]
    for eachheading in range(len(eachrow) - len(thisrowsheadings)):
      extracols.append(str(eachheading))
    thisrowdict={}
    for eachcolset in zip(thisrowsheadings + extracols, eachrow):
      thisrowdict[eachcolset[0]]=eachcolset[1]
    thisrowdict['extra']=[thisrowdict.pop(k) for k in thisrowdict.keys() if k in extracols]
    allrowsbynumber[eachrownumber]=thisrowdict
  return allrowsbynumber