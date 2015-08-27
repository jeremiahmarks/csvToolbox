#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-08-20
# @Last Modified
# @Last Modified 2015-08-23

import os
import sys
import csv
import urllib3
import ssl
import re
import ssl


import threading
import requests
from Queue import Queue

import ISServer_master as ISServer
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
import Tkinter as tk
import tkFileDialog
tk.Tk().withdraw()

global pw

class DownloadThread(threading.Thread):
    def __init__(self, queue, destfolder, owner):
        super(DownloadThread, self).__init__()
        self.queue = queue
        self.destfolder = destfolder
        self.daemon = True
        self.owner=owner

    def run(self):
        while True:
            url = self.queue.get()
            try:
                self.download_url(url)
            except Exception,e:
                print "   Error: %s"%e
            self.queue.task_done()

    def download_url(self, url):
        # change it to a different way if you require
        fileoutpath = os.path.join(self.basedir, contactId, str(fileId)+fileName)


class fullexporter():
    global pw
    def __init__(self):
        self.startingpath = os.path.abspath(os.curdir)
        self.appname=self.getappname()
        self.mapping={}
        self.mapping['Contact']=-1
        self.mapping['Affiliate']=-3
        self.mapping['ContactAction']=-5
        self.mapping['Company']=-6
        self.mapping['OrderItem']=-9

        self.menu()

    def menu(self, context="initial"):
        if context is "initial":
            self.baseurl = 'https://' + self.appname + '.infusionsoft.com/'
            self.apikey=self.getapikey()
            self.svr = ISServer.ISServer(self.appname, self.apikey)
            self.apppath = os.path.join(self.startingpath, self.appname)
            if not os.path.exists(self.apppath):
                os.mkdir(self.apppath)
            os.chdir(self.apppath)
            if not os.path.exists('files'):
                os.mkdir('files')
            os.chdir('files')
            self.usermenu={}
            self.usermenu['downloadAPITables'] = 'apit'
            self.usermenu['play'] = 'play'
            self.usermenu['reports'] = 'rpts'
        for eachitem in self.usermenu.keys():
            print eachitem + ":\t" + self.usermenu[eachitem]
        thisChoice = raw_input('please make a choice: ').strip(' \n\t')
        if thisChoice == 'apit':
            self.handleAPItables()
        elif thisChoice == 'play':
            self.play()
        elif thisChoice == 'rpts':
            self.downloadAllReports()
        else:
            self.menu()

    def handlefiles(self):
        os.chdir(self.startingpath)
        if not os.path.exists('files'):
            os.mkdir('files')
        os.chdir('files')
        allfiles = self.svr.getAllRecords('FileBox')
        for eachfile in allfiles:
            downloadurl = self.baseurl+"Download?Id="+str(eachfile['Id'])
            self.browser.open(downloadurl)
            fileoutpath = os.path.join(self.startingpath, 'files', eachfile['ContactId'], eachfile['FileName'])
            if not os.path.exists(os.path.dirname(fileoutpath)):
                os.makedirs(fileoutpath)
            fout = open(fileoutpath, 'wb')
            fout.write(self.browser.response.content)
            fout.close()


    def play(self):
        print "she's all yours captain!"

    def downloadAReport(self, reportname):
        self.browser.open(self.baseurl + "Reports/exportResults.jsp?reportClass=" + reportname)
        reportForm = [eachform for eachform in self.browser.get_forms() if eachform.action == 'qbExport.jsp']
        if len(reportForm) > 0:
            self.browser.submit_form(reportForm[0], submit=reportForm[0].submit_fields['process'])
            with open(reportname+".csv", 'wb') as outfile:
                outfile.write(self.browser.response.content)
        else:
            print "no " + reportname

    def downloadAllReports(self):
        for reportname in [ "AffiliateActivitySummary", "AffiliateLedger", "AffiliateRedirectActivity", "AffiliateReferral", "AffPayout", "AllOrders", "AllSales", "AllSalesItemized", "ARAgingReport", "CampaigneeBasic", "CampaigneeByDay", "CampaignProductConversion", "ClickThroughPercentage", "ClickThroughPercentageByEmail", "ContactDistributed", "CProgramRevenueSummary", "CreditCard", "CreditsIssued", "CustomerLifetimeValue", "DailyPayments", "DailyReceivables", "DailySalesTotals", "DashboardCampaign", "DashboardEmail", "DashboardLeads", "DashboardOrders", "DashboardUsers", "DigitalProductKey", "EmailBatchSearch", "EmailBroadcastConversionReport", "EmailConversion", "EmailSentSearch", "FailedCharge", "FaxBatchSearch", "FollowUpSequenceConversionReport", "FunnelFlowRecipient", "FunnelFlowRecipientWaiting", "FunnelGoalAchieved", "FunnelQueuedFlowItem", "FunnelUniqueContacts", "GroupAdds", "HabeasDetail", "InvoiceNetIncome", "LeadSourceConversion", "LeadSourceIncome", "LeadSourceROI", "LeadSourceROIByCategory", "MonthlyPayments", "MonthlyReceivables", "MonthlySalesTotals", "MonthlySalesTotalsByProduct", "OptOutSearch", "PaymentsReport", "PieceResponse", "ProductNetIncome", "Receivables", "RevenueForecastReport", "TaskSearch", "VoiceBatchSearch", "VoiceOptOutSearch", "WebformActivitySummary", "WebFormTracking" ]:
            self.downloadAReport(reportname)

    def getFilePath(self):
        return tkFileDialog.askopenfilename()

    def getFolderPath(self):
        return tkFileDialog.askdirectory()

    def getappname(self):
        return raw_input("Please enter appname:").strip('\n \t')

    def getapikey(self):
        global pw
        username = pw['username']
        password = pw['password']
        #Basically:
        #    #Add username and password to your global variables.
        self.browser = RoboBrowser(history=True)
        self.browser.open(self.baseurl)
        logform = self.browser.get_form()
        logform.fields['username'].value = username
        logform.fields['password'].value = password
        self.browser.submit_form(logform)
        self.browser.follow_link(self.browser.get_links()[1])
        self.browser.open(self.baseurl + 'app/miscSetting/itemWrapper?systemId=nav.admin&settingModuleName=Application&settingTabName=Application')
        pageSoup = BeautifulSoup(self.browser.response.content, 'html.parser')
        return pageSoup.findAll(id='Application_Encrypted_Key:_data')[0].text

    def handleAPItables(self):
        apidata={}
        self.customfields=self.svr.getAllRecords('DataFormField')
        for eachtable in ISServer.tables.keys():
            print "starting " + eachtable
            if eachtable not in self.mapping.keys():
                self.mapping[eachtable]=99
            fields = ISServer.tables[eachtable] +  ['_'+fld['Name'] for fld in self.customfields if fld['FormId'] is self.mapping[eachtable]]
            apidata[eachtable] =  self.svr.getAllRecords(eachtable, interestingData=fields)
            with open(eachtable+".csv", 'wb') as outfile:
                writer=csv.DictWriter(outfile, fields)
                writer.writeheader()
                writer.writerows(apidata[eachtable])
            print "done writing " + eachtable
        self.apidata = apidata



    def handlewebforms(self):
        # for eachid
        # webformsubmissionpath="https://" + self.appname + ".infusionsoft.com/app/webformSubmission/contactTabDetails?customFormWebResultId=" + str(x)
        pass



