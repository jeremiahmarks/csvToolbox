#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-16 19:15:29
# @Last Modified 2015-06-20
# @Last Modified time: 2015-06-20 22:09:46
import datetime
import random
import string
import xmlrpclib
import urllib
import csv
import productImage
import productObjects
import my_pw as pw

global products

localids=set()

productCatagories={}
products=[]
tables={}
tables["Product"] = ["BottomHTML", "CityTaxable", "CountryTaxable", "Description", "HideInStore", "Id", "InventoryLimit", "InventoryNotifiee", "IsPackage", "LargeImage", "NeedsDigitalDelivery", "ProductName", "ProductPrice", "Shippable", "ShippingTime", "ShortDescription", "Sku", "StateTaxable", "Status", "Taxable", "TopHTML", "Weight"]
tables['ProductOptValue'] = ["Id", "IsDefault", "Label", "Name", "OptionIndex", "PriceAdjustment", "ProductOptionId", "Sku",]
tables['ProductOption'] = ["AllowSpaces", "CanContain", "CanEndWith", "CanStartWith", "Id", "IsRequired", "Label", "MaxChars", "MinChars", "Name", "OptionType", "Order", "ProductId", "TextMessage"]
tables['ProductCategory'] = ["CategoryDisplayName", "CategoryImage", "CategoryOrder", "Id", "ParentId"]
tables["ProductCategoryAssign"]=["Id","ProductCategoryId","ProductId"]

# This is the SKU scheme, as I have figured out.
# GP  [RB]Attachment Type=Standard 3- Hole System"
# GPM  [RB]Attachment Type=Polar Magnetic System"
# GPP  [RB]Attachment Type=Standard 3- Hole System"
# GPPX  [RB]Attachment Type=Standard 3- Hole System"




def id_generator(size=10, chars=string.ascii_uppercase):

    global localids
    thisid=''.join(random.choice(chars) for _ in range(size))
    while thisid in localids:
        thisid =''.join(random.choice(chars) for _ in range(size))
    localids.add(thisid)
    return thisid

