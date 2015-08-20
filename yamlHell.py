import sys
sys.path.append('C:\\users\\jeremiah.marks\\Documents\\GitHub\\csvToolbox\\')
import csv
import ISServer_master as ISServer
import datetime

appname='ji237'
apikey='3a45a6f8c3bc261cf3d681c046f794ee'
filename='C:\Users\jeremiah.marks\Dropbox (JlMarks)\JlMarks Team Folder\\some.csv'
dateformatinfiles = "%B %d, %Y %H:%M"
desiredformat = "%Y-%m-%d %H:%M:%S"

thisserver = ISServer.ISServer(appname, apikey)

infile=open(filename)
thisreader = csv.DictReader(infile)
thesefields = thisreader.fieldnames

importcsv = []
for eachrow in thisreader:
	thisrecord={}
	originaltime='"'+str(datetime.datetime.strptime(eachrow['Written'], dateformatinfiles).strftime(desiredformat))+'"'
	thisrecord['CreationDate'] = originaltime
	thisrecord['CompletionDate'] = originaltime
	thisrecord['ActionType'] = eachrow['FActionType']
	thisrecord['ActionDescription'] = eachrow['Subject']
	thisrecord['CreationNotes'] = eachrow['Body']
	matching = thisserver.getMatchingRecords("Contact", {'Name': eachrow['Name']}, ['Id'])
	if len(matching)>0:
		thisrecord['ContactId'] = matching[0]
	else:
		thisrecord['ContactId'] = eachrow['Name']
	importcsv.append(thisrecord)
outfile = "C:\\users\\jeremiah.marks\\Desktop\\some2.csv"
with open(outfile, 'wb') as outfiles:
	thiswriter = csv.DictWriter(outfiles, importcsv[0].keys())
	thiswriter.writerows(importcsv)

