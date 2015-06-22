#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-21 22:56:49
# @Last Modified 2015-06-21>
# @Last Modified time: 2015-06-21 23:00:16

class Product(object):

    def __init__(self, values):
        self.values=values
        global products
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
        self.images=[]
        self.imageStrings=[]



    def __eq__(self, other):
        if self.getid()==other.getid():
            return True
        # catsmatch= len(self.categories.keys())>0 is len(other.categories.keys())>0   # Basically,
        # this checks to see if both of the products have categories or if
        # they both do not. Basically the statment says
        #               [T/F] is [T/F]
        # and returns that.
        if self.ProductName and other.ProductName:
            namesmatch=self.ProductName.lower().strip(' \n') is other.ProductName.lower().strip(' \n')
            return namesmatch
        return False

    def getid(self):
        """Doing functionality like this allows things to be
        saved by a unique id, even if there is not one available
        """
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
        if self.Id is None:
            self.Id = "UNKNOWN"
            products[self.getid()] = self


class ProductManager(object):
    def __init__(self, server):
        self.server=server
        self.table="Product"
        self.objectTemplate=Product
        self.downloadAllRecords()
        self.sortItems()

    def sortItems(self):
        self.productsbyid={}
        self.productsbyname={}
        for eachobject in self.allObjects:
            eachobject.register()
            self.productsbyid[eachobject.Id]=eachobject
            self.productsbyname[eachobject.ProductName]=eachobject

    def downloadAllRecords(self):
        self.allRecords=self.server.getAllRecords(self.table)
        self.allObjects=[self.objectTemplate(record) for record in self.allRecords]

    def getObject(self, aProductValues):
        if "Id" in aProductValues.keys():
            if aProductValues["Id"] in self.productsbyid.keys():
                return self.productsbyid[aProductValues["Id"]]
            else:
                matchingrecords=self.server.getMatchingRecords("Product", aProductValues)
                if len(matchingrecords)>0:
                    self.allRecords.append(matchingrecords[0])
                    thisProduct=Product(matchingrecords[0])
                    self.productsbyid[thisProduct.Id]=thisProduct
                    self.productsbyname[thisProduct.ProductName]=thisProduct
                    thisProduct.register()
                    return thisProduct
                else:
                    thisid=self.server.cnp(aProductValues)
                    thisProduct=Product(aProductValues)
                    thisProduct.Id=thisid
                    self.productsbyid[thisProduct.Id]=thisProduct
                    self.productsbyname[thisProduct.ProductName]=thisProduct
                    thisProduct.register()
                    return thisProduct
        else:
            if not len(aProductValues["ProductName"].strip(' \n'))>0:
                return "This is an invalid product name"
            else:
                if aProductValues["ProductName"] in self.productsbyname.keys():
                    return self.productsbyname[aProductValues["ProductName"]]
                thisProduct=Product(aProductValues)
                thisProduct.Id=self.server.cnp(thisProduct.prepare())
                self.productsbyid[thisProduct.Id]=thisProduct
                self.productsbyname[thisProduct.ProductName]=thisProduct
                thisProduct.register()
                return thisProduct