class Product(object):

    def __init__(self, values):
        self.values=values
        global products
        self.internalid=id_generator()
        if 'products' not in globals():
            products=[]
        if ("BottomHTML" in values.keys()):
            self.BottomHTML = values["BottomHTML"]
        else:
            self.BottomHTML=None
        if ("CityTaxable" in values.keys()):
            self.CityTaxable = values["CityTaxable"]
        else:
            self.CityTaxable=None
        if ("CountryTaxable" in values.keys()):
            self.CountryTaxable = values["CountryTaxable"]
        else:
            self.CountryTaxable=None
        if ("Description" in values.keys()):
            self.Description = values["Description"]
        else:
            self.Description=None
        if ("HideInStore" in values.keys()):
            self.HideInStore = values["HideInStore"]
        else:
            self.HideInStore=None
        if ("Id" in values.keys()):
            self.Id = values["Id"]
        else:
            self.Id=None
        if ("InventoryLimit" in values.keys()):
            self.InventoryLimit = values["InventoryLimit"]
        else:
            self.InventoryLimit=None
        if ("InventoryNotifiee" in values.keys()):
            self.InventoryNotifiee = values["InventoryNotifiee"]
        else:
            self.InventoryNotifiee=None
        if ("IsPackage" in values.keys()):
            self.IsPackage = values["IsPackage"]
        else:
            self.IsPackage=None
        if ("LargeImage" in values.keys()):
            self.LargeImage = values["LargeImage"]
        else:
            self.LargeImage=None
        if ("NeedsDigitalDelivery" in values.keys()):
            self.NeedsDigitalDelivery = values["NeedsDigitalDelivery"]
        else:
            self.NeedsDigitalDelivery=None
        if ("ProductName" in values.keys()):
            self.ProductName = values["ProductName"]
        else:
            self.ProductName=None
        if ("ProductPrice" in values.keys()):
            self.ProductPrice = values["ProductPrice"]
        else:
            self.ProductPrice=None
        if ("Shippable" in values.keys()):
            self.Shippable = values["Shippable"]
        else:
            self.Shippable=None
        if ("ShippingTime" in values.keys()):
            self.ShippingTime = values["ShippingTime"]
        else:
            self.ShippingTime=None
        if ("ShortDescription" in values.keys()):
            self.ShortDescription = values["ShortDescription"]
        else:
            self.ShortDescription=None
        if ("Sku" in values.keys()):
            self.Sku = values["Sku"]
        else:
            self.Sku=None
        if ("StateTaxable" in values.keys()):
            self.StateTaxable = values["StateTaxable"]
        else:
            self.StateTaxable=None
        if ("Status" in values.keys()):
            self.Status = values["Status"]
        else:
            self.Status=None
        if ("Taxable" in values.keys()):
            self.Taxable = values["Taxable"]
        else:
            self.Taxable=None
        if ("TopHTML" in values.keys()):
            self.TopHTML = values["TopHTML"]
        else:
            self.TopHTML=None
        if ("Weight" in values.keys()):
            self.Weight = values["Weight"]
        else:
            self.Weight=None
        self.categories={}
        self.catStrings=[]
        self.images=[]
        self.imageStrings=[]
        self.options={}
        self.optionrows=[]
        self.optionsSettings=None
        self.optionsPriceChange={}
        self.pricingrows=[]
        self.rowdata=[]
        self.register()

    def getid(self):
        """Doing functionality like this allows things to be
        saved by a unique id, even if there is not one available
        """
        if self.Id is None:
            return self.internalid
        else:
            return self.Id

    def __eq__(self, other):
        if self.getid()==other.getid() or self.internalid==other.internalid:
            return True
        catsmatch= len(self.categories.keys())>0 is len(other.categories.keys())>0   # Basically,
        # this checks to see if both of the products have categories or if
        # they both do not. Basically the statment says
        #               [T/F] is [T/F]
        # and returns that.
        if self.ProductName and other.ProductName:
            namesmatch=self.ProductName.lower().strip(' \n') is other.ProductName.lower().strip(' \n')
            return namesmatch and catsmatch
        return False

    def getid(self):
        """Doing functionality like this allows things to be
        saved by a unique id, even if there is not one available
        """
        if self.Id is None:
            return self.internalid
        else:
            return self.Id

    def prepare(self):
        vals={}
        if self.BottomHTML is not None:
            vals["BottomHTML"] = self.BottomHTML
        if self.CityTaxable is not None:
            vals["CityTaxable"] = self.CityTaxable
        if self.CountryTaxable is not None:
            vals["CountryTaxable"] = self.CountryTaxable
        if self.Description is not None:
            vals["Description"] = self.Description
        if self.HideInStore is not None:
            vals["HideInStore"] = self.HideInStore
        if self.Id is not None:
            vals["Id"] = self.Id
        if self.InventoryLimit is not None:
            vals["InventoryLimit"] = self.InventoryLimit
        if self.InventoryNotifiee is not None:
            vals["InventoryNotifiee"] = self.InventoryNotifiee
        if self.IsPackage is not None:
            vals["IsPackage"] = self.IsPackage
        if self.LargeImage is not None:
            vals["LargeImage"] = self.LargeImage
        if self.NeedsDigitalDelivery is not None:
            vals["NeedsDigitalDelivery"] = self.NeedsDigitalDelivery
        if self.ProductName is not None:
            vals["ProductName"] = self.ProductName
        if self.ProductPrice is not None:
            vals["ProductPrice"] = self.ProductPrice
        if self.Shippable is not None:
            vals["Shippable"] = self.Shippable
        if self.ShippingTime is not None:
            vals["ShippingTime"] = self.ShippingTime
        if self.ShortDescription is not None:
            vals["ShortDescription"] = self.ShortDescription
        if self.Sku is not None:
            vals["Sku"] = self.Sku
        if self.StateTaxable is not None:
            vals["StateTaxable"] = self.StateTaxable
        if self.Status is not None:
            vals["Status"] = self.Status
        if self.Taxable is not None:
            vals["Taxable"] = self.Taxable
        if self.TopHTML is not None:
            vals["TopHTML"] = self.TopHTML
        if self.Weight is not None:
            vals["Weight"] = self.Weight
        # for eachitem in vals.keys():
        #     # Since I cannot currently deal well with unicode, I must exclude it from writing to csv
        #     if type('str')==type(vals[eachitem]):
        #         for eachchr in vals[eachitem]:
        #             if ord(eachchr)>127:
        #                 print "Error " + str(ord(eachchr))
        #                 vals[eachitem]=vals[eachitem].replace(eachchr, 'RR'+str(ord(eachchr)))
        return vals

    def setAppName(self, appname):
        self.appname=appname

    def setServer(self,parentServer):
        self.server=parentServer
        self.appname=server.infusionsoftapp

    def getPublicPage(self, appname):
        if self.Id is not None:
            return "https://" + server.infusionsoftapp + ".infusionsoft.com/app/storeFront/showProductDetail?productId=" + str(self.Id)
        else:
            return "I do not seem to have an ID."

    def getInternalPage(self):
        if self.Id is not None:
            return "https://" + server.infusionsoftapp + ".infusionsoft.com/app/product/manageProduct?productId=" + str(self.Id)
        else:
            return "I do not seem to have an ID."

    def detailedData(self):
        externalValues={}
        externalValues['publicPage'] = self.getPublicPage(server.infusionsoftapp)
        externalValues['internalPage'] = self.getInternalPage()
        externalValues.update(self.vals())
        return externalValues

    def register(self):
        if self not in products:
            products.append(self)

class ProductCategory(object):
    global productcategorys
    if 'productcategorys' not in globals():
        productcategorys = []

    def __init__(self,values):
        self.values=values
        self.internalid = id_generator()
        if "CategoryDisplayName" in values.keys():
            self.CategoryDisplayName=values["CategoryDisplayName"]
        else:
            self.CategoryDisplayName=None
        if "CategoryImage" in values.keys():
            self.CategoryImage=values["CategoryImage"]
        else:
            self.CategoryImage=None
        if "CategoryOrder" in values.keys():
            self.CategoryOrder=values["CategoryOrder"]
        else:
            self.CategoryOrder=None
        if "Id" in values.keys():
            self.Id=values["Id"]
        else:
            self.Id=None
        if "ParentId" in values.keys():
            self.ParentId=values["ParentId"]
        else:
            self.ParentId=None
        self.register()

    def getid(self):
        """Doing functionality like this allows things to be
        saved by a unique id, even if there is not one available
        """
        if self.Id is None:
            return self.internalid
        else:
            return self.Id

    def prepare(self):
        vals={}
        if self.CategoryDisplayName is not None:
            vals["CategoryDisplayName"] = self.CategoryDisplayName
        if self.CategoryImage is not None:
            vals["CategoryImage"] = self.CategoryImage
        if self.CategoryOrder is not None:
            vals["CategoryOrder"] = self.CategoryOrder
        if self.Id is not None:
            vals["Id"] = self.Id
        if self.ParentId is not None:
            vals["ParentId"] = self.ParentId
        # for eachitem in vals.keys():
            # Since I cannot currently deal well with unicode, I must exclude it from writing to csv
            # if type(u'str')==type(vals[eachitem]):
            #     for eachchr in vals[eachitem]:
            #         if ord(eachchr)>127:
            #             print "Error " + str(ord(eachchr))
            #             vals[eachitem]=vals[eachitem].replace(eachchr, 'RR'+str(ord(eachchr)))
        return vals

    def register(self):
        if self not in productcategorys:
            productcategorys.append(self)

