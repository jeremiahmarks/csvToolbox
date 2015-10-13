#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-10-12 18:26:03
# @Last Modified 2015-10-12

# This is basically just a quick example of 
# some basic csv functionality with a gui.

import csv
from Tkinter import *
import tkFileDialog
import os
import ISServer_master as ISServer

class csvDisplay:
    def __init__(self, parent):
        self.parent = parent
        self.appname = None

        self.currentbuttons=[]
        self.currentframes=[]

        buttonwidth = 4
        buttonxpad = "1m"
        buttonypad = "1m"

        mainframexpad = "1m"
        mainframeypad = "1m"
        mainframeixpad = "1m"
        mainframeiypad = "1m"


        self.greeting = Label(parent, text = "Welcome to the CIA.")
        self.greeting.pack()

        self.addcsvfunctions()

    def getappname(self):
        for eachframe in self.currentframes:
            eachframe.pack_forget()
        appnameframe = Frame(self.parent)
        appnameframe.pack()
        self.currentframes.append(appnameframe)
        thisentry = Entry(appnameframe)
        thisentry.pack()
        subbut = Button(appnameframe, text="Set Appname", command = self.getan(thisentry))
        subbut.pack()

    def clearframes(self):
        for eachframe in self.currentframes:
            eachframe.pack_forget()

    def getan(self, entryWidget):
        self.appname = entryWidget.get()
        self.addcsvfunctions()

    def addcsvfunctions(self):
        if self.appname == None:
            self.getappname()
        else:
            self.clearframes()
            self.csvFunctionsOptionFrame = Frame(self.parent)
            self.csvFunctionsOptionFrame.pack()

            self.firstOptionButton = Button(self.csvFunctionsOptionFrame, text = "Contact FKID", command=lambda: self.addFKID())
            self.firstOptionButton.pack()

            self.currentframes.append(self.csvFunctionsOptionFrame)
            self.currentbuttons.append(self.firstOptionButton)

    def addFKID(self):
        self.currentbuttons = []
        if type(self.csvFunctionsOptionFrame) == type(Frame(self.parent)):
            self.csvFunctionsOptionFrame.pack_forget()
        pathtocsv = tkFileDialog.askopenfilename()
        with open(pathtocsv, 'rbU') as infile:
            thisreader = csv.DictReader(infile)
            thesecols = list(thisreader.fieldnames)
        self.chooseframe = Frame(self.parent)
        self.chooseframe.pack()

        for colnum, eachcolumn in enumerate(thesecols):
            colcount = int(colnum) % 5
            thisbutton = Button(self.chooseframe, text = eachcolumn, command=lambda: self.setFKID(eachcolumn))
            thisbutton.grid(column = colcount, row = colnum/5)
            self.currentbuttons.append(thisbutton)

    def setFKID(self, fkidColumn):
        self.fkidcol = fkidColumn





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
