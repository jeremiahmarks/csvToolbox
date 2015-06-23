#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-21 23:00:41
# @Last Modified 2015-06-21
# @Last Modified time: 2015-06-22 17:04:54

import HTMLParser
html_parser = HTMLParser.HTMLParser()


class ProductCategory(object):
    global productcategorys
    global productCatagories
    if 'productcategorys' not in globals():
        productcategorys = {}

    def __init__(self, values):
        self.values = values
        self.children = {}
        if "CategoryDisplayName" in values.keys():
            self.CategoryDisplayName = values["CategoryDisplayName"]
        else:
            self.CategoryDisplayName = None
        if "CategoryImage" in values.keys():
            self.CategoryImage = values["CategoryImage"]
        else:
            self.CategoryImage = None
        if "CategoryOrder" in values.keys():
            self.CategoryOrder = values["CategoryOrder"]
        else:
            self.CategoryOrder = None
        if "Id" in values.keys():
            self.Id = values["Id"]
        else:
            self.Id = None
        if "ParentId" in values.keys():
            self.ParentId = values["ParentId"]
        else:
            self.ParentId = None

    def getid(self):
        """Doing functionality like this allows things to be
        saved by a unique id, even if there is not one available
        """
        return self.Id

    def prepare(self):
        vals = {}
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
        return vals

    def register(self):
        if self.Id not in productcategorys.keys():
            productcategorys[self.Id] = self
        # if self.getid() not in productcategorys.keys():
        #     productcategorys[self.getid()] = self


class ProductCategoryManager(object):
    def __init__(self, server):
        self.server = server
        self.table = "ProductCategory"
        self.objectTemplate = ProductCategory
        self.downloadAllRecords()
        self.sortItems()

    def sortItems(self):
        self.productCatsbyID = {}
        self.productCatsbyName = {}
        self.productCatsbyParentId = {}
        for eachobject in self.allObjects:
            if eachobject.CategoryDisplayName and len(eachobject.CategoryDisplayName) > 0:
                eachobject.CategoryDisplayName = html_parser.unescape(eachobject.CategoryDisplayName)
            eachobject.register()
            self.productCatsbyID[eachobject.Id] = eachobject
            if eachobject.CategoryDisplayName not in \
                    self.productCatsbyName.keys():
                self.productCatsbyName[eachobject.CategoryDisplayName] = {}
            self.productCatsbyName[
                eachobject.CategoryDisplayName
            ][eachobject.Id] = eachobject
            if eachobject.ParentId not in [None, 0]:
                if eachobject.ParentId not in \
                        self.productCatsbyParentId.keys():
                    self.productCatsbyParentId[eachobject.ParentId] = {}
                self.productCatsbyParentId[eachobject.ParentId][
                    eachobject.CategoryDisplayName
                ] = eachobject

    def downloadAllRecords(self):
        self.allRecords = self.server.getAllRecords(self.table)
        self.allObjects = [
            self.objectTemplate(record) for record in self.allRecords
        ]

    def getObject(self, aProductCategoryValues):
        if ("ParentId" not in aProductCategoryValues or
                aProductCategoryValues["ParentId"] is None):
            aProductCategoryValues["ParentId"] = 0
        if "Id" in aProductCategoryValues.keys():
            if aProductCategoryValues["Id"] in self.productCatsbyID.keys():
                return self.productCatsbyID[aProductCategoryValues["Id"]]
            else:
                matchingrecords = self.server.getMatchingRecords(
                    "ProductCategory", aProductCategoryValues)
                if len(matchingrecords) > 0:
                    self.allRecords.append(matchingrecords[0])
                    thisProductCategory = ProductCategory(matchingrecords[0])
                    self.productCatsbyID[
                        thisProductCategory.Id] = thisProductCategory
                    if (thisProductCategory.CategoryDisplayName not in
                            self.productCatsbyName.keys()):
                        self.productCatsbyName[
                            html_parser.unescape(
                                thisProductCategory.CategoryDisplayName)
                        ] = {}
                    self.productCatsbyName[
                        html_parser.unescape(
                            thisProductCategory.CategoryDisplayName
                        )
                    ][thisProductCategory.Id] = thisProductCategory
                    thisProductCategory.register()
                    return thisProductCategory
                else:
                    thisid = self.server.createNewRecord(
                        "ProductCategory", aProductCategoryValues)
                    thisProductCategory = ProductCategory(
                        aProductCategoryValues)
                    thisProductCategory.Id = thisid
                    self.productCatsbyID[
                        thisProductCategory.Id] = thisProductCategory
                    if (thisProductCategory.CategoryDisplayName not in
                            self.productCatsbyName.keys()):
                        self.productCatsbyName[
                            html_parser.unescape(
                                thisProductCategory.CategoryDisplayName
                            )] = {}
                    self.productCatsbyName[
                        html_parser.unescape(
                            thisProductCategory.CategoryDisplayName
                        )][thisProductCategory.Id] = thisProductCategory
                    thisProductCategory.register()
                    return thisProductCategory
        else:
            if not len(
                aProductCategoryValues["CategoryDisplayName"].strip(' \n')
            ) > 0:
                return "This is an invalid CatName name"
            else:
                if aProductCategoryValues[
                        "CategoryDisplayName"] in self.productCatsbyName.keys():
                    for eachpotential in self.productCatsbyName[aProductCategoryValues["CategoryDisplayName"]].keys():
                        if self.productCatsbyName[aProductCategoryValues["CategoryDisplayName"]][eachpotential].ParentId ==  aProductCategoryValues["ParentId"]:
                            return self.productCatsbyName[aProductCategoryValues["CategoryDisplayName"]][self.productCatsbyName[aProductCategoryValues["CategoryDisplayName"]].keys()[0]]
                thisProductCategory = ProductCategory(aProductCategoryValues)
                thisProductCategory.Id = self.server.createNewRecord("ProductCategory", thisProductCategory.prepare())
                self.productCatsbyID[thisProductCategory.Id] = thisProductCategory
                if thisProductCategory.CategoryDisplayName not in self.productCatsbyName.keys():
                    self.productCatsbyName[html_parser.unescape(thisProductCategory.CategoryDisplayName)] = {}
                self.productCatsbyName[html_parser.unescape(thisProductCategory.CategoryDisplayName)][thisProductCategory.Id] = thisProductCategory
                thisProductCategory.register()
                return thisProductCategory
