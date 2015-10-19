#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Last Modified 2015-10-14

# This is just a text file

import csv
from Tkinter import *
import tkFileDialog
import os
import ISServer_master as ISServer
import datetime

class csvDisplay:
    def __init__(self, parent):
        self.parent = parent
        self.appname = 'xo263'
        self.apikey = '9e0a9f3b60b39b40c463075062468496ed5c0aa2a164482e70822f70444ea259'
        self.svr = ISServer.ISServer(self.appname, self.apikey)
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



        self.addFKID()


    def addFKID(self):
        thesecols=['a', 'b', 'c']
        self.currentbuttons = []
        if type(self.csvFunctionsOptionFrame) == type(Frame(self.parent)):
            self.csvFunctionsOptionFrame.pack_forget()
        self.chooseframe = Frame(self.parent)
        self.chooseframe.pack()

        for colnum, eachcolumn in enumerate(sorted(thesecols)):
            colcount = int(colnum) % 5
            thisbutton = Button(self.chooseframe, text = eachcolumn, command=lambda: self.setFKID(str(eachcolumn)))
            thisbutton.grid(column = colcount, row = colnum/5)
            self.currentbuttons.append(thisbutton)

    def setFKID(self, fkidColumn):
        print fkidColumn








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
        print fkidColumn
