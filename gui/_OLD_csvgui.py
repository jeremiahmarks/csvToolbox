#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-10-13 20:19:45
# @Last Modified 2015-10-14
# @Last Modified time: 2015-10-14 00:11:07

import csv
from Tkinter import *
import tkFileDialog
import os
import ISServer_master as ISServer
import datetime
##
# First documentation run at 2332, 13Oct


class csvDisplay:
    """This class will define the basic interface that the
    user will have to control the sequence of actions that
    the script performs.

    The application itself can be though of as two columns,
    both split into two rows, so there are four cells total.

    The left column is three units wide.

    The top cell in the left column contains a
    frame to hold basic data describing the current state of
    the application.  Currently that is just appname and
    apikey, but it could easily be expanded to display
    more key:value pairs.

    The bottom cell in the left column is destined to be
    some sort of control panel.

    The right column is the "wide" column.

    At the top of the right cell there should be a narrow area
    for helpful text messages to be displayed to the user.
    There is a default message. The goal is to use it as
    little as possible.

    Below that is the main area.  This is where things will
    do stuff to objects when the user goes hard in the gui.

    Example desired functionality:
        * accept a csv file. scan the file for stats about
        the data within the file. Displays said stats.
            * example stats include - number of unique values
            in a column.
            * longest column
            * average column length
            * best guess of data type
            * excel busters, backend busters(note length, company name length, empty columns, columns without headers)
        * accept a csv file, have credentials, match columns
        to import drop down, create custom fields, help sort
        data (drag and drop for custom drop down fields.)
    """
    def __init__(self, parent):
        # parent is the parent window.  I am not 100% on
        # this but I believe that in this case, it is the
        # Tk() instance.
        # appname, apikey, username, and password should
        # all be obvious. Currently username and password
        # will need to be an employee on the VPN, but that
        # is only because of the stealth "Select a user"
        # screen.
        # self.svr will be a browser instance. I will try to
        # leave it as open as possible, but I am not sure
        # how well I can do that.
        self.parent = parent
        self.appname = None
        self.apikey = None
        self.svr = None
        self.username = None
        self.password = None
        self.browser = None
        #########
        # This serves as the default string displayed if nothing else is passed.
        self.helpfulinfostring = StringVar()
        # self.helpfulinfostring="Let this variable name become ironic.  I dare you."

        self.dataframe = Frame(self.parent)
        self.dataframe.grid(column = 0, sticky=E+W)

        self.buttonsframe = Frame(self.parent)
        self.buttonsframe.grid(column = 0, columnspan=3, row=5, sticky = E+W)

        self.helpfulframe = Frame(self.parent)
        #self.helpfulframe.grid(row=0, column = 3, sticky = E + W)
        self.helpfulframe.grid(row=0, column = 3, rowspan=1, columnspan=1)
        self.mainframe = Frame(self.parent)
        self.mainframe.grid(row=1, column = 3)

        self.builddataframe()
        self.buildbuttonsframe()
        self.buildhelpfulframe()
        self.buildmainframe()


    def builddataframe(self):
        self.appnamelabel = Label(self.dataframe, text="Appname")
        self.appnamelabel.grid(row=0, sticky=W)

        self.appnameentry = Entry(self.dataframe)
        self.appnameentry.grid(row = 0, column=1)

        self.apikeylabel = Label(self.dataframe, text="Apikey")
        self.apikeylabel.grid(row=1, sticky=W)

        self.apikeyentry = Entry(self.dataframe)
        self.apikeyentry.grid(row=1, column=1)
        self.updatedataframe()

    def updatedataframe(self):
        self.appnameentry.delete(0, END)
        self.appnameentry.insert(0, str(self.appname))

        self.apikeyentry.delete(0,END)
        self.apikeyentry.insert(0, str(self.apikey))

    def buildbuttonsframe(self):
        self.updateappnamebutton = Button(self.buttonsframe, text="Update appname", command = self.updateappname(), width=30)
        self.updateappnamebutton.grid()

        self.updateapikeybutton = Button(self.buttonsframe, text="Update apikey", command = self.updateapikey(), width=30)
        self.updateapikeybutton.grid()

        self.downloadconsbutton = Button(self.buttonsframe, text="Download Contacts", command = self.downloadcontacts(), width=30)
        self.downloadconsbutton.grid()

    def buildhelpfulframe(self):

        self.helpfuleinfoLabel = Label(self.helpfulframe, textvariable=self.helpfulinfostring)
        self.helpfuleinfoLabel.pack()
        self.updatehelpfulframe()

    def updatehelpfulframe(self, displaystring=None):
        if displaystring is None:
            displaystring = "Let this variable name become ironic.  I dare you."
        # self.helpfuleinfotext.delete(0,END)
        self.helpfulinfostring.set(displaystring)

    def buildmainframe(self):
        """I would imagine that watching for any function that declares a list and then a for loop
        would be better served by list comprehension.
        """
        self.mainframewidgets=[]
        for x in range(3):
            thislabel = Label(self.mainframe, text=str(x))
            thislabel.grid()
            self.mainframewidgets.append(thislabel)


    def updatemainframe(self):
        pass

    def updateappname(self):
        pass
    def updateapikey(self):
        pass
    def downloadcontacts(self):
        pass

def hello():
    print "hello!"


root = Tk()
menubar = Menu(root)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="split csv to 10Mb", command=hello)
filemenu.add_command(label="Save", command=hello)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=hello)
editmenu.add_command(label="Copy", command=hello)
editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=hello)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar)

myapp = csvDisplay(root)
root.mainloop()
