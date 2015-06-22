#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-20 22:11:09
# @Last Modified 2015-06-21
# @Last Modified time: 2015-06-21 20:18:17
############################################################
## ToDo: build a getproductid(Product()): function
############################################################
# Product Categories
# Product
# Product options
#   Product.Id
# Product option Values
#   ProductOption.Id
# Product Category assignments
#   Product.Id
#   ProductCategory.Id
import my_pw as pw
import csv
import datetime
import xmlrpclib
import string
import random

global server
global localobjects
localobjects={}
localids=set()
def id_generator(size=10, chars=string.ascii_uppercase):

    global localids
    thisid=''.join(random.choice(chars) for _ in range(size))
    while thisid in localids:
        thisid =''.join(random.choice(chars) for _ in range(size))
    localids.add(thisid)
    return thisid
# Product.Sku
# Product.Id
# Product.Status
# Product.ProductPrice
# Product.Description
# Product.ShortDescription
# Product.ProductName
# 
# ProductOption.Id
# ProductOption.IsRequired
# ProductOption.Label
# ProductOption.Name
# ProductOption.OptionType
# ProductOption.Order
# ProductOption.ProductId
# 
# ProductOptionValue.Id
# ProductOptionValue.IsDefault
# ProductOptionValue.Label
# ProductOptionValue.Name
# ProductOptionValue.OptionIndex
# ProductOptionValue.PriceAdjustment
# ProductOptionValue.ProductOptionId
# ProductOptionValue.Sku


# ppp=[allatonce.remoteTables['ProductOptValue'][k] for k in allatonce.remoteTables['ProductOptValue'].keys() if allatonce.remoteTables['ProductOptValue'][k]['Id']==8181]


############################################################
## These are the different columns on the tables that we need
## to interact with.
############################################################
tables={}
tables["Product"] = ["BottomHTML", "CityTaxable", "CountryTaxable", "Description", "HideInStore", "Id", "InventoryLimit", "InventoryNotifiee", "IsPackage", "LargeImage", "NeedsDigitalDelivery", "ProductName", "ProductPrice", "Shippable", "ShippingTime", "ShortDescription", "Sku", "StateTaxable", "Status", "Taxable", "TopHTML", "Weight"]
tables['ProductOptValue'] = ["Id", "IsDefault", "Label", "Name", "OptionIndex", "PriceAdjustment", "ProductOptionId", "Sku",]
tables['ProductOption'] = ["AllowSpaces", "CanContain", "CanEndWith", "CanStartWith", "Id", "IsRequired", "Label", "MaxChars", "MinChars", "Name", "OptionType", "Order", "ProductId", "TextMessage"]
tables['ProductCategory'] = ["CategoryDisplayName", "CategoryImage", "CategoryOrder", "Id", "ParentId"]
tables["ProductCategoryAssign"]=["Id","ProductCategoryId","ProductId"]

############################################################
## These will be used to hold what exists on the remote server
############################################################
remoteTables={}
remoteTables["Product"] = {}
remoteTables['ProductOptValue'] = {}
remoteTables['ProductOption'] = {}
remoteTables['ProductCategory'] = {}
remoteTables["ProductCategoryAssign"] = {}

############################################################
############################################################




class Product(object):

    def __init__(self, values):
        self.values=values
        global products
        self.internalid=id_generator()
        if 'products' not in globals():
            products={}
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
        if self in products.values():
            for eachid in products.keys():
                if self == products[eachid]:
                    self=products[eachid]
                    break
        if self.getid() not in products.keys():
            products[self.getid()] = self

class ProductCategory(object):
    global productcategorys
    global productCatagories
    if 'productcategorys' not in globals():
        productcategorys = {}

    def __init__(self,values):
        self.values=values
        self.children={}
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


    def __eq__(self, other):
        if self.generatePath()==other.generatePath():
            return True
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

    def generatePath(self):
        pathroot=''
        if self.ParentId not in [None,0]:
            pathroot = pathroot+productcategorys[self.ParentId].generatePath()
        return pathroot+"/"+self.CategoryDisplayName

    def registerChild(self, childCat):
        self.children[childCat.generatePath()]=childCat

    def register(self):
        if self.Id not in productcategorys.keys():
            productcategorys[self.Id]=self
        else:
            self=productcategorys[self.Id]
        # if self.getid() not in productcategorys.keys():
        #     productcategorys[self.getid()]=self

    def pathreg(self):
        if self.ParentId in [None,0]:
            self.ParentId = 0
            self.path=""+str(self.CategoryDisplayName)
        else:
            self.path=productcategorys[self.ParentId].generatePath()+"/"+self.CategoryDisplayName
        productCatagories[self.path]=self
        if self.Id is not None:
            productCatagories[self.Id]=self

class ProductCategoryAssign(object):
    global productcategoryassigns
    if 'productcategoryassigns' not in globals():
        productcategoryassigns = {}

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
        if self.getid() not in productcategoryassigns.keys():
            productcategoryassigns[self.getid()] = self

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

remoteTableObject={}
remoteTableObject["Product"] = Product
remoteTableObject['ProductOptValue'] = ProductOptValue
remoteTableObject['ProductOption'] = ProductOption
remoteTableObject['ProductCategory'] = ProductCategory
remoteTableObject["ProductCategoryAssign"] = ProductCategoryAssign

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



server = ISServer(pw.passwords['appname'], pw.passwords['apikey'])

