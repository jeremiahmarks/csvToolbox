#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-06-18 14:45:26
# @Last Modified by:   jeremiah.marks
# @Last Modified time: 2015-06-18 14:50:36

# This script will allow you to specify one of the contact fields
# and then will delete the information in that field from all
# contacts in the account.
import xmlrpclib


# You will want to set this variable to the column that you want
# to delete.  Default options are listed below, however custom
# fields should work as well.

fieldtodelete="LastName"

#          "AccountId"  "LeadSourceId"   "Country"       "Phone5Type"
#       "Address1Type"  "Leadsource"     "Country2"      "PostalCode"
#    "Address2Street1"  "MiddleName"     "Country3"      "PostalCode2"
#    "Address2Street2"  "Nickname"       "CreatedBy"     "PostalCode3"
#       "Address2Type"  "OwnerID"        "DateCreated"   "ReferralCode"
#    "Address3Street1"  "Password"       "Email"         "SpouseName"
#    "Address3Street2"  "Phone1"         "EmailAddress2" "State"
#       "Address3Type"  "Phone1Ext"      "EmailAddress3" "State2"
#        "Anniversary"  "Phone1Type"     "Fax1"          "State3"
#      "AssistantName"  "Phone2"         "Fax1Type"      "StreetAddress1"
#     "AssistantPhone"  "Phone2Ext"      "Fax2"          "StreetAddress2"
# "BillingInformation"  "Phone2Type"     "Fax2Type"      "Suffix"
#           "Birthday"  "Phone3"         "FirstName"     "Title"
#               "City"  "Phone3Ext"      "Groups"        "Username"
#              "City2"  "Phone3Type"     "Id"            "Validated"
#              "City3"  "Phone4"         "JobTitle"      "Website"
#            "Company"  "Phone4Ext"      "LastName"      "ZipFour1"
#          "CompanyID"  "Phone4Type"     "LastUpdated"   "ZipFour2"
#       "ContactNotes"  "Phone5"         "LastUpdatedBy" "ZipFour3"
#        "ContactType"  "Phone5Ext"




class ISServer:
    def __init__(self, infusionsoftapp, infusionsoftAPIKey):
        self.infusionsoftapp=infusionsoftapp
        self.infusionsoftAPIKey=infusionsoftAPIKey
        self.appurl = "https://" + self.infusionsoftapp + ".infusionsoft.com:443/api/xmlrpc"
        self.connection = xmlrpclib.ServerProxy(self.appurl)

    def getAllRecords(self, tableName, interestingData=None, searchCriteria=None, orderedBy=None):
        if interestingData is None:
            interestingData = tables[tableName]
        if searchCriteria is None:
            searchCriteria={}
        if orderedBy is None:
            orderedBy = interestingData[0]
        records = []
        p=0
        while True:
            listOfDicts = self.connection.DataService.query(self.infusionsoftAPIKey, tableName, 1000, p, searchCriteria, interestingData, orderedBy, True)
            for each in listOfDicts:
                thisRecord={}
                for eachbit in interestingData:
                    if not each.has_key(eachbit):
                        each[eachbit]=None
                    thisRecord[eachbit] = each[eachbit]
                records.append(thisRecord)
            if not(len(listOfDicts)==1000):
                break
            p+=1
        return records


    ########################################################
  ## Methods to updating existing records
    ##
    def updateRecord(self, tableName, recordId, updateValues):
        return self.connection.DataService.update(self.infusionsoftAPIKey, tableName, recordId, updateValues)


appname=raw_input('\nappname:').strip(' \n')
apikey=raw_input('\napikey').strip(' \n')

server=ISServer(appname, apikey)


allcontacts=server.getAllRecords("Contact")

for counter, eachcontact in enumerate(allcontacts):
    server.updateRecord("Contact", eachcontact['Id'], {fieldtodelete : ''})
    print counter
