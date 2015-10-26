#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-10-25 13:18:49
# @Last Modified 2015-10-26
# @Last Modified time: 2015-10-26 01:01:49

# this method will accept an Infusionsoft Application
# name, it's API key (should I be doing an OAuth example?)
# a path to a csv that maps needed values, and then
# uploads the email.

# TODO:
# replace with some OAuth magic.
#
import sys
import ISServer_master as ISServer
import csv
# args = {"contactId" : "", "fromName" : "", "fromAddress" : "", "toAddress" : "", "ccAddresses" : "", "bccAddresses" : "", "contentType" : "", "subject" : "", "htmlBody" : "", "textBody" : "", "header" : "", "receivedDate" : "", "sentDate" : "", "emailSentType" : ""}


class emailuploader:
    neededFieldsInOrder=["contactId","fromName","fromAddress","toAddress","ccAddresses","bccAddresses","contentType","subject","htmlBody","textBody","header","receivedDate","sentDate","emailSentType"]
    neededFieldsSet=set(neededFieldsInOrder)
    """
    Potential fields for CSV
        privateKey:       string (required)
            Your Infusionsoft API key
        contactId:        integer (required)
            The ID of the contact to add this email history to
        fromName:         string (required)
            The name of the email sender
        fromAddress:      string (required)
            The address the email was sent from
        toAddress:        string (required)
            The address the email was sent to
        ccAddresses:      string (required)
            The addresses the email was CC'd to
        bccAddresses:     string (required)
            The addresses the email was BCC'd to
        contentType:      string (required)
            The content type of the email (Text, HTML, or Multipart)
        subject:          string (required)
            The subject line of the email
        htmlBody:         string (required)
            The HTML body of the email
        textBody:         string (required)
            The plain text body of the email
        header:           string (required)
            The email header information
        receivedDate:     string (required)
            The date this email was received. This value determines where the email displays in comparison to other sent messages.
        sentDate:         string (required)
            The date the email was sent
        emailSentType:    integer (required)
            A boolean integer value of 1 is used for marking the email as sent inside the contact history and 0 is used for marking the email as received

    Default values:
        "contactId" : "1",
        "fromName" : "",
        "fromAddress" : "",
        "toAddress" : "",
        "ccAddresses" : "",
        "bccAddresses" : "",
        "contentType" : "",
        "subject" : "",
        "htmlBody" : "",
        "textBody" : "",
        "header" : "",
        "receivedDate" : "",
        "sentDate" : "",
        "emailSentType" : ""

    """
    def __init__(self, pathtofile, appname, apikey):
        self.pathtofile = pathtofile
        self.appname=appname
        self.apikey=apikey
        self.connection=ISServer.ISServer(self.appname, self.apikey)
        with open(self.pathtofile, 'rUb') as infile:
            thisreader = csv.DictReader(infile)
            if set(emailuploader.neededFieldsInOrder).issubset(set(thisreader.fieldnames)):
                for eachrow in thisreader:
                    print self.apikey, int(eachrow["contactId"]),eachrow["fromName"],eachrow["fromAddress"],eachrow["toAddress"],eachrow["ccAddresses"],eachrow["bccAddresses"],eachrow["contentType"],eachrow["subject"],eachrow["htmlBody"],eachrow["textBody"],eachrow["header"],eachrow["receivedDate"],eachrow["sentDate"],int(eachrow["emailSentType"])
                    self.connection.connection.APIEmailService.attachEmail(self.apikey, int(eachrow["contactId"]),eachrow["fromName"],eachrow["fromAddress"],eachrow["toAddress"],eachrow["ccAddresses"],eachrow["bccAddresses"],eachrow["contentType"],eachrow["subject"],eachrow["htmlBody"],eachrow["textBody"],eachrow["header"],eachrow["receivedDate"],eachrow["sentDate"],int(eachrow["emailSentType"]))

if __name__ == '__main__':
    emailuploader('/home/jlmarks/dangerzone/csvToolbox/samplecsv.txt', 'if188', 'f1a4ac7f9dbe2341ad0b84b52581c93e')
