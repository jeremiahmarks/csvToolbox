#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-14 18:49:15
# @Last Modified 2015-06-14
# @Last Modified time: 2015-06-14 22:58:33
############################################################
##
##  This is a series of products meant to take a dictionary
##  as input and then provide a dictionary describing 
##  themselves when called by the .prepare() method
##
##  It includes  objects for data from the following tables
##      Product
##      ProductCategory
##      ProductCategoryAssign
##      ProductOptValue
##      ProductOption
############################################################



global products

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
        if self.id is not None:
            return "https://" + server.infusionsoftapp + ".infusionsoft.com/app/storeFront/showProductDetail?productId=" + str(self.Id)
        else:
            return "I do not seem to have an ID."

    def getInternalPage(self):
        if self.id is not None:
            return "https://" + server.infusionsoftapp + ".infusionsoft.com/app/product/manageProduct?productId=" + str(self.Id)
        else:
            return "I do not seem to have an ID."

    def detailedData(self):

        externalValues={}
        externalValues['publicPage'] = self.getPublicPage()
        externalValues['internalPage'] = self.getInternalPage()
        externalValues.update(self.vals())
        return externalValues

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
        self.register()

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
        for eachitem in vals.keys():
            # Since I cannot currently deal well with unicode, I must exclude it from writing to csv
            if type('str')==type(vals[eachitem]):
                for eachchr in vals[eachitem]:
                    if ord(eachchr)>128:
                        print "Error " + str(vals[eachitem])
                        vals[eachitem]=vals[eachitem].replace(eachchr, 'replaced')
        return vals

    def register(self):
        if self not in productoptions:
            productoptions.append(self)
            