def buildCategories(force=False):
    global productCatagories
    if 'productCatagories' not in globals():
        productCatagories={}
    global server
    global tables
    if (len(productCatagories.keys())==0 or force):
        print "building"
        allCategories=server.getAllRecords('ProductCategory', tables['ProductCategory'])
        catHold=[]
        for eachCategory in allCategories:
            thisCat = ProductCategory(eachCategory)
            catHold.append(thisCat)
        for eachCat in [cat for cat in catHold if cat.ParentId in[None,0]]:
            eachCat.pathreg()
        while True:
            repeat=False
            for eachCategory in catHold:
                try:
                    eachCategory.pathreg()
                except KeyError:
                    # print KeyError.args
                    # print KeyError.message
                    print "preg" + str(eachCategory.prepare())
            if not repeat:
                break



def getCatId(pathToCat):
    if len(pathToCat.strip(' /'))==0:
        return ''
    global productCatagories
    global iditerator
    global server
    buildCategories()
    # if (checkPath[0] != '/'):
    #     checkPath = '/' + pathToCat
    if pathToCat.replace('_','/') in productCatagories.keys():
        print "I found one!"
        return productCatagories[pathToCat.replace('_','/')].Id
    else:
        pathData=pathToCat.rsplit('/',1)
        if len(pathData)==1:
            thisCat = ProductCategory({"CategoryDisplayName": pathData[0].replace('_','/')})
        else:
            pd=pathData[1].replace('_','/')
            thisCat = ProductCategory({"CategoryDisplayName": pd})
            thisCat.ParentId=getCatId(pathData[0])
        print "create new catid", pathToCat
        thisCat.Id=server.createNewRecord('ProductCategory', thisCat.prepare())
        thisCat.register()
        thisCat.pathreg()
        return thisCat.Id

def getCatAssiggnId(productCatAssRecord):
    global server
    global tables
    catassignsforthisproduct=[assignid for assignid in remoteTables["ProductCategoryAssign"].keys() if remoteTables["ProductCategoryAssign"][assignid].ProductId == productCatAssRecord.ProductId]
    catassignids=[assignid for assignid in catassignsforthisproduct if remoteTables["ProductCategoryAssign"][assignid].ProductCategoryId == productCatAssRecord.ProductCategoryId]
    if len(catassignids)>0:
        return catassignids[0]
    else:
        print "create new catassignid"
        return server.createNewRecord("ProductCategoryAssign", productCatAssRecord.prepare())


def buildremotelocally():
    for eachtable in tables.keys():
        remotevals=server.getAllRecords(eachtable)
        for eachvalue in remotevals:
            remoteTables[eachtable][eachvalue["Id"]]=remoteTableObject[eachtable](eachvalue)


def getProductId(aProduct):
    global productsByName
    if len(remoteTables["Product"].keys())==0:
        buildremotelocally()
    if 'productsByName' not in globals():
        productsByName = {}
        for eachid in remoteTables['Product'].keys():
            productsByName[remoteTables['Product'][eachid].ProductName]=remoteTables['Product'][eachid]
    if aProduct.ProductName in productsByName.keys():
        return productsByName[aProduct.ProductName].Id
    else:
        print "creating a new product"
        aProduct.Id = server.createNewRecord('Product', aProduct.prepare())
        productsByName[aProduct.ProductName]=aProduct
        remoteTables["Product"][aProduct.Id]=aProduct
        return aProduct.Id


def act():
    """This is the method that will be used to orchestrate
    everything.
    """
    starttime=datetime.datetime.now()
    ########################################################
    ## Order of operations:
    ## Generate local copy of all product tables.
    ## process file into variables imitating the remotes.
    ## check for each local variable in remote table. if it
    ## it exists, remove it from the local lists
    ## if it does not, add it to the remote list and the remote
    ## server.
    ########################################################
    buildCategories()
    buildremotelocally()
    with open(pw.passwords['inputfilepath']) as csvin:
        thisreader=csv.DictReader(csvin)
        for eachrow in thisreader:
            if eachrow["Name"] and len(eachrow['Name'].strip(' \n'))>0 and eachrow["Name"][0] is not "[":
                #This is a product row
                thisproductline={}
                thisproductline['options']={} # A place to store options by name
                if eachrow["SKU"]:
                    thisproductline['Sku'] =eachrow["SKU"]
                thisproductline['Status'] = "1"
                if eachrow["Price"]:
                    thisproductline['ProductPrice'] = eachrow["Price"]
                if eachrow['Description']:
                    thisproductline['Description']=eachrow['Description']
                if eachrow["Meta Description"]:
                    thisproductline['ShortDescription'] = eachrow["Meta Description"]
                thisproductline['ProductName'] =eachrow["Name"]
                thisproductline['Id'] = [remoteTables["Product"][k]["Id"] for k in remoteTables["Product"].keys() if remoteTables["Product"][k]["ProductName"] == thisproductline['ProductName']]
                if len(thisproductline['Id'])>0:
                    print thisproductline["ProductName"]
                    thisproductline['Id']=thisproductline['Id'][0]
                    thisProduct=Product(thisproductline)
                else:
                    thisProduct=Product(thisproductline)
                    thisproductline['Id'] = server.createNewRecord("Product", thisProduct.prepare())
                if eachrow["Product Images"]:
                    thisProduct.imageStrings.append(eachrow["Product Images"])
                if eachrow["Product Images"]:
                    imageStrings=eachrow["Product Images"].split("|")
                    for eachS in imageStrings:
                        for eachVal in eachS.split(","):
                            if "Product Image URL: " in eachVal:
                                thisProduct.images.append(eachVal.replace("Product Image URL: ","").strip())
