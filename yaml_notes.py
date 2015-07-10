#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-07-09 02:45:06
# @Last Modified 2015-07-09
# @Last Modified time: 2015-07-09 23:24:16

import yaml
import os
import glob
import datetime

names = {}

if os.sep == '/':
    DROPBOXPATH = '/home/jlmarks/Dropbox/JlMarks Team Folder/'
else:
    DROPBOXPATH = "C:\\Users\\Jeremiah.marks\\Dropbox (JlMarks)\\JlMarks Team Folder\\"
folderpath = os.path.abspath(DROPBOXPATH)

pathtoyaml = folderpath + os.sep + "contacts"
yamlfiles = sorted(glob.glob(pathtoyaml + os.sep + "*.txt"))
dateformatinfiles = "%B %d, %Y %H:%M"
desiredformat = "%Y-%m-%d %H:%M:%S"

listoffiles=[]
for eachfile in yamlfiles:
    listoffiles.append(yaml.safe_load(open(eachfile)))

for eachfile in listoffiles:
    if len(eachfile)>2:
        print eachfile[0]
        print eachfile[1].keys()
        print eachfile[2].keys(),'\n\n'

len(listoffiles)
allid=set()
for eachfile in listoffiles:
    allid.add(eachfile[0]['ID'])
len(allid)
honkingholder={}
for eachfile in listoffiles:
    honkingholder[eachfile[0]['ID']] = eachfile
a=json.dumps(honkingholder)
len(a)
outfile=open('/home/jlmarks/deleteFiles/__a.txt', 'wb')
outfile.write(a)
outfile.close()
import json
infile=open('/home/jlmarks/deleteFiles/__a.txt', 'rb')
a=json.loads(infile.read())

# Just a test to make sure Name is a key in the first dict
for each in a:
    if u'Name' not in a[each][0]:
        print each[0]

# This basically verifies that every first value contains
# a subset of the columns below. Basically if I prepare to 
# handle each of those cases, I will be good no matter what.
# First Layer keys:
flayerkeys=[u'Name', u'ID', u'Tags']
for each in a:
    if len(a[each][0].keys()) == 0:
        print each
    for eachd in a[each][0].keys():
        if eachd not in flayerkeys:
            print each, eachd

tocsv=[]
for eachfileid in a:
    for eachdict in a[eachfileid]:
        if a[eachfileid].index(eachdict) == 0:
            basevalues={}
            basevalues['FK'] = eachfileid
            for eachflayer in flayerkeys:
                if eachflayer in eachdict.keys():
                    basevalues[eachflayer] = eachdict[eachflayer]
                else:
                    basevalues[eachflayer] = ""
        else:
            thesevalues = dict(basevalues)
            for eachkey in eachdict.keys():
                thesevalues[eachkey] = eachdict[eachkey]
            tocsv.append(thesevalues)


# Basically, we determine that the keys with a 
kl=set()
for each in tocsv:
    for eachkey in [k for k in each.keys() if len(k.split(' ')) > 1]:
        kl.add(' '.join(eachkey.split(' ')[:-1]))
print kl

recsv=[]
totalkeys=set()
for each in tocsv:
    repl={}
    for eachkey in each.keys():
        splits=eachkey.split(' ')
        if len(splits) is 1:
            repl[eachkey] = each[eachkey]
        else:
            repl[u'FActionType'] = ' '.join(splits[:-1])
            repl[u'ActionFK'] = splits[-1]
            for eachdict in each[eachkey]:
                repl.update(eachdict)
    totalkeys |= set(repl.keys())
    recsv.append(repl)

for dicthere in recsv:
    for eachkey in totalkeys:
        if eachkey not in dicthere.keys():
            dicthere[eachkey] = ' '

import csv

tout='some.csv'
thiswriter=csv.DictWriter(open(tout, 'wb'), recsv[0].keys())
thiswriter.writeheader()
thiswriter.writerows(recsv)