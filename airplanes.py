#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-10-19 09:59:34
# @Last Modified 2015-10-19

import csv

owneroperatorfile='C:\\actCrap\\airplanes\\aircrafttoOwnOperator.csv'
owneroperatorfileout='C:\\actCrap\\airplanes\\aircrafttoOwnOperator2.csv'

contactdeetsfile = 'C:\\actCrap\\airplanes\\contactDeets.csv'
currentlyExisting = 'C:\\actCrap\\airplanes\\currentExport.csv'

finaloutputfile = 'C:\\actCrap\\airplanes\\importopportunitites.csv'

rowsforimport=[]

with open(owneroperatorfile, 'rb') as infile:
	thisreader =  csv.DictReader(infile)
	for eachrow in thisreader:
		owner = dict(eachrow)
		owner.pop('OperatorId')
		owner['conOrigId'] = owner.pop('OwnerId')
		owner['type']='Owner'
		operator = dict(eachrow)
		operator.pop('OwnerId')
		operator['type']='Operator'
		operator['conOrigId'] = operator.pop('OperatorId')
		rowsforimport.append(owner)
		rowsforimport.append(operator)

with open(owneroperatorfileout, 'wb') as outfile:
	thiswriter = csv.DictWriter(outfile, rowsforimport[0].keys())
	thiswriter.writeheader()
	thiswriter.writerows(rowsforimport)