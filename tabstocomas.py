#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-07-07 00:52:21
# @Last Modified 2015-07-07
# @Last Modified time: 2015-07-07 02:46:01
import os
import csv
import glob
import codecs
import datetime


pathtoinfolder='/home/jlmarks/Dropbox (JlMarks)/imports/Working/hl247/originals/'
pathtomidlocation='/home/jlmarks/Dropbox (JlMarks)/imports/Working/hl247/stilltsv/'
pathtooutfolder='/home/jlmarks/Dropbox (JlMarks)/imports/Working/hl247/'

listofcsvfiles=glob.glob(pathtoinfolder+'*.csv')


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.DictReader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [{key: unicode(value, 'utf-8')} for key, value in row.iteritems()]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')




def decodeFilesFirst(listofcsvfiles = listofcsvfiles):
    for eachfile in listofcsvfiles:
        filename=os.path.basename(eachfile)
        with open(eachfile, 'rb') as infile:
            infiletext=infile.read()
            bom= codecs.BOM_UTF16_LE
            if infiletext.startswith(bom):
                infiletext= infiletext[len(bom):]                         #strip away the BOM
            decoded_text= infiletext.decode('utf-16le')
        with open(pathtomidlocation+filename, 'wb') as outfile:
            outfile.write(decoded_text)

def convertFromTabs(pathtofolder=pathtomidlocation):
    allfiles = glob.glob(pathtofolder + "*.csv")
    for eachfile in allfiles:
        filename=os.path.basename(eachfile)
        with open(eachfile, 'rb') as infile:
            thisreader = csv.DictReader(infile, delimiter='\t')
            alllines=[dict(zip(thisreader.fieldnames, thisreader.fieldnames)), ]
            for eachline in thisreader:
                alllines.append(eachline)
        with open(pathtooutfolder+filename, 'wb') as outfile:
            thiswriter=csv.writer(outfile)
            for eachline in alllines:
                thiswriter.writerow([eachline[k] for k in alllines[0].keys()])


def breakuofiles(pathtofolder = pathtooutfolder):
    folderpath = os.path.abspath(pathtofolder)
    allfiles = glob.glob(pathtofolder + os.path.sep + "*.csv")
    brokenfolder=folderpath + os.path.sep + "broken" + os.path.sep + datetime.datetime.now().strftime('%Y%m%d')
    for eachfile in allfiles:
        filename=os.path.basename(eachfile)[:-4]
        filebrokendir = brokenfolder + os.path.sep + filename
        with open(eachfile, 'rb') as infile:
            thisreader=csv.DictReader(infile)
            filewriters={}
            for eachheading in thisreader.fieldnames:
                filepath = filebrokendir + os.path.sep + eachheading + ".txt"
                if not os.path.exists(os.path.dirname(filepath)):
                    os.makedirs(os.path.dirname(filepath))
                filewriters[eachheading] = open(filepath, 'wb')
            for eachline in thisreader:
                for eachwritername in filewriters.keys():
                    if eachwritername in eachline.keys():
                        filewriters[eachwritername].write(str(eachline[eachwritername]) + '\n' + '-'*50 + '\n\n\n\n')
                    else:
                        filewriters[eachwritername].write('-'*50 +'\n\n\n\n')
            for eachfile in filewriters:
                filewriters[eachfile].close()