class ProductCategoryAssign(object):
    global productcategoryassigns
    if 'productcategoryassigns' not in globals():
        productcategoryassigns = []

    def __init__(self,values):
        self.values=values
        self.internalid=id_generator()
        if "Id" in values.keys():
            self.Id=values["Id"]
        else:
            self.Id=None
        if "ProductCategoryId" in values.keys():
            self.ProductCategoryId=values["ProductCategoryId"]
        else:
            self.ProductCategoryId=None
        if "ProductId" in values.keys():
            self.ProductId=values["ProductId"]
        else:
            self.ProductId=None
        self.register()

    def getid(self):
        """Doing functionality like this allows things to be
        saved by a unique id, even if there is not one available
        """
        if self.Id is None:
            return self.internalid
        else:
            return self.Id

    def prepare(self):
        vals={}
        if self.Id is not None:
            vals["Id"] = self.Id
        if self.ProductCategoryId is not None:
            vals["ProductCategoryId"] = self.ProductCategoryId
        if self.ProductId is not None:
            vals["ProductId"] = self.ProductId
        # for eachitem in vals.keys():
            # Since I cannot currently deal well with unicode, I must exclude it from writing to csv
            # if type('str')==type(vals[eachitem]):
            #     for eachchr in vals[eachitem]:
            #         if ord(eachchr)>127:
            #             print "Error " + str(ord(eachchr))
            #             vals[eachitem]=vals[eachitem].replace(eachchr, 'RR'+str(ord(eachchr)))
        return vals

    def register(self):
        if self not in productcategoryassigns:
            productcategoryassigns.append(self)

class ProductOptValue(object):
    global productoptvalues
    if 'productoptvalues' not in globals():
        productoptvalues = []

    def __init__(self,values):
        self.values=values
        self.internalid=id_generator()
        if "Id" in values.keys():
            self.Id=values["Id"]
        else:
            self.Id=None
        if "IsDefault" in values.keys():
            self.IsDefault=values["IsDefault"]
        else:
            self.IsDefault=None
        if "Label" in values.keys():
            self.Label=values["Label"]
        else:
            self.Label=None
        if "Name" in values.keys():
            self.Name=values["Name"]
        else:
            self.Name=None
        if "OptionIndex" in values.keys():
            self.OptionIndex=values["OptionIndex"]
        else:
            self.OptionIndex=None
        if "PriceAdjustment" in values.keys():
            self.PriceAdjustment=values["PriceAdjustment"]
        else:
            self.PriceAdjustment=None
        if "ProductOptionId" in values.keys():
            self.ProductOptionId=values["ProductOptionId"]
        else:
            self.ProductOptionId=None
        if "Sku" in values.keys():
            self.Sku=values["Sku"]
        else:
            self.Sku=None
        self.register()

    def __eq__(self, other):
        if self.getid()==other.getid() or self.internalid==other.internalid:
            return True
        if self.Name and other.Name:
            namesmatch=self.Name.lower().strip(' \n') is other.Name.lower().strip(' \n')
            return namesmatch and (self.ProductOptionId is other.ProductOptionId)
        return False

    def getid(self):
        """Doing functionality like this allows things to be
        saved by a unique id, even if there is not one available
        """
        if self.Id is None:
            return self.internalid
        else:
            return self.Id

    def prepare(self):
        vals={}
        if self.Id is not None:
            vals["Id"] = self.Id
        if self.IsDefault is not None:
            vals["IsDefault"] = self.IsDefault
        if self.Label is not None:
            vals["Label"] = self.Label
        if self.Name is not None:
            vals["Name"] = self.Name
        if self.OptionIndex is not None:
            vals["OptionIndex"] = self.OptionIndex
        if self.PriceAdjustment is not None:
            vals["PriceAdjustment"] = self.PriceAdjustment
        if self.ProductOptionId is not None:
            vals["ProductOptionId"] = self.ProductOptionId
        if self.Sku is not None:
            vals["Sku"] = self.Sku
        # for eachitem in vals.keys():
        #     # Since I cannot currently deal well with unicode, I must exclude it from writing to csv
        #     if type('str')==type(vals[eachitem]):
        #         for eachchr in vals[eachitem]:
        #             if ord(eachchr)>128:
        #                 vals[eachitem]=vals[eachitem].replace(eachchr, 'replaced')
        return vals

    def register(self):
        if self not in productoptvalues:
            productoptvalues.append(self)

