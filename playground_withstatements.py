#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jlmarks
# @Date:   2015-10-25 12:22:34
# @Last Modified 2015-10-25
# @Last Modified time: 2015-10-25 12:29:02
import csv

class CSVThing:
    def __init__(self, pathtofile):
        self.pathtofile=pathtofile
    def __enter__(self):
        self.openfile = open(self.pathtofile, 'rb')
        self.reader=csv.DictReader(self.openfile)
        return self.reader
    def __exit__(self, type, value, traceback):
        self.openfile.close()

with CSVThing('/home/jlmarks/actually.csv') as thisfile:
    for eachline in thisfile:
        print eachline
