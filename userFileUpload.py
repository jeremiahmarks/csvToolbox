# This script is intended for customers to use on their 
# machines to upload files to the infusionsoft filebox.

import xmlrpclib
import csv
import base64

from Tkinter import *
import tkFileDialog
import glob
import os

def getFilePath():
    return tkFileDialog.askopenfilename()


def getFolderPath():
    return tkFileDialog.askdirectory()

class infusionsoftConnection:
    """This will be the whole class that we will use to update
    files.
    """
    def __init__(self, parent):
        self.missingcontactid=[]
        self.parent = parent
        self.filefolders = []

        self.dataframe = Frame(self.parent)
        self.dataframe.grid(column = 0, sticky=E+W)

        self.appnamelabel = Label(self.dataframe, text="Appname")
        self.appnamelabel.grid(row=0, sticky=W)
        
        self.apikeylabel = Label(self.dataframe, text="Apikey")
        self.apikeylabel.grid(row=1, sticky=W)

        self.appnameentry = Entry(self.dataframe)
        self.appnameentry.grid(row = 0, column=1)

        self.apikeyentry = Entry(self.dataframe)
        self.apikeyentry.grid(row=1, column=1)

        self.setvarsbutton = Button(self.dataframe, text="Update app", command = self.updateappname, width=30)
        self.setfolder1 = Button(self.dataframe, text="Add a folder", command = self.setfirstfolder, width = 30)
        self.setmappingbutton = Button(self.dataframe, text = "Set mapping CSV", command = self.setmappingcsv, width=30)
        self.starteverything = Button(self.dataframe, text = "Upload that stuff!", command = self.process, width=30)

        self.setvarsbutton.grid()
        self.setfolder1.grid()
        self.setmappingbutton.grid()
        self.starteverything.grid()
    def updateappname(self):
        self.appname = self.appnameentry.get()
        self.apikey = self.apikeyentry.get()
        self.connection = xmlrpclib.ServerProxy("https://" + self.appname + ".infusionsoft.com:443/api/xmlrpc")

    def setfirstfolder(self):
        self.filefolders.append(getFolderPath())

    def setmappingcsv(self):
        self.mappingcsv = getFilePath()
    def process(self):
        self.dlcontacts()
        self.potentialfiles=[]
        self.filenametopath={}
        for eachfolder in self.filefolders:
            self.potentialfiles += list(glob.glob(os.path.join(eachfolder, '*')))
        for eachfile in potentialfiles:
            thisfilename = os.path.basename(eachfile)
            self.filenametopath[thisfilename] = eachfile
        try:
            with open(self.mappingcsv, 'rb') as infile:
                thisreader = csv.DictReader(infile)
                for eachline in thisreader:
                    print eachline
                    fkid = eachline['AccountId']
                    filename = eachline['Name']
                    if fkid in self.fkidtocid.keys():
                        self.connection.FileService.uploadFile(self.apikey, self.fkidtocid[fkid], filename, base64.b64encode(open(self.filenametopath[eachrow['Id']])))
                    else:
                        self.missingcontactid.append(eachline)
        except Exception, e:
            print e
            raise
        finally:
            if len(self.missingcontactid) > 0:
                with open(os.path.join(os.path.expanduser('~'), 'fileuploaderrs.csv'), 'wb') as outfile:
                    thiswriter = csv.DictWriter(outfile, self.missingcontactid[0].keys())
                    thiswriter.writeheader()
                    thiswriter.writerows(self.missingcontactid)

    def dlcontacts(self):
        interestingdata = ['Id', '_AccountId']
        searchcriteria = {'_AccountId': '%'}
        orderedby = interestingdata[0]
        records = []
        self.fkidtocid={}
        p = 0
        while True:
            listofdicts = \
                self.connection.DataService.query(self.apikey,
                                                  'Contact',
                                                  1000,
                                                  p,
                                                  searchcriteria,
                                                  interestingdata,
                                                  orderedby,
                                                  True)
            for each in listofdicts:
                thisrecord = {}
                for eachbit in interestingdata:   # this should be
                    # records.append(zip(interestingdata, each)) perhaps
                    if eachbit not in each:   # TODO: research THIS
                        each[eachbit] = None
                    thisrecord[eachbit] = each[eachbit]
                records.append(thisrecord)
            if not(len(listofdicts) == 1000):
                break
            p += 1
        for eachrecord in records:
            if eachrecord['_AccountId'] not in self.fkidtocid.keys():
                self.fkidtocid[eachrecord['_AccountId']] = eachrecord['Id']
            else:
                print eachrecord['_AccountId'] + "Already exists."


root = Tk()
menubar = Menu(root)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
# display the menu
root.config(menu=menubar)

myapp = infusionsoftConnection(root)
root.mainloop()