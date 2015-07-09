#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-07-08 19:48:38
# @Last Modified 2015-07-08
# @Last Modified time: 2015-07-08 19:55:58

import Tkinter as tk
import tkFileDialog
tk.Tk().withdraw()


def getFilePath():
    return tkFileDialog.askopenfilename()


def getFolderPath():
    return tkFileDialog.askdirectory()
