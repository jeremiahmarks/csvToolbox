#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-22 00:02:38
# @Last Modified 2015-06-22>
# @Last Modified time: 2015-06-22 00:03:16


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


class ProductCategoryAssignManager(object):


    def __init__(self, server):
        self.server=server
        self.table="ProductCategoryAssign"
        self.objectTemplate=ProductCategoryAssign
        self.downloadAllRecords()
        self.sortItems()

    def sortItems(self):
        self.prodCatAssById={}
        self.prodCatAssByProdId={}
        self.prodCatAssByCatId={}
        for eachobject in self.allObjects:
            eachobject.register()
            self.prodCatAssById[eachobject.Id]=eachobject
            if eachobject.ProductId not in self.prodCatAssByProdId.keys():
                self.prodCatAssByProdId[eachobject.ProductId]={}
            self.prodCatAssByProdId[eachobject.ProductId][eachobject.ProductCategoryId]=eachobject
            if eachobject.ProductCategoryId not in self.prodCatAssByCatId.keys():
                self.prodCatAssByCatId[eachobject.ProductCategoryId]={}
            self.prodCatAssByCatId[eachobject.ProductCategoryId][eachobject.ProductId]=eachobject


    def downloadAllRecords(self):
        self.allRecords=self.server.getAllRecords(self.table)
        self.allObjects=[self.objectTemplate(record) for record in self.allRecords]

    def getObject(self, aProductCategoryAssignValues):
        if "Id" in aProductCategoryAssignValues.keys():
            if aProductCategoryAssignValues["Id"] in self.prodCatAssById.keys():
                return self.prodCatAssById[aProductCategoryAssignValues["Id"]]
            else:
                matchingrecords=self.server.getMatchingRecords("ProductCategoryAssign", aProductCategoryAssignValues)
                if len(matchingrecords)>0:
                    self.allRecords.append(matchingrecords[0])
                    thisProductCategoryAssign=ProductCategoryAssign(matchingrecords[0])
                    self.prodCatAssById[thisProductCategoryAssign.Id]=thisProductCategoryAssign
                    if thisProductCategoryAssign.ProductId not in self.prodCatAssByProdId.keys():
                        self.prodCatAssByProdId[thisProductCategoryAssign.ProductId]={}
                    self.prodCatAssByProdId[thisProductCategoryAssign.ProductId][thisProductCategoryAssign.ProductCategoryId]=thisProductCategoryAssign
                    if thisProductCategoryAssign.ProductCategoryId not in self.prodCatAssByCatId.keys():
                        self.prodCatAssByCatId[thisProductCategoryAssign.ProductCategoryId]={}
                    self.prodCatAssByCatId[thisProductCategoryAssign.ProductCategoryId][thisProductCategoryAssign.ProductId]=thisProductCategoryAssign
                    thisProductCategoryAssign.register()
                    return thisProductCategoryAssign
                else:
                    thisid=self.server.createNewRecord("ProductCategoryAssign", aProductCategoryAssignValues)
                    thisProductCategoryAssign=ProductCategoryAssign(aProductCategoryAssignValues)
                    thisProductCategoryAssign.Id=thisid
                    self.prodCatAssById[thisProductCategoryAssign.Id]=thisProductCategoryAssign
                    if thisProductCategoryAssign.ProductId not in self.prodCatAssByProdId.keys():
                        self.prodCatAssByProdId[thisProductCategoryAssign.ProductId]={}
                    self.prodCatAssByProdId[thisProductCategoryAssign.ProductId][thisProductCategoryAssign.ProductCategoryId]=thisProductCategoryAssign
                    if thisProductCategoryAssign.ProductCategoryId not in self.prodCatAssByCatId.keys():
                        self.prodCatAssByCatId[thisProductCategoryAssign.ProductCategoryId]={}
                    self.prodCatAssByCatId[thisProductCategoryAssign.ProductCategoryId][thisProductCategoryAssign.ProductId]=thisProductCategoryAssign
                    thisProductCategoryAssign.register()
                    return thisProductCategoryAssign
        else:
            if not len(str(aProductCategoryAssignValues["ProductId"]).strip(' \n'))>0:
                return "This is an invalid CatName name"
            else:
                if aProductCategoryAssignValues["ProductId"] in self.prodCatAssByProdId.keys():
                    for eachpotential in self.prodCatAssByProdId[aProductCategoryAssignValues["ProductId"]].keys():
                        if self.prodCatAssByProdId[aProductCategoryAssignValues["ProductId"]][eachpotential].ProductCategoryId == aProductCategoryAssignValues["ProductCategoryId"]:
                            return self.prodCatAssByProdId[aProductCategoryAssignValues["ProductId"]][self.prodCatAssByProdId[aProductCategoryAssignValues["ProductId"]].keys()[0]]
                thisProductCategoryAssign=ProductCategoryAssign(aProductCategoryAssignValues)
                thisProductCategoryAssign.Id=self.server.createNewRecord("ProductCategoryAssign", thisProductCategoryAssign.prepare())
                self.prodCatAssById[thisProductCategoryAssign.Id]=thisProductCategoryAssign
                if thisProductCategoryAssign.ProductId not in self.prodCatAssByProdId.keys():
                    self.prodCatAssByProdId[thisProductCategoryAssign.ProductId]={}
                self.prodCatAssByProdId[thisProductCategoryAssign.ProductId][thisProductCategoryAssign.ProductCategoryId]=thisProductCategoryAssign
                if thisProductCategoryAssign.ProductCategoryId not in self.prodCatAssByCatId.keys():
                    self.prodCatAssByCatId[thisProductCategoryAssign.ProductCategoryId]={}
                self.prodCatAssByCatId[thisProductCategoryAssign.ProductCategoryId][thisProductCategoryAssign.ProductId]=thisProductCategoryAssign
                thisProductCategoryAssign.register()
                return thisProductCategoryAssign
