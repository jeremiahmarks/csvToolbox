#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-10-18 15:03:04
# @Last Modified 2015-10-18
# @Last Modified time: 2015-10-18 15:31:23


# menus are used throughout the application. This file will
# serve as their main "home"
import Tkinter as tk
def sayhi():
    print "Hi!"

def main(parent):
    menubar = tk.Menu(parent)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label = "set appname", command = sayhi)
    filemenu.add_command(label = "Exit", command = parent.quit)
    menubar.add_cascade(label = "File", menu=filemenu)

    parent.config(menu=menubar)