class ProductOption(object):
    global productoptions
    if 'productoptions' not in globals():
        productoptions = []

    def __init__(self,values):
        self.values=values
        self.internalid=id_generator()
        if "AllowSpaces" in values.keys():
            self.AllowSpaces=values["AllowSpaces"]
        else:
            self.AllowSpaces=None

        if "CanContain" in values.keys():
            self.CanContain=values["CanContain"]
        else:
            self.CanContain=None

        if "CanEndWith" in values.keys():
            self.CanEndWith=values["CanEndWith"]
        else:
            self.CanEndWith=None

        if "CanStartWith" in values.keys():
            self.CanStartWith=values["CanStartWith"]
        else:
            self.CanStartWith=None

        if "Id" in values.keys():
            self.Id=values["Id"]
        else:
            self.Id=None

        if "IsRequired" in values.keys():
            self.IsRequired=values["IsRequired"]
        else:
            self.IsRequired=None

        if "Label" in values.keys():
            self.Label=values["Label"]
        else:
            self.Label=None

        if "MaxChars" in values.keys():
            self.MaxChars=values["MaxChars"]
        else:
            self.MaxChars=None

        if "MinChars" in values.keys():
            self.MinChars=values["MinChars"]
        else:
            self.MinChars=None

        if "Name" in values.keys():
            self.Name=values["Name"]
        else:
            self.Name=None

        if "OptionType" in values.keys():
            self.OptionType=values["OptionType"]
        else:
            self.OptionType=None

        if "Order" in values.keys():
            self.Order=values["Order"]
        else:
            self.Order=None

        if "ProductId" in values.keys():
            self.ProductId=values["ProductId"]
        else:
            self.ProductId=None

        if "TextMessage" in values.keys():
            self.TextMessage=values["TextMessage"]
        else:
            self.TextMessage=None
        self.optionvalues=[]

    def getid(self):
        """Doing functionality like this allows things to be
        saved by a unique id, even if there is not one available
        """
        if self.Id is None:
            return self.internalid
        else:
            return self.Id

    def prepare(self):
        vals={}
        if self.AllowSpaces is not None:
            vals["AllowSpaces"] = self.AllowSpaces
        if self.CanContain is not None:
            vals["CanContain"] = self.CanContain
        if self.CanEndWith is not None:
            vals["CanEndWith"] = self.CanEndWith
        if self.CanStartWith is not None:
            vals["CanStartWith"] = self.CanStartWith
        if self.Id is not None:
            vals["Id"] = self.Id
        if self.IsRequired is not None:
            vals["IsRequired"] = self.IsRequired
        if self.Label is not None:
            vals["Label"] = self.Label
        if self.MaxChars is not None:
            vals["MaxChars"] = self.MaxChars
        if self.MinChars is not None:
            vals["MinChars"] = self.MinChars
        if self.Name is not None:
            vals["Name"] = self.Name
        if self.OptionType is not None:
            vals["OptionType"] = self.OptionType
        if self.Order is not None:
            vals["Order"] = self.Order
        if self.ProductId is not None:
            vals["ProductId"] = self.ProductId
        if self.TextMessage is not None:
            vals["TextMessage"] = self.TextMessage
        return vals

    def register(self):
        if self not in productoptions:
            productoptions.append(self)

class ISServer:
    def __init__(self, infusionsoftapp, infusionsoftAPIKey):
        self.infusionsoftapp=infusionsoftapp
        self.infusionsoftAPIKey=infusionsoftAPIKey
        self.appurl = "https://" + self.infusionsoftapp + ".infusionsoft.com:443/api/xmlrpc"
        self.connection = xmlrpclib.ServerProxy(self.appurl)

    ########################################################
    ## Methods to get records from various tables
    ##
    ##
    def getMatchingRecords(self, tableName, criteria, desiredFields=None, orderedBy=None):
        """Search at table by criteria
        """
        return self.getAllRecords(tableName, searchCriteria=criteria, interestingData=desiredFields, orderedBy=orderedBy)
    def getTagCats(self):
        return self.getAllRecords("ContactGroupCategory")
    def getAllTags(self):
        return self.getAllRecords("ContactGroup")
    def getAllProductCats(self):
        return self.getAllRecords("ProductCategory")
    def getAllProducts(self):
        return self.getAllRecords("Product")
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
                for eachbit in interestingData:   # this should be records.append(zip(interestingData, each)) perhaps
                    if not each.has_key(eachbit):   # TODO: research THIS
                        each[eachbit]=None
                    thisRecord[eachbit] = each[eachbit]
                records.append(thisRecord)
            if not(len(listOfDicts)==1000):
                break
            p+=1
        return records

    ########################################################
    ## Methods to create records
    ##
    def cnp(self, productValues):
        return self.createNewRecord('Product', productValues)
    def createNewRecord(self, table, recordvalues):
        return self.connection.DataService.add(self.infusionsoftAPIKey, table, recordvalues)

    ########################################################
    ## Methods to updating existing records
    ##
    def updateRecord(self, tableName, recordId, updateValues):
        return self.connection.DataService.update(self.infusionsoftAPIKey, tableName, recordId, updateValues)

    ########################################################
    ## Methods to get meta-data about records
    def getCount(self, tableName, query):
        return self.connection.DataService.count(self.infusionsoftAPIKey, tableName, query)
    def verifyConnection(self):
        try:
            listOfDicts=self.connection.DataService.query(self.infusionsoftAPIKey, "User", 1000, 0,{},["Email"],"Email",True)
            return True
        except:
            return False

