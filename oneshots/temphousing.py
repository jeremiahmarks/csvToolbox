#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-16 19:15:29
# @Last Modified 2015-06-17
# @Last Modified time: 2015-06-17 03:59:46

import random
import string
import xmlrpclib
import urllib
import csv
import productImage
import productObjects
import my_pw as pw

global products

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
        if 'products' not in globals():
            print "Products now exist as an empty set"
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
        self.categories=None
        self.catStrings=[]
        self.images=[]
        self.imageStrings=[]
        self.options=None
        self.optionsSettings=None
        self.optionsPriceChange={}
        self.register()

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
        for eachitem in vals.keys():
            # Since I cannot currently deal well with unicode, I must exclude it from writing to csv
            if type('str')==type(vals[eachitem]):
                for eachchr in vals[eachitem]:
                    if ord(eachchr)>127:
                        print "Error " + str(vals[eachitem])
                        vals[eachitem]=vals[eachitem].replace(eachchr, 'replaced')
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
        for eachitem in vals.keys():
            # Since I cannot currently deal well with unicode, I must exclude it from writing to csv
            if type(u'str')==type(vals[eachitem]):
                for eachchr in vals[eachitem]:
                    if ord(eachchr)>0:
                        print eachchr
                    if ord(eachchr)>127:
                        print "Error " + str(ord(eachchr))
                        vals[eachitem]=vals[eachitem].replace(eachchr, 'replaced')
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
    def prepare(self):
        vals={}
        if self.Id is not None:
            vals["Id"] = self.Id
        if self.ProductCategoryId is not None:
            vals["ProductCategoryId"] = self.ProductCategoryId
        if self.ProductId is not None:
            vals["ProductId"] = self.ProductId
        for eachitem in vals.keys():
            # Since I cannot currently deal well with unicode, I must exclude it from writing to csv
            if type('str')==type(vals[eachitem]):
                for eachchr in vals[eachitem]:
                    if ord(eachchr)>127:
                        print "Error " + str(vals[eachitem])
                        vals[eachitem]=vals[eachitem].replace(eachchr, 'replaced')
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
        for eachitem in vals.keys():
            # Since I cannot currently deal well with unicode, I must exclude it from writing to csv
            if type('str')==type(vals[eachitem]):
                for eachchr in vals[eachitem]:
                    if ord(eachchr)>128:
                        vals[eachitem]=vals[eachitem].replace(eachchr, 'replaced')
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
        return getAllRecords(tableName, searchCriteria=criteria, interestingData=desiredFields, orderedBy=orderedBy)
    def getTagCats(self):
        return getAllRecords("ContactGroupCategory")
    def getAllTags(self):
        return getAllRecords("ContactGroup")
    def getAllProductCats(self):
        return getAllRecords("ProductCategory")
    def getAllProducts(self):
        return getAllRecords("Product")
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
    server = ISServer(pw.pw['appname'], pw.pw['apikey'])
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
        with open('/home/jlmarks/' + eachtable + eachtable + ".csv", 'wb') as outfile:
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

