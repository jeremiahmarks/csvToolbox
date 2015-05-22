

import csv
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def removeSubstrings(inFile='hcsv.csv', outfile='aaa.csv'):
    aaa=["""This e-mail transmission, and any documents, files or previous e-mail messages attached to it may contain confidential information that is legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that any disclosure, copying, distribution or use of any of the information contained in or attached to this transmission is STRICTLY PROHIBITED.  If you have received this transmission in error, please immediately notify the sender. Please destroy the original transmission and its attachments without reading or saving in any manner.""","\n\n"]
    filecounter=0
    linecounter=0
    a=open(inFile,'rb')
    reader=csv.DictReader(a)
    columns=reader.fieldnames
    # create the output file
    outfileName='%i'%(filecounter) + outfile
    b=open(outfileName,'wb')
    writer=csv.DictWriter(b,reader.fieldnames)
    writer.writeheader()
    for eachline in reader:
        for eachCol in columns:
            if not (len(eachline[eachCol].replace(' ','\n'))>0):
                eachline[eachCol]="0"
            if(len(eachline[eachCol])>30000):
                for eachBadData in aaa:
                    eachline[eachCol]=eachline[eachCol].replace(eachBadData,'')
                eachline[eachCol] = strip_tags(eachline[eachCol])
        writer.writerow(eachline)
        linecounter+=1
        if linecounter>30000:
            b.close()
            filecounter+=1
            outfileName='%i'%(filecounter) + outfile
            b=open(outfileName,'wb')
            writer=csv.DictWriter(b,reader.fieldnames)
            writer.writeheader()
            linecounter=0
    a.close()




def splitFile(inFile='hcsv.csv', outfile='aaa.csv'):
    aaa=["""This e-mail transmission, and any documents, files or previous e-mail messages attached to it may contain confidential information that is legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that any disclosure, copying, distribution or use of any of the information contained in or attached to this transmission is STRICTLY PROHIBITED.  If you have received this transmission in error, please immediately notify the sender. Please destroy the original transmission and its attachments without reading or saving in any manner.""","\n\n"]
    filecounter=0
    linecounter=0
    a=open(inFile,'rb')
    reader=csv.DictReader(a)
    columns=reader.fieldnames
    # create the output file
    outfileName='%i'%(filecounter) + outfile
    b=open(outfileName,'wb')
    writer=csv.DictWriter(b,reader.fieldnames)
    writer.writeheader()
    for eachline in reader:
        for eachCol in columns:
            if not (len(eachline[eachCol].replace(' ',''))>0):
                eachline[eachCol]="0"
            for eachBadData in aaa:
                eachline[eachCol]=eachline[eachCol].replace(eachBadData,'')
        writer.writerow(eachline)
        linecounter+=1
        if linecounter>30000:
            b.close()
            filecounter+=1
            outfileName='%i'%(filecounter) + outfile
            b=open(outfileName,'wb')
            writer=csv.DictWriter(b,reader.fieldnames)
            writer.writeheader()
            linecounter=0
    a.close()


def fineLine(inFile='hcsv.csv', linenumber):
    filecounter=0
    linecounter=0
    a=open(inFile,'rb')
    reader=csv.DictReader(a)
    columns=reader.fieldnames
    # create the output file
    # outfileName='%i'%(filecounter) + outfile
    # b=open(outfileName,'wb')
    # writer=csv.DictWriter(b,reader.fieldnames)
    # writer.writeheader()
    for eachline in reader:
        if None in eachline.keys():
            eachline.pop(None,None)
        for eachCol in columns:
            if not (len(eachline[eachCol].replace(' ',''))>0):
                eachline[eachCol]="0"
        # writer.writerow(eachline)
        linecounter+=1
        if linecounter==linenumber:
            return eachline
    a.close()