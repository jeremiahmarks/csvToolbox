#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-22 01:21:54
# @Last Modified 2015-06-22
# @Last Modified time: 2015-06-22 01:58:30

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


    def __eq__(self, other):
        if self.getid()==other.getid():
            return True
        if self.Name and other.Name:
            namesmatch=self.Name.lower().strip(' \n') is other.Name.lower().strip(' \n')
            return namesmatch and (self.ProductOptionId is other.ProductOptionId)
        return False

    def getid(self):
        """Doing functionality like this allows things to be
        saved by a unique id, even if there is not one available
        """
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




class ProductOptValueManager(object):
    def __init__(self, server):
        self.server=server
        self.table="ProductOptValue"
        self.objectTemplate=ProductOptValue
        self.downloadAllRecords()
        self.sortItems()

    def sortItems(self):
        self.ProdOptValById={}
        self.ProdOptValByName={}
        self.ProdOptValByProdOptId={}
        for eachobject in self.allObjects:
            eachobject.register()
            self.ProdOptValById[eachobject.Id]=eachobject
            if eachobject.Name not in self.ProdOptValByName.keys():
                self.ProdOptValByName[eachobject.Name]={}
            self.ProdOptValByName[eachobject.Name][eachobject.ProductOptionId]=eachobject
            if eachobject.ProductOptionId not in self.ProdOptValByProdOptId.keys():
                self.ProdOptValByProdOptId[eachobject.ProductOptionId]={}
            self.ProdOptValByProdOptId[eachobject.ProductOptionId][eachobject.Name]=eachobject

    def downloadAllRecords(self):
        self.allRecords=self.server.getAllRecords(self.table)
        self.allObjects=[self.objectTemplate(record) for record in self.allRecords]

    def getObject(self, aProductOptValueValues):
        if "Id" in aProductOptValueValues.keys():
            if aProductOptValueValues["Id"] in self.ProdOptValById.keys():
                return self.ProdOptValById[aProductOptValueValues["Id"]]
            else:
                matchingrecords=self.server.getMatchingRecords("ProductOptValue", aProductOptValueValues)
                if len(matchingrecords)>0:
                    self.allRecords.append(matchingrecords[0])
                    thisProductOptValue=ProductOptValue(matchingrecords[0])
                    self.ProdOptValById[thisProductOptValue.Id]=thisProductOptValue
                    if thisProductOptValue.Name not in self.ProdOptValByName.keys():
                        self.ProdOptValByName[thisProductOptValue.Name]={}
                    self.ProdOptValByName[thisProductOptValue.Name][thisProductOptValue.ProductOptionId]=thisProductOptValue
                    if thisProductOptValue.ProductOptionId not in self.ProdOptValByProdOptId.keys():
                        self.ProdOptValByProdOptId[thisProductOptValue.ProductOptionId]={}
                    self.ProdOptValByProdOptId[thisProductOptValue.ProductOptionId][thisProductOptValue.Name]=thisProductOptValue
                    thisProductOptValue.register()
                    return thisProductOptValue
                else:
                    thisid=self.server.createNewRecord("ProductOptValue", aProductOptValueValues)
                    thisProductOptValue=ProductOptValue(aProductOptValueValues)
                    thisProductOptValue.Id=thisid
                    self.ProdOptValById[thisProductOptValue.Id]=thisProductOptValue
                    if thisProductOptValue.Name not in self.ProdOptValByName.keys():
                        self.ProdOptValByName[thisProductOptValue.Name]={}
                    self.ProdOptValByName[thisProductOptValue.Name][thisProductOptValue.ProductOptionId]=thisProductOptValue
                    if thisProductOptValue.ProductOptionId not in self.ProdOptValByProdOptId.keys():
                        self.ProdOptValByProdOptId[thisProductOptValue.ProductOptionId]={}
                    self.ProdOptValByProdOptId[thisProductOptValue.ProductOptionId][thisProductOptValue.Name]=thisProductOptValue
                    thisProductOptValue.register()
                    return thisProductOptValue
        else:
            if not len(aProductOptValueValues["Name"].strip(' \n'))>0:
                return "This is an invalid product name"
            else:
                if aProductOptValueValues["Name"] not in self.ProdOptValByName.keys():
                    self.ProdOptValByName[aProductOptValueValues["Name"]]={}
                thisProductOptValue=ProductOptValue(aProductOptValueValues)
                thisProductOptValue.Id=self.server.createNewRecord("ProductOptValue", thisProductOptValue.prepare())
                self.ProdOptValById[thisProductOptValue.Id]=thisProductOptValue
                if thisProductOptValue.Name not in self.ProdOptValByName.keys():
                    self.ProdOptValByName[thisProductOptValue.Name]={}
                self.ProdOptValByName[thisProductOptValue.Name][thisProductOptValue.ProductOptionId]=thisProductOptValue
                if thisProductOptValue.ProductOptionId not in self.ProdOptValByProdOptId.keys():
                    self.ProdOptValByProdOptId[thisProductOptValue.ProductOptionId]={}
                self.ProdOptValByProdOptId[thisProductOptValue.ProductOptionId][thisProductOptValue.Name]=thisProductOptValue
                thisProductOptValue.register()
                return thisProductOptValue

