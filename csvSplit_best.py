import os
import csv
import Tkinter as tk
import tkFileDialog
tk.Tk().withdraw()


def getFilePath():
    return tkFileDialog.askopenfilename()


def getFolderPath():
    return tkFileDialog.askdirectory()


def main():
    filepath = getFilePath()
    filecounter=1
    maxsize = 9000000
    currentsize = 0
    basefilename = os.path.basename(filepath)
    basedirectory = os.path.dirname(filepath)
    filename = lambda x: filepath[:-4] + '%05d' %(x) + filepath[-4:]
    with open(filepath, 'rb') as infile:
        reader = csv.DictReader(infile)
        columns = reader.fieldnames
        currentfile = open(filename(filecounter),'w+')
        currentwriter = csv.DictWriter(currentfile, columns)
        currentwriter.writeheader()
        currentsize = 0
        for eachrow in reader:
            thislength=0
            rowsub={}
            for eachcolumn in columns:
                if eachcolumn not in eachrow.keys() or type(eachrow[eachcolumn]) == type(None):
                    rowsub[eachcolumn] = ''
                else:
                    rowsub[eachcolumn] = eachrow[eachcolumn]
                thislength +=len(rowsub[eachcolumn])
            if maxsize - currentsize > thislength:
                currentsize+=thislength
                currentwriter.writerow(rowsub)
            else:
                currentfile.close()
                removeblanklines(filename(filecounter))
                filecounter+=1
                currentfile=open(filename(filecounter),'w+')
                currentwriter=csv.DictWriter(currentfile, columns)
                currentwriter.writeheader()
                currentsize=thislength
                currentwriter.writerow(rowsub)
        removeblanklines(filename(filecounter))
    currentfile.close()




def removeblanklines(outputpath):
    outputfilepath = outputpath
    filename = lambda x: outputfilepath[:-4] + str(x) + outputfilepath[-4:]
    alllines=[]
    with open(outputpath) as reading:
        for eachline in reading.readlines():
            eachline=eachline.strip(' \n')
            if len(eachline)>3:
                alllines.append(eachline)
    with open(outputpath, 'w+') as writing:
        writing.writelines(alllines)