fullknownreports = [ "AffiliateActivitySummary", "AffiliateLedger", "AffiliateRedirectActivity", "AffiliateReferral", "AffPayout", "AllOrders", "AllSales", "AllSalesItemized", "ARAgingReport", "CampaigneeBasic", "CampaigneeByDay", "CampaignProductConversion", "ClickThroughPercentage", "ClickThroughPercentageByEmail", "ContactDistributed", "CProgramRevenueSummary", "CreditCard", "CreditsIssued", "CustomerLifetimeValue", "DailyPayments", "DailyReceivables", "DailySalesTotals", "DashboardCampaign", "DashboardEmail", "DashboardLeads", "DashboardOrders", "DashboardUsers", "DigitalProductKey", "EmailBatchSearch", "EmailBroadcastConversionReport", "EmailConversion", "EmailSentSearch", "FailedCharge", "FaxBatchSearch", "FollowUpSequenceConversionReport", "FunnelFlowRecipient", "FunnelFlowRecipientWaiting", "FunnelGoalAchieved", "FunnelQueuedFlowItem", "FunnelUniqueContacts", "GroupAdds", "HabeasDetail", "InvoiceNetIncome", "LeadSourceConversion", "LeadSourceIncome", "LeadSourceROI", "LeadSourceROIByCategory", "MonthlyPayments", "MonthlyReceivables", "MonthlySalesTotals", "MonthlySalesTotalsByProduct", "OptOutSearch", "PaymentsReport", "PieceResponse", "ProductNetIncome", "Receivables", "RevenueForecastReport", "TaskSearch", "VoiceBatchSearch", "VoiceOptOutSearch", "WebformActivitySummary", "WebFormTracking" ]