def buildCategories(force=False):
    global productCatagories
    global server
    global tables
    if (len(productCatagories)==0 or force):
        allCategories=server.getAllRecords('ProductCategory', tables['ProductCategory'])
        catHold=[]
        for eachCategory in allCategories:
            thisCat = productCat(eachCategory['CategoryDisplayName'])
            thisCat.Id=eachCategory['Id']
            if eachCategory["ParentId"] is not None:
                thisCat.parent=eachCategory["ParentId"]
            if eachCategory["CategoryImage"] is not None:
                thisCat.CategoryImage=eachCategory["CategoryImage"]
            if eachCategory["CategoryImage"] is not None:
                thisCat.order=eachCategory["CategoryImage"]
            catHold.append(thisCat)
        for eachCat in [cat for cat in catHold if cat.parent in[None,0]]:
            eachCat.register()
        while True:
            repeat=False
            for eachCategory in catHold:
                try:
                    eachCategory.register()
                except KeyError:
                    # print KeyError.args
                    # print KeyError.message
                    repeat=True
            if not repeat:
                break

def getBuildRemote(force=False):
    global server
    server = ISServer(pw.passwords['appname'], pw.passwords['apikey'])
    global remotevalues

    tablesneeded={}
    tablesneeded['Product']=["Id", "ProductName", "Sku"]
    tablesneeded['ProductCategory']=['CategoryDisplayName', 'Id', 'ParentId']
    tablesneeded['ProductCategoryAssign']=["Id", "ProductCategoryId", "ProductId"]
    tablesneeded['ProductOptValue']=['Id', 'Name', 'ProductOptionId', 'Sku']
    tablesneeded['ProductOption']=['Id', 'Label', 'Name', 'ProductId']

    remotevalues={}

    remotevalues['Product']={}
    remotevalues['Product']["Id"]={}
    remotevalues['Product']["ProductName"]={}
    remotevalues['Product']["Sku"]={}

    remotevalues['ProductCategory']={}
    remotevalues['ProductCategory']['CategoryDisplayName']={}
    remotevalues['ProductCategory']['Id']={}
    remotevalues['ProductCategory']['ParentId']={}

    remotevalues['ProductCategoryAssign']={}
    remotevalues['ProductCategoryAssign']["Id"]={}
    remotevalues['ProductCategoryAssign']["ProductCategoryId"]={}
    remotevalues['ProductCategoryAssign']["ProductId"]={}

    remotevalues['ProductOptValue']={}
    remotevalues['ProductOptValue']['Id']={}
    remotevalues['ProductOptValue']['Name']={}
    remotevalues['ProductOptValue']['ProductOptionId']={}
    remotevalues['ProductOptValue']['Sku']={}

    remotevalues['ProductOption']={}
    remotevalues['ProductOption']['Id']={}
    remotevalues['ProductOption']['Label']={}
    remotevalues['ProductOption']['Name']={}
    remotevalues['ProductOption']['ProductId']={}

    for eachtable in tablesneeded.keys():
        with open('C:\\users\\jeremiah.marks\\desktop\\portable python 2.7.6.1\\' + eachtable + eachtable + ".csv", 'wb') as outfile:
            thiswriter=csv.DictWriter(outfile, tables[eachtable])
            thiswriter.writeheader()
            if 'Product' == eachtable:
                objectType=Product
            if 'ProductCategory' == eachtable:
                objectType=ProductCategory
            if 'ProductCategoryAssign' == eachtable:
                objectType=ProductCategoryAssign
            if 'ProductOptValue' == eachtable:
                objectType=ProductOptValue
            if 'ProductOption' == eachtable:
                objectType=ProductOption
            tabledata = server.getAllRecords(eachtable)
            for eachrecord in tabledata:
                eachRecordObject=objectType(eachrecord)
                thesevalues=eachRecordObject.prepare()
                holder={}
                for eachkey in thesevalues.keys():
                    tmps=''
                    if type(u'') is not type(thesevalues[eachkey]):
                        for eachletter in str(thesevalues[eachkey]):
                            if ord(eachletter)>127:
                                print eachletter, ord(eachletter), 'Letter Dropped'
                            else:
                                tmps+=eachletter
                    else:
                        print eachkey, thesevalues[eachkey][0:50]
                    holder[eachkey] =  tmps
                thiswriter.writerow(thesevalues)
                for eachidentifier in tablesneeded[eachtable]:
                    if eachidentifier in thesevalues.keys():
                        remotevalues[eachtable][eachidentifier][thesevalues[eachidentifier]]=eachRecordObject
            outfile.close()

def getCatId(pathToCat):
    global productCatagories
    global server
    buildCategories()
    checkPath = '/'+pathToCat
    # if (checkPath[0] != '/'):
    #     checkPath = '/' + pathToCat
    if pathToCat in productCatagories.keys():
        return productCatagories[pathToCat].Id
    else:
        pathData=pathToCat.rsplit('/',1)
        if len(pathData)==1:
            thisCat = productCat(pathData[0])
        else:
            thisCat = productCat(pathData[1])
            thisCat.parent=getCatId(pathData[0])
        thisCat.Id=server.createNewRecord('ProductCategory', thisCat.prepare())
        thisCat.register()
        return thisCat.Id

def getCatAssiggnId(productCatAssRecord):
    global server
    global tables
    matchingRecords=server.getMatchingRecords( "ProductCategoryAssign", productCatAssRecord.prepare(), tables["ProductCategoryAssign"])
    if len(matchingRecords)>0:
        return matchingRecords[0]["Id"]
    else:
        return server.createNewRecord("ProductCategoryAssign", productCatAssRecord.prepare())

