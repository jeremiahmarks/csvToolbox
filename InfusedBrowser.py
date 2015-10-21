#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-10-20 20:21:09
# @Last Modified 2015-10-21
# @Last Modified time: 2015-10-21 00:16:40

# Infused browser will handle the browser automation side
# of things.

# here is a base example of the functionality that I
# envision

    # def getapikey(self):
    #     global pw
    #     username = pw['username']
    #     password = pw['password']
    #     #Basically:
    #     #    #Add username and password to your global variables.
    #     self.browser = RoboBrowser(history=True)
    #     self.browser.open(self.baseurl)
    #     logform = self.browser.get_form()
    #     logform.fields['username'].value = username
    #     logform.fields['password'].value = password
    #     self.browser.submit_form(logform)
    #     self.browser.follow_link(self.browser.get_links()[1])
    #     self.browser.open(self.baseurl + 'app/miscSetting/itemWrapper?systemId=nav.admin&settingModuleName=Application&settingTabName=Application')
    #     pageSoup = BeautifulSoup(self.browser.response.content, 'html.parser')
    #     return pageSoup.findAll(id='Application_Encrypted_Key:_data')[0].text
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
import os

class infs_brsr:
    """This browser will have functions useful to someone
    browsing the Infusionsoft front end programatically.
    """

    def __init__(self, appname, username, password, *args, **kwargs):
        self.loggedin=False
        self.browser=RoboBrowser(history=True)
        self.appname=appname
        self.username=username
        self.password=password
        self.baseurl = 'https://' + self.appname + '.infusionsoft.com'

    def openbase(self):
        self.browser.open(self.baseurl)

    def login(self):
        self.openbase()
        loginform = self.browser.get_form()
        loginform.fields['username'].value = self.username
        loginform.fields['password'].value = self.password
        self.browser.submit_form(loginform)
        # This next step is probably a bad idea.  It needs
        # some form of control
        self.browser.follow_link(self.browser.get_links()[1])
        self.loggedin=True

    def getapikey(self):
        if not self.loggedin:
            self.login()
        self.browser.open(self.baseurl + 'app/miscSetting/itemWrapper?systemId=nav.admin&settingModuleName=Application&settingTabName=Application')
        pageSoup = BeautifulSoup(self.browser.response.content, 'html.parser')
        self.apikey=pageSoup.findAll(id='Application_Encrypted_Key:_data')[0].text
        return self.apikey

    def importContactCSV(self, pathToCSV='/home/jlmarks/importme.csv'):
        if not self.loggedin:
            self.login()
        importURL = "https://" + self.appname + ".infusionsoft.com/Import/jumpToWizard.jsp?update=false&profileClass=com.infusion.crm.db.importer.profiles.ContactProfile"
        self.browser.open(importURL)
        frms = self.browser.get_forms()
        for eachform in frms:
            if 'id' in eachform.fields.keys():
                self.thisimportid=eachform['id'].value
                correctform = eachform
        correctform.fields.pop('Back')
        correctform.fields['importFile'].value=open(pathToCSV, 'rb')
        self.browser.submit_form(correctform)
# some stuff to note!
# kk=a.browser.session.get( 'https://if188.infusionsoft.com/Import/step/map/include/fields.jsp?_=1445410553874')
# kk.content
# print kk.content
