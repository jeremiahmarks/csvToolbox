#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-21 23:08:05
# @Last Modified 2015-06-21
# @Last Modified time: 2015-06-21 23:59:40

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


    def getid(self):
        """Doing functionality like this allows things to be
        saved by a unique id, even if there is not one available
        """
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
