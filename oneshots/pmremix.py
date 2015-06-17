#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-16 19:14:15
# @Last Modified 2015-06-16
# @Last Modified time: 2015-06-16 19:23:48
#
#
# Now with more concise!
#
import csv
import random
import simpleIS
import productObjects
import temphousing

temhousingqueue=temphousing.temhousingqueue

try:
    from my_pw  import passwords
except:
    collectcredentials()


def processproductsfile(pathtoproductfile=passwords['inputfilepath']):
    global temhousingqueue
    """This method will open a the specified file.
    This method expects the file to be in a very particular format.
    """
    with open(pathtoproductfile) as inputfile:
        thisreader=csv.DictReader(inputfile)
        thisproduct=None
        for rownum, eachrow in enumerate(thisreader):
            if len(eachrow["Product Images"]) > 0 and len(eachrow["Product Condition"])>0 and eachrow["Name"] and len(eachrow["Name"].strip(' \n')) > 0:
                thisproduct=temphousing.temphousing(eachrow)
            elif len(eachrow["Meta Description"])==0  and len(eachrow["Price"])==0 and eachrow["Name"] and eachrow["Name"][0]=='[':
                thisproduct.addoptionsrow(eachrow, rownum)
            elif eachrow["Price"] and eachrow["Price"][0]=='[':
                thisproduct.addpricingrulerow(eachrow, rownum)
            else:
                print "I must have missed something on line " + str(rownum)
    return temhousingqueue