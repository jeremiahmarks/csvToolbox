#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-10-26 17:37:07
# @Last Modified 2015-10-26 @Last Modified time: 2015-10-26 17:37:07


a=fullexport.fullexporter('ro130')
a.svr.verifyconnection()
neededtables=['CreditCard', 'Contact', 'Product', 'CProgram']
import os
bpath = 'C:\\actCrap\\ro130\\'
import csv
for eachtable in neededtables:
    theserecords = a.svr.getallrecords(eachtable)
    with open(os.path.join(bpath, eachtable+".csv"), 'wb') as outfile:
        thiswriter = csv.DictWriter(outfile, theserecords[0].keys())
        thiswriter.writeheader()
        thiswriter.writerows(theserecords)
