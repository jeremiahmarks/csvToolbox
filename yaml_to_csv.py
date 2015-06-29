#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-28 15:43:34
# @Last Modified 2015-06-28
# @Last Modified time: 2015-06-28 21:17:00

############################################################
##  This script is designed to import a folder full of YAML
##  files into one, hopefully meaningful, csv.
##
############################################################

############################################################
## Notes on navigation:
##
## a=open(listoffiles[0], 'rb')
## b=yaml.safe_load(a)
## b[0]
## b[1]
## b[3].keys()
## b[3]['Email 220921797'].keys()
## b[3]['Email 220921797']
## b[3]['Email 220921797'][0].keys()
##
############################################################


import tablib
import yaml
import csv
import glob
import os
import pprint

pathtofolder = '/home/jlmarks/Desktop/HighriseKirsty/contacts/'
listoffiles = sorted(glob.glob(pathtofolder + "*.txt"))

contactsandnotes = {}

for eachfile in listoffiles:
    thiscontactname = os.path.basename(eachfile)[:-4]
    print thiscontactname
    with open(eachfile, 'rb') as contactsYAML:
        contactsandnotes[thiscontactname] = yaml.safe_load(contactsYAML)



convertedtoDicts=[]
for eachkey in sorted(contactsandnotes.keys()):
    thisdict={}
    thisdict['Contact Name']=eachkey
    for eachdict in contactsandnotes[eachkey]:
        for eachkey in eachdict:
            thisdict[eachkey] = eachdict[eachkey]
    convertedtoDicts.append(thisdict)

for eachthing in convertedtoDicts:
    thiscounter={}
    for eachkey in eachthing.keys():
        if type(eachthing[eachkey]) is type(list()):
            thisthing=eachkey.strip(' 1234567890')
            print thisthing
            if thisthing not in thiscounter.keys():
                thiscounter[thisthing]=0
            thiscounter[thisthing]+=1
            for eachitem in eachthing[eachkey]:
                if type(eachitem) is type(dict()):
                    for eachnewkey in eachitem.keys():
                        eachthing[thisthing+str('%03i' %thiscounter[thisthing])+"-"+eachnewkey]= eachitem.pop(eachnewkey)
            eachthing.pop(eachkey)

headings=set()
for eachthingthistime in convertedtoDicts:
    headings |= set(eachthingthistime.keys())


csvout='thisfile.csv'
outfile=open(csvout, 'wb')
theseheadings = sorted(list(headings))
thiswriter=csv.DictWriter(outfile, theseheadings)
thiswriter.writeheader()
for finalthing in convertedtoDicts:
    for eachheading in theseheadings:
        if eachheading not in finalthing.keys():
            finalthing[eachheading]=''
thiswriter.writerows(convertedtoDicts)
outfile.close()

outfile = open('thisout.txt', 'wb')
pp = pprint.PrettyPrinter(indent=4, stream=outfile)
pp.pprint(convertedtoDicts)
outfile.close()
