#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-10-18 14:52:56
# @Last Modified 2015-10-19
# @Last Modified time: 2015-10-19 04:41:28

# Main frame will be the frame that holds the individual
# frames that make up the user interface.  This will include
# the main navigation menu.

import Tkinter as tk
import menus
import interactionframe


class CIA:
    def __init__(self, appname=None, apikey=None, settings=None, mode=None):
        self.appname=appname
        self.apikey=apikey
        if settings is None:
            self.settings="CIA.settings"
        else:
            self.settings = settings
        self.mainframe = tk.Tk()
        menus.main(self.mainframe)
        self.dataframe=tk.Frame(self.mainframe)
        self.dataframe.grid(column = 0, columnspan=3)

        self.interactionframe=tk.Frame(self.mainframe)
        self.interactionframe.grid(column=3)

        self.builddataframe()
        self.buildinteractionframe()
        root.mainloop()

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
