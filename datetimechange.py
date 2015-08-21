import datetime
import csv

pathtofile='C:\\users\\jeremiah.marks\\Desktop\\calls (3).csv'
pathtofileout='C:\\users\\jeremiah.marks\\Desktop\\callsThree.csv'
formatin = '%d/%m/%Y %H:%M'
formatout = '%m/%d/%Y %H:%M'

fuckedFields=[ "Start Date and Time","Date End"]

with open(pathtofile, 'rb') as currentfile:
    rdr=csv.DictReader(currentfile)
    with open(pathtofileout, 'wb') as outfile:
        wtr = csv.DictWriter(outfile, rdr.fieldnames)
        wtr.writeheader()
        for eachrow in rdr:
            thisrow={}
            for eachcolname in eachrow:
                if eachcolname in fuckedFields:
                    thisrow[eachcolname] = datetime.datetime.strptime(eachrow[eachcolname], formatin).strftime(formatout)
                else:
                    thisrow[eachcolname] = eachrow[eachcolname]
            wtr.writerow(thisrow)

