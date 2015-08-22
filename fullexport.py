#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-08-20
# @Last Modified
# @Last Modified time:

import os
import sys
import csv
import urllib3
import ssl


import ISServer_master as ISServer
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
import Tkinter as tk
import tkFileDialog
tk.Tk().withdraw()

class fullexporter():

	def __init__(self):
		self.fullrun()

	def getFilePath(self):
	    return tkFileDialog.askopenfilename()

	def getFolderPath(self):
	    return tkFileDialog.askdirectory()

	def getappname(self):
		return raw_input("Please enter appname:").strip('\n \t')

	def getapikey(self):
		username='yourusername'
		password='yourpassword'
		self.browser = RoboBrowser(history=True)
		self.browser.open(self.baseurl)
		logform = self.browser.get_form()
		logform.fields['username'].value = username
		logform.fields['password'].value = password
		self.browser.submit_form(logform)
		self.browser.follow_link(self.browser.get_links()[1])
		self.browser.open(self.baseurl + 'app/miscSetting/itemWrapper?systemId=nav.admin&settingModuleName=Application&settingTabName=Application')
		pageSoup = BeautifulSoup(self.browser.response.content, 'html.parser')
		self.apikey = pageSoup.findAll(id='Application_Encrypted_Key:_data')[0].text

	def fullrun(self):
		self.appname=self.getappname()
		self.baseurl = 'https://' + self.appname + '.infusionsoft.com/'
		self.getapikey()
		self.svr = ISServer.ISServer(self.appname, self.apikey)
		self.startingpath = os.path.abspath(os.curdir)
		self.apppath = os.path.join(self.startingpath, self.appname)
		if not os.path.exists(self.apppath):
			os.mkdir(self.apppath)
		os.chdir(self.apppath)
		if not os.path.exists('files'):
			os.mkdir('files')
		self.tabs = self.svr.getAllRecords('DataFormTab')
		self.groups = self.svr.getAllRecords('DataFormGroup')
		self.fields = self.svr.getAllRecords('DataFormField')