def processImport(productsfile=pw.pw['inputfilepath']):

    global server
    global products
    global productCatagories
    server = ISServer(pw.pw['appname'], pw.pw['apikey'])

    getBuildRemote()

    thisProduct=None
    with open(productsfile) as datas:
        reader = csv.DictReader(datas)

        for row in reader:
            if (len(row["Name"])>0 and row["Name"][0]=="["):
                #This indicates that it is not a product
                if (row["Price"]==""):
                    # If the price value is blank, this means
                    # that it is an option, not a pricing rule
                    mycopy=row['Name']
                    while len(mycopy) > 0:
                        mycopy=mycopy[ mycopy.find(']') + 1 : ]
                        if '[' in mycopy:
                            thisoption=mycopy[:mycopy.find('[')]
                            mycopy=mycopy[mycopy.find('['):]
                        else:
                            thisoption=mycopy
                            mycopy=mycopy[0:0]
                            # Since we are using slices, we may
                            # as well kill a string with a slice
                        #Theoretically we should only have a comma separated list of different variations 
                        # on available options.
                        for eachoptionvaluepair in mycopy.split(','):
                            # optionname, optionvalue = eachoptionvaluepair.split("=")
                            optionname = eachoptionvaluepair.split("=")
                            if len(optionname)==1:
                                optionname=optionname[0]
                            else:
                                optionname, optionvalue = optionname[0],optionname[1]
                            if thisProduct.optionsSettings is None:
                                thisProduct.optionsSettings={}
                            if optionname not in thisProduct.optionsSettings.keys():
                                thisProduct.optionsSettings[optionname] = set()
                            thisProduct.optionsSettings[optionname].add(optionvalue)
                else:
                    # This is a pricing rule
                    changetype=row["Price"][1:row["Price"].find(']')]
                    priceChange = row["Price"][row["Price"].find(']')+1:]
                    optionChoice, optionChoiceValue = row["Name"][4:].split("=",1)
                    if thisProduct.optionsPriceChange is None:
                        thisProduct.optionsPriceChange={}
                    if optionChoice not in thisProduct.optionsPriceChange.keys():
                        thisProduct.optionsPriceChange[optionChoice]={}
                    thisProduct.optionsPriceChange[optionChoice][optionChoiceValue] = priceChange
                    thisProduct.optionsPriceChange[optionChoice][changetype]=changetype
            else:
                #this is a product
                if thisProduct is not None:
                    # This is to save the just completed product. 
                    # so that we can access it later, and assign its variable to 
                    # a different object. (Okay, really assign a different object
                    # to this variable ) We do not want to call it before the first
                    # product is created, hence the if to check.
                    products.append(thisProduct)
                thisProduct = Product({"ProductName" : row["Name"]})
                for column in ["GPS Category", "Brand", "Category String"]:
                    thisProduct.catStrings.append(row[column])
                if row["SKU"]:
                    thisProduct.Sku = row["SKU"]
                if row['Description']:
                    thisProduct.Description=row['Description']
                if row["Price"]:
                    thisProduct.ProductPrice = row["Price"]
                if row["Product Images"]:
                    thisProduct.imageStrings.append(row["Product Images"])
                if row["Meta Description"]:
                    thisProduct.ShortDescription = row["Meta Description"]
                if row["Product Images"]:
                    imageStrings=row["Product Images"].split("|")
                    for eachS in imageStrings:
                        for eachVal in eachS.split(","):
                            if "Product Image URL: " in eachVal:
                                thisProduct.images.append(eachVal.replace("Product Image URL: ","").strip())
                ############################################
                ############################################
                ##
                ##  I need to make sure that I am checking
                ## for existing product before just creating
                ## one
                ##
                ##  Actually, thinking about it, it makes more
                ##  Sense to just pull everything down first

                ## Now to check for the product and see if it exists

                if thisProduct.ProductName in remotevalues['Product']["ProductName"].keys():
                    thisProduct.Id = remotevalues['Product']["ProductName"][thisProduct.ProductName].Id
                else:
                    thisProduct.Id = server.cnp(thisProduct.prepare())
                values=thisProduct.prepare()
                print thisProduct.getPublicPage(server.infusionsoftapp)
                print thisProduct.getInternalPage()
                # if thisProduct.images:
                #     productImage.addImageToProduct(thisProduct.Id, thisProduct.images[0])
                # thisProduct.Id=iditerator.next()
    # we need to save the last product somewhere after it gets created. 
    products.append(thisProduct)
    return products






    #                 optionString=row["Name"]
    #                 while(len(optionString)>0):
    #                     optionString = optionString[4:]
    #                     # This should remove the original tag
    #                     optionName, optionString = optionString.split("=",1)
    #                     if thisProduct.optionsSettings is None:
    #                         thisProduct.optionsSettings={}
    #                     if optionName not in thisProduct.optionsSettings.keys():
    #                         thisProduct.optionsSettings[optionName] = set()
    #                     try:
    #                         optionsValue, optionString = optionString.split(",",1)
    #                     except ValueError:
    #                         optionsValue = optionString
    #                         optionString = ""
    #                     thisProduct.optionsSettings[optionName.replace('-_-',",")].add(optionsValue.replace('-_-',","))
    # ####
    # ##
    # # Products have been created and have their optionsp set up.
    # # Let's create the actual optionsp.
    # for eachProduct in products:
    #     if eachProduct.optionsSettings:
    #         if eachProduct.options is None:
    #             eachProduct.options = {}
    #         counter=0
    #         for eachOption in eachProduct.optionsSettings.keys():
    #             counter+=1
    #             thisOption = prodOption(eachProduct.Id)
    #             thisOption.name=eachOption
    #             thisOption.label = eachOption
    #             thisOption.required = 1
    #             thisOption.order = counter
    #             thisOption.optionType='FixedList'
    #             thisOption.Id = server.createNewRecord("ProductOption", thisOption.prepare())
    #             # thisOption.Id=iditerator.next()
    #             eachProduct.options[eachOption] = thisOption
    #             optionCounter=0
    #             for eachValue in eachProduct.optionsSettings[eachOption]:
    #                 optionCounter+=1
    #                 newOptionValue=prodOptVal(thisOption.Id)
    #                 newOptionValue.optionIndex=optionCounter
    #                 newOptionValue.label = eachValue
    #                 newOptionValue.isdefault=0
    #                 newOptionValue.name=eachValue
    #                 if eachOption in eachProduct.optionsPriceChange.keys():
    #                     if eachValue in eachProduct.optionsPriceChange[eachOption].keys():
    #                         newOptionValue.adjustment=eachProduct.optionsPriceChange[eachOption][eachValue]
    #                 newOptionValue.Id = server.createNewRecord("ProductOptValue", newOptionValue.prepare())
    #                 # newOptionValue.Id = iditerator.next()
    #                 thisOption.values.append(newOptionValue)
    #     # each product option has been created and assigned. 
    #     # lets take care of the categories.
    #     for eachString in eachProduct.catStrings:
    #         if eachProduct.categories is None:
    #             eachProduct.categories={}
    #         eachString.replace("\\/", " - ")
    #         for eachSubstring in eachString.split(";"):
    #             #The string should now be something like
    #             # ParentCat/ChildCat/grandChildCat
    #             thiscatid=getCatId(eachSubstring)
    #             thisAssignment=prodCatAss(eachProduct.Id, thiscatid)
    #             thisAssignment.Id=getCatAssiggnId(thisAssignment)
    #             eachProduct.categories[eachSubstring]=eachProduct.categories[int(thiscatid)]=thisAssignment
    #     for lastEachProduct in products:
    #         if lastEachProduct.images:
    #             print "uploading image from " + lastEachProduct.images[0]
    #             productImage.addImageToProduct(lastEachProduct.Id, lastEachProduct.images[0])
    # return products

