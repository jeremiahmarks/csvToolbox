#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jlmarks
# @Date:   2015-10-19 07:10:30
# @Last Modified 2015-10-20
# @Last Modified time: 2015-10-20 00:26:15

# large file split and import.

############################################################
## General approach to the problem of import large files.
# Prompt user for appname and apikey
# get list of custom fields
# prompt user for custom field used as FKID
#     provide ability to make a new custom field if so desired
# download all contacts and companies to csv + sqllite - keep Id and FKID as keys
# prompt user for csv file to import
# prompt user to determine which column is the fkid in csv
# copy the large file to smaller files along the way:
#     add the infusionsoftid columns, as needed
#     collect stats on columns and cells
# prompt user to match columns
# allow user to merge values for dropdown type
# Create custom fields as needed
# import files
# match values
# log everything
# rinse and repeat

import Tkinter as tk
import tkSimpleDialog
import os
import xmlrpclib
import csv
import datetime

import ISServer_master as ISServer

class setupdialog(tkSimpleDialog.Dialog):
    """Taking advantage of the tkSimpleDialog
    """
    def body(self, master):
        self.removehtml=tk.IntVar()
        self.createcontacts=tk.IntVar()

        tk.Label(master, text="Appname:").grid(row=0)
        tk.Label(master, text="Apikey:").grid(row=1)

        self.appnameentry = tk.Entry(master)
        self.apikey = tk.Entry(master)


        self.appnameentry.grid(row=0, column=1)
        self.apikey.grid(row=1, column=1)
        self.removehtmlcb = tk.Checkbutton(master, text="Remove HTML", variable=self.removehtml, onvalue=1, offvalue=0)
        self.removehtmlcb.grid(row=2, columnspan=2, sticky=tk.W)
        self.createnewcontacts = tk.Checkbutton(master, text="Create New contacts", variable=self.createcontacts, onvalue=1, offvalue=0)
        self.createnewcontacts.grid(row=3, columnspan=2, sticky=tk.W)

        return self.appnameentry # initial focus


    def apply(self):
        self.appname = self.appnameentry.get()
        self.apikey = self.apikey.get()
        results = {}
        results['appname'] = self.appname
        results['apikey'] = self.apikey
        results['removehtml'] = bool(self.removehtml.get())
        results['createcontacts'] = bool(self.createcontacts.get())
        return results # or something



class largefileimporter:
    """largefileimporter extends the Frame widget from tk.
    this will serve as the "Base" of my application, if you
    will.
    """
    def __init__(self, parent):
        self.parent=parent
        self.sessionsettings=setupdialog(parent)
        self.baseurl = "http://" + self.sessionsettings['appname'] + ".infusionsoft.com"
        self.apiurl = self.baseurl + ":443/api/xmlrpc"
        self.connection = ISServer.ISServer(self.sessionsettings['appname'], self.sessionsettings['apikey'])
        self.applicationpath=os.path.abspath(os.path.join(os.path.expanduser('~'), 'CIA', self.sessionsettings['appname']))
        self.logfile=os.path.join(self.applicationpath, "CIAlogfile.log")
        self.updatelog("Initting")
        os.chdir(self.applicationpath)

    def updatelog(self, message="If you see this you are wrong"):
        logtime=datetime.datetime.now().strftime("%c")
        with open(self.logfile, 'a+') as logging:
            logging.writelines([logtime, message])

    def getallcontactcustomfields(self):
        self.contactcustomfields=self.connection.getallrecords('DataFormField', searchcriteria={"FormId": -1})

    def usermatchFKID(self):
        """This method will have the user inform the
        application of what custom field the fkid is
        stored in
        """
        self.customfieldframe=tk.Frame(self.parent)
        self.customfieldframe.grid()
        ##############
        ## Pick up here


    # def getappname(self):
    #     top = self.top = tk.Toplevel(self.parent)
    #     tk.Label(top, text="AppName").grid(row=0, sticky=tk.W)
    #     tk.Label(top, text="ApiKey").grid(row=1, sticky=tk.W)
    #     self.appnameentry=tk.Entry(top)
    #     self.apikeyentry=tk.Entry(top)
    #     self.appnameentry.grid(row=0, column=1)
    #     self.apikeyentry.grid(row=1, column=1)
    #     self.removehtmlcb = tk.Checkbutton(top, text="Remove HTML")
    #     self.removehtmlcb.grid(row=2, columnspan=2, sticky=tk.W)

d=tk.Tk()
largefileimporter(d)
d.mainloop()
