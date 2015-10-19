#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-10-18 15:58:35
# @Last Modified 2015-10-18
# @Last Modified time: 2015-10-18 16:06:15

import Tkinter as tk
import os

class overview:
    def __init__(self, parent, appname = None, apikey = None):
        self.parent = parent
        if appname is not None:
            self.appname = appname
        else:
            self.appname = ''
        if apikey is not None:
            self.apikey = apikey
        else:
            self.apikey = ''
        self.currentFolder = os.path.abspath(os.curdir)
        self.frame = tk.Frame(self.parent)
        self.frame.grid(column = 0, sticky = tk.E+tk.W)