if __name__ == '__main__':
    server=ISServer(pw.pw['appname'], pw.pw['apikey'])
    getBuildRemote()





































































# global temhousingqueue
# global temoptionqueue
# global localids
# localids=set()
# temhousingqueue={}
# temoptionqueue={}
# temhousingqueuecounter=0
# temoptionqueuecounter=0


# ############################################################
# ##
# ## Since we want this to be reusable,  we are going to add
# ## in a random unique id generator.  When working with the 
# ## api we will have ID numbers in place to check for things,
# ## we could hash the item, but that is a topic for another 
# ## day
# ##































# class temphousing(object):
#     """This is just a simple class. It gives you a location
#     to hold data. It will then process the data and crate the
#     appropriate records.
#     """
#     def __init__(self, productrow):
#         global temhousingqueue
#         global temhousingqueuecounter
#         temhousingqueuecounter+=1
#         temhousingqueue[temhousingqueuecounter]=self
#         self.productrow=productrow
#         self.childrow=0
#         self.optionsrows={}
#         self.pricingrulerows={}
#         self.options={}
#         self.processSelf()
#         self.houseid=id_generator()
#         self.Idset=False
#         self.getid()

#     def getid(self):
#         """Doing functionality like this allows things to be
#         saved by a unique id, even if there is not one available
#         """
#         return self.houseid

#     def addoptionsrow(self, optionsrow, rownum=None):
#         if rownum is None:
#             rownum=random.randint(500,500**2)
#         self.optionsrows[rownum]=(optionsrow)

#     def addpricingrulerow(self, pricingrulerow, rownum=None):
#         if rownum is None:
#             rownum=random.randint(500,500**2)
#         self.pricingrulerows[rownum]=(pricingrulerow)

#     def processSelf(self):
#         self.productValues={}

#         if len(self.productrow['SKU']) > 0:
#             # something exists in  'SKU',
#             self.productValues["Sku"] = self.productrow["SKU"]

#         if len(self.productrow['Allow Purchases']) > 0:
#             # something exists in  'Allow Purchases',
#             if self.productrow["Allow Purchases"] == "1":
#                 self.productValues['Status']='1'
#             else:
#                 self.productValues['Status']='0'

#         if len(self.productrow['Meta Description']) > 0:
#             # something exists in  'Meta Description',
#             self.productValues["ShortDescription"]=self.productrow['Meta Description']

#         if len(self.productrow['GPS Manufacturer Part Number']) > 0:
#             # something exists in  'GPS Manufacturer Part Number',
#             # check with email and verify how to process
#             # until then
#             pass

