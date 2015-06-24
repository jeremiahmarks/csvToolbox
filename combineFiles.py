

import csv
import glob
import os
import json
pathToFiles = '/home/jlmarks/FXO/FXO-Salesforce-Export/'

listoffiles = sorted(glob.glob(pathToFiles + "*.csv"))


def mushFiles():
    honkinghugeholder = {}
    for eachfile in listoffiles:
        thisfilename = os.path.basename(eachfile)[:-4]
        with open(eachfile) as infile:
            thisreader = csv.DictReader(infile)
            for eachnewheading in [thisfilename + "." + k for k in thisreader.fieldnames]:
                honkinghugeholder[eachnewheading] = ''
    allrows = []
    for eachfile in listoffiles:
        thisfilename = os.path.basename(eachfile)[:-4]
        with open(eachfile) as infile:
            thisreader = csv.DictReader(infile)
            for eachrow in thisreader:
                thisdict = honkinghugeholder.copy()
                for eachvalue in eachrow.keys():
                    thisdict[
                        thisfilename + "." + eachvalue] = eachrow[eachvalue]
                allrows.append(thisdict)
    print "starting writingout"
    with open('alldatainone.csv', 'wb') as outfile:
        thiswriter = csv.DictWriter(outfile, sorted(honkinghugeholder.keys()))
        thiswriter.writeheader()
        thiswriter.writerows(allrows)
    print "done?"


def getallheadings():
    with open('allheadingsinone.txt', 'wb') as outfile:
        for eachfile in listoffiles:
            thisfilename = os.path.basename(eachfile)[:-4]
            with open(eachfile) as infile:
                outfile.write('"' + thisfilename + '",' + infile.readline())


def generateStats():
    honkinghugeholder = {}
    for eachfile in listoffiles:
        thisfilename = os.path.basename(eachfile)[:-4]
        honkinghugeholder[thisfilename] = {}
        with open(eachfile) as infile:
            thisreader = csv.DictReader(infile)
            honkinghugeholder[thisfilename][
                "headings"] = thisreader.fieldnames[:]
            honkinghugeholder[thisfilename]['numofrecords'] = 0
            for eachrow in thisreader:
                honkinghugeholder[thisfilename]['numofrecords'] += 1
                honkinghugeholder[thisfilename][honkinghugeholder[thisfilename]['numofrecords']] = dict(
                    zip(honkinghugeholder[thisfilename]["headings"], [eachrow[k] for k in honkinghugeholder[thisfilename]["headings"]]))
    colsneeded = max([len(honkinghugeholder[thisfilename]["headings"]) for thisfilename in honkinghugeholder.keys()])
    # colsneeded should now the number of columns in the file with the most columns.
    templatedictionary=dict([("c"+str(number), '') for number in range(colsneeded)])
    thesekeys=templatedictionary.keys()
    for eachkey in thesekeys:
        templatedictionary[eachkey+" tot"]=0
        templatedictionary[eachkey+" uni"]=0
    templatedictionary['filename']=''
    templatedictionary['numberofrecords']=0
    outrows=[]
    for eachfile in honkinghugeholder.keys():
        fileskeys=honkinghugeholder[eachfile]["headings"]
        thisDict=templatedictionary.copy()
        thisDict['filename']=eachfile
        thisDict['numberofrecords']=honkinghugeholder[eachfile]['numofrecords']
        # Generate stats
        statsbuilder={}
        for eachrow in honkinghugeholder[eachfile].keys():
            if eachrow in ['numofrecords', "headings"]:
                continue
            for eachkey in fileskeys:
                keyname='c' + str(fileskeys.index(eachkey))
                if keyname not in statsbuilder.keys():
                    statsbuilder[keyname]={}
                    statsbuilder[keyname]['all']=[]
                    statsbuilder[keyname]['uniq']=set()
                    thisDict[keyname] = eachkey
                statsbuilder[keyname]['all'].append(honkinghugeholder[eachfile][eachrow][eachkey])
                statsbuilder[keyname]['uniq'].add(honkinghugeholder[eachfile][eachrow][eachkey])
        for eachcolumnname in statsbuilder:
            thisDict[eachcolumnname+" tot"]=len([k for k in statsbuilder[eachcolumnname]['all'] if k and len(k)>0])
            thisDict[eachcolumnname + " uni"]=len(statsbuilder[eachcolumnname]['uniq'])
        outrows.append(thisDict)
    with open("datas.txt",'wb') as outfile:
        thiswriter = csv.DictWriter(outfile, sorted(templatedictionary.keys()))
        thiswriter.writeheader()
        thiswriter.writerows(outrows)
    with open("datas.txt") as inf:
        thisfile=inf.read()
        thisfile = thisfile.replace(',',' '*200+',')
        with open('datas.csv', 'wb') as outf:
                  outf.write(thisfile)