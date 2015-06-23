

import csv
import glob
import os
pathToFiles='/home/jlmarks/FXO/FXO-Salesforce-Export/'

listoffiles=glob.glob(pathToFiles+"*.csv")
honkinghugeholder={}
for eachfile in listoffiles:
    thisfilename=os.path.basename(eachfile)[:-4]
    with open(eachfile) as infile:
        thisreader=csv.DictReader(infile)
        for eachnewheading in [thisfilename+"."+k for k in thisreader.fieldnames]:
            honkinghugeholder[eachnewheading]=''
allrows=[]
for eachfile in listoffiles:
    thisfilename=os.path.basename(eachfile)[:-4]
    with open(eachfile) as infile:
        thisreader=csv.DictReader(infile)
        for eachrow in thisreader:
            thisdict=honkinghugeholder.copy()
            for eachvalue in eachrow.keys():
                thisdict[thisfilename+"."+eachvalue]=eachrow[eachvalue]
            allrows.append(thisdict)
print "starting writingout"
with open('alldatainone.csv', 'wb') as outfile:
    thiswriter=csv.DictWriter(outfile, sorted(honkinghugeholder.keys()))
    thiswriter.writeheader()
    thiswriter.writerows(allrows)
print "done?"