#         if len(self.productrow['Brand']) > 0:
#             # something exists in  'Brand',
#             # check if there is a category created callend
#             # "Brands". If there is not, create it.
#             # Create the category "Brands"/self.productrow['Brand']
#             # and assign self to that category
#             pass

#         if len(self.productrow['Product Images']) > 0:
#             # something exists in  'Product Images',
#             self.imagurl=self.productrow["Product Images"][self.productrow["Product Images"].find('URL:')+4: self.productrow["Product Images"].find(',',self.productrow["Product Images"].find('URL:'))]

#         if len(self.productrow['GPS Category']) > 0:
#             # something exists in  'GPS Category',
#             # check if there is a category created callend
#             # "GPS Category". If there is not, create it.
#             # Create the category "GPS Category"/self.productrow['GPS Category']
#             # and assign self to that category
#             pass

#         if len(self.productrow['Category String']) > 0:
#             # something exists in  'Category String',
#             # This breaks down all of the categories
#             # Process these as categories
#             ##
#             pass

#         if len(self.productrow['Product Files']) > 0:
#             # something exists in  'Product Files',
#             ##unknown
#             pass

#         if len(self.productrow['Option Set']) > 0:
#             # something exists in  'Option Set',
#             # potential categories or options related.
#             pass

#         if len(self.productrow['Description']) > 0:
#             # something exists in  'Description',
#             self.productValues["Description"]=self.productrow['Description']

#         if len(self.productrow['Price']) > 0:
#             self.productValues["ProductPrice"] = self.productrow['Price']

#         if len(self.productrow['Name']) > 0:
#             # something exists in  'Name'
#             self.productValues["ProductName"] = self.productrow['Name']

#     def processoptions(self):
#         for eachnum, eachoptionrow in enumerate(self.optionsrows):

#             self.options[eachnum]={}
#             if len(eachoptionrow['SKU']) > 0:
#                 # something exists in  'SKU',
#                 self.options[eachnum]['SKU']= eachoptionrow['SKU']

#             if len(eachoptionrow['Allow Purchases']) > 0:
#                 # something exists in  'Allow Purchases',
#                 self.options[eachnum]['Allow Purchases']= eachoptionrow['Allow Purchases']

#             if len(eachoptionrow['Meta Description']) > 0:
#                 # something exists in  'Meta Description',
#                 self.options[eachnum]['Meta Description']= eachoptionrow['Meta Description']

#             if len(eachoptionrow['GPS Manufacturer Part Number']) > 0:
#                 # something exists in  'GPS Manufacturer Part Number',
#                 # check with email and verify how to process
#                 # until then
#                 self.options[eachnum]['GPS Manufacturer Part Number']= eachoptionrow['GPS Manufacturer Part Number']

#             if len(eachoptionrow['Brand']) > 0:
#                 # something exists in  'Brand',
#                 # check if there is a category created callend
#                 # "Brands". If there is not, create it.
#                 # Create the category "Brands"/eachoptionrow['Brand']
#                 # and assign self to that category
#                 self.options[eachnum]['Brand']= eachoptionrow['Brand']

#             if len(eachoptionrow['Product Images']) > 0:
#                 # something exists in  'Product Images',
#                 self.options[eachnum]['Product Images']= eachoptionrow['Product Images']

#             if len(eachoptionrow['GPS Category']) > 0:
#                 # something exists in  'GPS Category',
#                 # check if there is a category created callend
#                 # "GPS Category". If there is not, create it.
#                 # Create the category "GPS Category"/eachoptionrow['GPS Category']
#                 # and assign self to that category
#                 self.options[eachnum]['GPS Category']= eachoptionrow['GPS Category']

#             if len(eachoptionrow['Category String']) > 0:
#                 # something exists in  'Category String',
#                 # This breaks down all of the categories
#                 # Process these as categories
#                 ##
#                 self.options[eachnum]['Category String']= eachoptionrow['Category String']

#             if len(eachoptionrow['Product Files']) > 0:
#                 # something exists in  'Product Files',
#                 ##unknown
#                 self.options[eachnum]['Product Files']= eachoptionrow['Product Files']

#             if len(eachoptionrow['Option Set']) > 0:
#                 # something exists in  'Option Set',
#                 # potential categories or options related.
#                 self.options[eachnum]['Option Set']= eachoptionrow['Option Set']

#             if len(eachoptionrow['Description']) > 0:
#                 # something exists in  'Description',
#                 self.options[eachnum]['Description']= eachoptionrow['Description']

