#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-07-08 19:58:40
# @Last Modified 2015-10-18
# @Last Modified time: 2015-10-18 15:14:41

# CSV Import Assistant (CIA) will provide a full on
# Graphical, moderately user friendly, way to interact with
# CSV files (potentially others, depends on need) and the
# Infusionsoft front end and API. It will use only external
# methods.


import csv
import os
import Tkinter as tk
import tkFileDialog
tk.Tk().withdraw()


def getFilePath():
    return tkFileDialog.askopenfilename()


def getFolderPath():
    return tkFileDialog.askdirectory()