def processImport(productsfile=pw.passwords['inputfilepath']):

    global server
    global products
    global productCatagories
    server = ISServer(pw.passwords['appname'], pw.passwords['apikey'])

    # badpatterns holds different patterns that break parsing
    #
    # badpatterns

    t='temp value'
    r='replacement value'
    badpatterns={}
    badpatterns['\\,'] = {}
    badpatterns['\\,'][t]="__comma"
    badpatterns['\\,'][r]=", "
    badpatterns['= ']={}
    badpatterns['= '][t]='eq_sp'
    badpatterns['= '][r]="= "
    badpatterns[', ']={}
    badpatterns[', '][t]='com_sp'
    badpatterns[', '][r]=", "



    getBuildRemote()
    thisProduct=None
    with open(productsfile) as datas:
        reader = csv.DictReader(datas)
        filefields=reader.fieldnames
        for row in reader:
            thisrow={}
            for eachheading in filefields:
                thisrow[eachheading] = row[eachheading].strip(" \n")
            if (len(thisrow["Name"]) == 0) or (len(thisrow["Name"])>0 and thisrow["Name"][0]=="["):
                #This indicates that it is not a product
                if (thisrow["Price"]==""):
                    # If the price column is empty then that
                    # will indicate that this is a option
                    # not a pricing rule
                    thisProduct.optionrows.append(thisrow)
                    # Appending the row to the product object
                    # Is probably not needed at all, but it
                    # is only a memory hit and should not
                    # meaningfully impact processing ability
                    if thisProduct.optionsSettings is None:
                        thisProduct.optionsSettings={}
                    thisnamecol = thisrow['Name']
                    # Now that we have the Name columns
                    # pulled out to parse, we are going to
                    # Replace the values that are giving us
                    # issues during the parse
                    for eachpattern in badpatterns.keys():
                        thisnamecol = thisnamecol.replace(eachpattern, badpatterns[eachpattern][t])

                    while len(thisnamecol)>0:
                        thisnamecol=thisnamecol[thisnamecol.find(']')+1:]
                        if thisnamecol.count('[')>0:
                            thisoptionvalue=thisnamecol[:thisnamecol.find('[')].strip(',\n ')
                            thisnamecol=thisnamecol[thisnamecol.find('['):]
                        else:
                            thisoptionvalue=thisnamecol.strip(',\n ')
                            thisnamecol=''

                        theseoptions = thisoptionvalue.split(',')
                        for eachpair in theseoptions:
                            eqcount = eachpair.count('=')
                            if eqcount != 1:
                                # Ya broke it
                                print "You broke it!\t", thisrow, eachpair
                            else:
                                optionname, optionvalue = eachpair.split("=")
                                optionvalue = optionvalue.split(':')[0]
                                for eachpart in [optionname, optionvalue]:
                                    # Now that we have the actual values and names
                                    # Let's put the final replacement values
                                    # back for the chars we replaced earlier.
                                    for eachpattern in badpatterns.keys():
                                        eachpart=eachpart.replace(badpatterns[eachpattern][t], badpatterns[eachpattern][r])
                                    if optionname not in thisProduct.optionsSettings.keys():
                                        thisProduct.optionsSettings[optionname] = set()
                                        thisoptionvalues={}
                                        thisoptionvalues['Name']=optionname
                                        thisoptionvalues['IsRequired'] = '1'
                                        thisoptionvalues['Label'] = optionname
                                        thisoptionvalues['OptionType'] = 'FixedList'
                                        thisoptionvalues['Order'] = len(thisProduct.options)
                                        thisoptionvalues['ProductId'] = thisProduct.getid()
                                        ###################################################
                                        ## Since we have the values collected, we can
                                        ## go ahead and query the server to see if this option
                                        ## exists.  An option will be considered the same
                                        ## option if it has the same name and product ID
                                        ## of another option
                                        ###################################################
                                        matchingRecords = server.getMatchingRecords("ProductOption", {'Name': thisoptionvalues['Name'], 'ProductId': thisProduct.getid() }, ['Id'])
                                        if len(matchingRecords)>0:
                                            thisoptionvalues['Id']=matchingRecords[0]['Id']
                                        else:
                                            # It does not exist, lets create it
                                            thisoptionvalues['Id']=server.createNewRecord("ProductOption", thisoptionvalues)
                                        thispo = ProductOption(thisoptionvalues)
                                        thisProduct.options[optionname]=thispo
                                    thisProduct.optionsSettings[optionname].add(optionvalue)
                                    thispo = thisProduct.options[optionname]
                                    optval={}
                                    optval["Name"] = optionvalue
                                    optval["Label"] = optionvalue
                                    if thisrow['SKU'] and len(thisrow['SKU'])>0:
                                        optval['Sku'] = thisrow['SKU']
                                    optval['ProductOptionId']=thispo.getid()
                                    optval['OptionIndex']=len(thispo.optionvalues)
                                    matchingRecords = server.getMatchingRecords( "ProductOptValue", {"Name": optval["Name"], "ProductOptionId": optval['ProductOptionId']}, ['Id'])
                                    if len(matchingRecords)>0:
                                        optval['Id'] = matchingRecords[0]['Id']
                                    else:
                                        optval['Id'] = server.createNewRecord("ProductOptValue", optval)
                                    thisval = ProductOptValue(optval)
                                    thispo.optionvalues.append(thisval)
                                    ############################################################
                                    ## Now that we have the option value created and handy    ##
                                    ## We will take this opportunity to see if it is          ##
                                    ## created on the server.  If it is not we will create it.##
                                    ############################################################
                else:
                    # Basically, if there is something in the
                    # Price column and the Product name starts
                    # with a '[' then this is a pricing rule
                    # 
                    thisnamecol = thisrow['Name']
                    thispricecol = thisrow['Price']
                    thisskucol = thisrow["SKU"]
                    for eachpattern in badpatterns.keys():
                        thisnamecol = thisnamecol.replace(eachpattern, badpatterns[eachpattern][t])

                    while len(thisnamecol)>0:
                        thisnamecol=thisnamecol[thisnamecol.find(']')+1:]
                        if thisnamecol.count('[')>0:
                            thisoptionvalue=thisnamecol[:thisnamecol.find('[')].strip(',\n ')
                            thisnamecol=thisnamecol[thisnamecol.find('['):]
                        else:
                            thisoptionvalue=thisnamecol.strip(',\n ')
                            thisnamecol=''

                        theseoptions = thisoptionvalue.split(',')
                        for eachpair in theseoptions:
                            eqcount = eachpair.count('=')
                            if eqcount != 1:
                                # Ya broke it
                                print "You broke it!\t", thisrow, eachpair
                            else:
                                optionname, optionvalue = eachpair.split("=")
                                optionvalue = optionvalue.split(':')[0]
                                for eachpart in [optionname, optionvalue]:
                                    for eachpattern in badpatterns.keys():
                                        eachpart=eachpart.replace(badpatterns[eachpattern][t], badpatterns[eachpattern][r])
                                thisoptionval={}
                                thisoptionval["Name"] = optionname
                                if optionname not in thisProduct.options.keys():
                                    thisProduct.options[optionname]=ProductOption({"Name": optionname})
                                thisoptionval["ProductOptionId"] = thisProduct.options[optionname].getid()
                                matchingRecords = server.getMatchingRecords("ProductOptValue", thisoptionval, ['Id'])
                                if len(matchingRecords)>0:
                                    thisoptionval.update(matchingRecords[0])
                                else:
                                    if len(thispricecol) > 0:
                                        thisprice = thispricecol[thispricecol.find(']')+1:]
                                        thispriceaction =  thispricecol[1:thisprice.find(']')]
                                        thispricecol = ""
                                    if len(thisskucol) > 0:
                                        thissku = thisskucol
                                        thisskucol = ""
                                        thisoptionval["Sku"] = thissku
                                    thisoptionval["OptionIndex"] = len(thisProduct.optionsPriceChange)
                                    if thispriceaction == "ADD":
                                        thisoptionval["PriceAdjustment"] = thisprice
                                    elif thispriceaction == "REMOVE":
                                        thisoptionval["PriceAdjustment"] = "-"+thisprice
                                    elif thispriceaction == "FIXED":
                                        targetprice = float(thisprice)
                                        thisprice = str(targetprice - float(thisProduct.ProductPrice))
                                        thisoptionval["PriceAdjustment"] = thisprice
                                    thisoptionval["Label"] = optionvalue
                                    thisobject=ProductOptValue(thisoptionval)
                                    print "\n\n\n\n"
                                    print thisobject.prepare()
                                    thisoptionval["Id"]=server.createNewRecord("ProductOptValue", thisobject.prepare())
                                thisProduct.optionsPriceChange[thisoptionval["Id"]]=ProductOptValue(thisoptionval)
                    thisProduct.pricingrows.append(thisrow)
            else:
                #this is a product
                if thisProduct is not None:
                    # This is to save the just completed product.
                    products.append(thisProduct)
                thisProduct = Product({"ProductName" : thisrow["Name"].strip(' \n')})
                thisProduct.Status='1'
                thisProduct.rowdata.append(thisrow)
                for column in ["GPS Category", "Brand", "Category String"]:
                    thisProduct.catStrings.append(thisrow[column])
                if thisrow["SKU"]:
                    thisProduct.Sku = thisrow["SKU"]
                if thisrow['Description']:
                    thisProduct.Description=row['Description']
                if thisrow["Price"]:
                    thisProduct.ProductPrice = thisrow["Price"]
                if thisrow["Product Images"]:
                    thisProduct.imageStrings.append(row["Product Images"])
                if thisrow["Meta Description"]:
                    thisProduct.ShortDescription = thisrow["Meta Description"]
                if thisrow["Product Images"]:
                    imageStrings=thisrow["Product Images"].split("|")
                    for eachS in imageStrings:
                        for eachVal in eachS.split(","):
                            if "Product Image URL: " in eachVal:
                                thisProduct.images.append(eachVal.replace("Product Image URL: ","").strip())
                ############################################
                ## First we will check and see if this product
                ## already exists.  While there are reasons to use
                ## something more robust than only the name
                ## it is not needed currently, and I need to
                ## get this completed.
                ##
                ## Basically, though, what this will do is see if the product is already created.  If it is not
                ## It will then create the product.
                ##
                ## Basically from here on, the ID from the product should actually be a real product
                ## id.
                if thisProduct.ProductName.lower().strip(' \n') in remotevalues['Product']["ProductName"].keys():
                    thisProduct.Id = remotevalues['Product']["ProductName"][thisProduct.ProductName.lower().strip(' \n')].Id
                else:
                    thisProduct.Id = server.cnp(thisProduct.prepare())
                values=thisProduct.prepare()
                print values['Sku'], values['ProductName']


                # if thisProduct.images:
                #     productImage.addImageToProduct(thisProduct.Id, thisProduct.images[0])
                # thisProduct.Id=iditerator.next()
    # we need to save the last product somewhere after it gets created.
    products.append(thisProduct)

    # Now that all of the rows have been processed into their
    # appropriate product object, lets take those apart and
    # put them together again.
    # for eachproduct in products:
    #     # I am sure that there is a much better way to do this than what I am about to do.
    #     # Basically, though, if you are doing things right, you should only need to go
    #     ## through all of the products one time.  This will
    #     for eachoption in eachproduct.optionrows:
    #         if eachproduct.optionsSettings is None:
    #             eachproduct.optionsSettings={}
    #         thisnamecol=eachoption['Name']
    #         while len(thisnamecol)>0:
    #             thisnamecol=thisnamecol[thisnamecol.find(']')+1:]
    #             # This Basically strips off the first option class tag
    #             # thing
    #             if thisnamecol.count('[')>0:
    #                 # basically if there is another option tag
    #                 # thing we are going to deal with
    #                 thisoptionvalue=thisnamecol[:thisnamecol.find('[')].strip(',\n ')
    #                 thisnamecol=thisnamecol[thisnamecol.find('['):]
    #             else:
    #                 thisoptionvalue=thisnamecol.strip(',\n ')
    #                 thisnamecol=''
    #             ############################################
    #             ## thisoptionvalue should be expected to be a coma separated
    #             ## list of product options and option values
    #             ##
    #             if '\\,' in thisoptionvalue:
    #                 thisoptionvalue = thisoptionvalue.replace('\\,', '\\coma')
    #                 ########################################
    #                 ## This is because we are going to split the
    #                 ##  string with a coma and we do not want to lose
    #                 ##  values when we do that.
    #             theseoptions=thisoptionvalue.split(',')
    #             ############################################
    #             ## theseoptions should look like this:
    #             ## theseoptions =[
    #             ##                 "op1=val",
    #             ##                 "op2=val",
    #             ##                 "op3=val",
    #             ##               ]
    #             for eachpair in theseoptions:
    #                 eachpair.replace('\\coma', '\\,')
    #                 # as a note, these pairs should still be
    #                 # joined with a "="
    #                 eqcount=eachpair.count("=")
    #                 if eqcount==0:
    #                     print "this pair sucked ", eachpair
    #                 elif eqcount>1:
    #                     print "this pair has more then one! ", eachpair
    #                 else:
    #                     optionname, optionvalue = eachpair.split("=")
    #                     optionvalue = optionvalue.split(':')[0]
    #                     if optionname not in eachproduct.optionsSettings.keys():
    #                         eachproduct.optionsSettings[optionname] = set()
    #                         thisoptionvalues={}
    #                         thisoptionvalues['Name']=optionname
    #                         thisoptionvalues['IsRequired'] = '1'
    #                         thisoptionvalues['Label'] = optionname
    #                         thisoptionvalues['OptionType'] = 'FixedList'
    #                         thisoptionvalues['Order'] = len(eachproduct.options)
    #                         thisoptionvalues['ProductId'] = eachproduct.getid()
    #                         thispo = ProductOption(thisoptionvalues)
    #                         eachproduct.options[optionname]=thispo
    #                     eachproduct.optionsSettings[optionname].add(optionvalue)
    #                     thispo = eachproduct.options[optionname]
    #                     optval={}
    #                     optval["Name"]=optionvalue
    #                     optval["Label"]=optionvalue
    #                     if eachoption['SKU'] and len(eachoption['SKU'])>0:
    #                         optval['Sku'] = eachoption['SKU']
    #                     else:
    #                         optval['Sku']=None
    #                     optval['ProductOptionId']=thispo.getid()
    #                     optval['OptionIndex']=len(thispo.optionvalues)
    #                     thispo.optionvalues.append(ProductOptValue(optval))
    return products


