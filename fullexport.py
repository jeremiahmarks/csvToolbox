#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-08-20
# @Last Modified
# @Last Modified time:

import os
import sys
import ISServer_master as ISServer
import Tkinter as tk
import tkFileDialog
tk.Tk().withdraw()


def getFilePath():
    return tkFileDialog.askopenfilename()


def getFolderPath():
    return tkFileDialog.askdirectory()

def downloadall():