#             if len(eachoptionrow['Price']) > 0:
#                 self.options[eachnum]['Price']= eachoptionrow['Price']

#             if len(eachoptionrow['Name']) > 0:
#                 # something exists in  'Name'
#                 # In an option, the "Name" is where the actual options are listed.
#                 # Their format is:
#                 #    [somecode]This Option=thisvalue:someimagedatapotentially, This Option=thisvalue:someimagedatapotentially, This Option=thisvalue:someimagedatapotentially, [SOMEID]Other Option=otherValue
#                 #
#                 # We are going to handle this by recursively stripping off everything to and 
#                 # including the first "]". We will then break off everything before the first '['
#                 # We will work with that string and allow the loop to handle the next iteration.
#                 mycopy=eachoptionrow['Name']
#                 while len(mycopy) > 0:
#                     mycopy=[mycopy.find(']')+1:]
#                     if '[' in mycopy:
#                         thisoption=mycopy[:mycopy.find('[')]
#                         mycopy=mycopy[mycopy.find('['):]
#                     else:
#                         thisoption=mycopy
#                         mycopy=mycopy[0:0]
#                         # Since we are using slices, we may
#                         # as well kill a string with a slice
#                     #Theoretically we should only have a comma separated list of different variations 
#                     # on available options.
#                     for eachoptionvaluepair in mycopy.split(','):
#                         optionname, optionvalue = eachoptionvaluepair.split("=")
#                         ############################################################################
#                         ############################################################################
#                         ############################################################################
#                         ## This is where you are.
#                         ## I will be back after writing a good place to house and
#                         ## sort the options
#                         ##
#                 self.options[eachnum]['Name']= eachoptionrow['Name']



# class temoption(object):

#     def __init__(self, optionname, ProductId):
#         global temoptionqueue
#         global temoptionqueuecounter
#         self.ProductId=ProductId
#         self.internalid=id_generator()
#         self.Name=optionname
#         self.Id=None
#         self.Idset=False
#         self.getid()

#     def getid(self):
#         """Doing functionality like this allows things to be
#         saved by a unique id, even if there is not one available
#         """
#         if self.Id is None:
#             return self.internalid
#         else:
#             return self.Id


# class temproduct(object):
#     """This class is meant as a way to store information about
#     a product as well as include the ability to notify child
#     objects of a status change.
#     """
#     def __init__(self, productName):
#         """
#         I expect that every product will have a name. If a 
#         product tries to get created without a name, we will
#         report in it ... maybe
#         """
#         self.categories={} # (This is intended to store categories that the 
#                            #  product is assigned to  
#                            #        like self.categories["CategoryId"]=categoryPath)
#         # Id           This will ID a unique product    
#         # ProductName  This in conjunction with categories will define a unique category.
#         #       As a note, there can only be two products with the same name/Sku, one with no category
#         #       And one with a category.
#         # Sku          This may factor in to play.     
#         if productName is None:
#             return "This attempt was a failure"
#         self.ProductName=productName
#         self.internalid=id_generator()
#         self.Id=None
#         self.Idset=False
#         self.getid()


#     def getid(self):
#         """Doing functionality like this allows things to be
#         saved by a unique id, even if there is not one available
#         """
#         if self.Id is None:
#             return self.internalid
#         else:
#             return self.Id

#     def __eq__(self, other):
#         if self.getid()==other.getid():
#             return True
#         catsmatch= len(self.categories.keys())>0 is len(other.categories.keys())>0   # Basically, 
#         # this checks to see if both of the products have categories or if
#         # they both do not. Basically the statment says 
#         #               [T/F] is [T/F]
#         # and returns that.
#         namesmatch=self.ProductName.lower().strip(' \n') is other.ProductName.lower().strip(' \n')
#         return namesmatch and catsmatch








# ####################################################################################################
# ########        So, if you are reading down here, this is a place for my frequently used references
# ########
# ########           tables["ProductOptValue"]        tables["ProductOption"]
# ########           ["Id"                            ["AllowSpaces"
# ########           "IsDefault"                       "CanContain"
# ########           "Label"                           "CanEndWith"
# ########           "Name"                            "CanStartWith"
# ########           "OptionIndex"                     "Id"
# ########           "PriceAdjustment"                 "IsRequired"
# ########           "ProductOptionId"                 "Label"
# ########           "Sku"]                            "MaxChars"
# ########                                             "MinChars"
# ########                                             "Name"
# ########                                             "OptionType"
# ########                                             "Order"
# ########                                             "ProductId"
# ########                                             "TextMessage"]
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########
# ########