if __name__ == '__main__':
    server=ISServer(pw.passwords['appname'], pw.passwords['apikey'])
    processImport()





# OptionValue
# self.Id=values["Id"]
# self.IsDefault=values["IsDefault"]
# self.Label=values["Label"]
# self.Name=values["Name"]
# self.OptionIndex=values["OptionIndex"]
# self.PriceAdjustment=values["PriceAdjustment"]
# self.ProductOptionId=values["ProductOptionId"]
# self.Sku=values["Sku"]












                    #             optionname, optionvalue = optionname[0],optionname[1]
                    #         if thisProduct.optionsSettings is None:
                    #             thisProduct.optionsSettings={}
                    #         if optionname not in thisProduct.optionsSettings.keys():
                    #             thisProduct.optionsSettings[optionname] = set()
                    #         thisProduct.optionsSettings[optionname].add(optionvalue)


# Option                                # OptionValue
# if self.AllowSpaces is not None:      # self.Id=values["Id"]
# if self.CanContain is not None:       # self.IsDefault=values["IsDefault"]
# if self.CanEndWith is not None:       # self.Label=values["Label"]
# if self.CanStartWith is not None:     # self.Name=values["Name"]
# if self.Id is not None:               # self.OptionIndex=values["OptionIndex"]
# if self.IsRequired is not None:       # self.PriceAdjustment=values["PriceAdjustment"]
# if self.Label is not None:            # self.ProductOptionId=values["ProductOptionId"]
# if self.MaxChars is not None:         # self.Sku=values["Sku"]
# if self.MinChars is not None:
# if self.Name is not None:
# if self.OptionType is not None:
# if self.Order is not None:
# if self.ProductId is not None:
# if self.TextMessage is not None:
