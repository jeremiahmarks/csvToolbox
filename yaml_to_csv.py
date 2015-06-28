#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-28 15:43:34
# @Last Modified 2015-06-28
# @Last Modified time: 2015-06-28 15:59:06

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

pathtofolder = '/home/jlmarks/Desktop/HighriseKirsty/contacts/'

listoffiles = sorted(glob.glob(pathtofolder + "*.txt"))

contactsandnotes = {}

for eachfile in listoffiles:
    thiscontactname = os.path.basename(eachfile)[:-4]
    print thiscontactname
    with open(eachfile, 'rb') as contactsYAML:
        contactsandnotes[thiscontactname] = yaml.safe_load(contactsYAML)
