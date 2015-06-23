#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-22 00:02:38
# @Last Modified 2015-06-23
# @Last Modified time: 2015-06-23 01:07:19
import HTMLParser
html_parser = HTMLParser.HTMLParser()


class ProductOption(object):
    global productoptions
    if 'productoptions' not in globals():
        productoptions = []

    def __init__(self, values):
        self.values = values
        if "AllowSpaces" in values.keys():
            self.AllowSpaces = values["AllowSpaces"]
        else:
            self.AllowSpaces = None

        if "CanContain" in values.keys():
            self.CanContain = values["CanContain"]
        else:
            self.CanContain = None

        if "CanEndWith" in values.keys():
            self.CanEndWith = values["CanEndWith"]
        else:
            self.CanEndWith = None

        if "CanStartWith" in values.keys():
            self.CanStartWith = values["CanStartWith"]
        else:
            self.CanStartWith = None

        if "Id" in values.keys():
            self.Id = values["Id"]
        else:
            self.Id = None

        if "IsRequired" in values.keys():
            self.IsRequired = values["IsRequired"]
        else:
            self.IsRequired = None

        if "Label" in values.keys() and values["Label"]:
            self.Label = html_parser.unescape(values["Label"])
        else:
            self.Label = None

        if "MaxChars" in values.keys():
            self.MaxChars = values["MaxChars"]
        else:
            self.MaxChars = None

        if "MinChars" in values.keys():
            self.MinChars = values["MinChars"]
        else:
            self.MinChars = None

        if "Name" in values.keys() and values["Name"]:
            self.Name = html_parser.unescape(values["Name"])
        else:
            self.Name = None

        if "OptionType" in values.keys():
            self.OptionType = values["OptionType"]
        else:
            self.OptionType = None

        if "Order" in values.keys():
            self.Order = values["Order"]
        else:
            self.Order = None

        if "ProductId" in values.keys():
            self.ProductId = values["ProductId"]
        else:
            self.ProductId = None

        if "TextMessage" in values.keys():
            self.TextMessage = values["TextMessage"]
        else:
            self.TextMessage = None
        self.optionvalues = []

    def getid(self):
        """Doing functionality like this allows things to be
        saved by a unique id, even if there is not one available
        """
        return self.Id

    def prepare(self):
        vals = {}
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


class ProductOptionManager(object):

    def __init__(self, server):
        self.server = server
        self.table = "ProductOption"
        self.objectTemplate = ProductOption
        self.downloadAllRecords()
        self.sortItems()

    def sortItems(self):
        self.prodOptById = {}
        self.prodOptByProdId = {}
        self.prodOptByName = {}
        for eachobject in self.allObjects:
            if not eachobject.Name:
                continue
            eachobject.Name = html_parser.unescape(eachobject.Name)
            eachobject.Label = html_parser.unescape(eachobject.Label)
            eachobject.register()
            self.prodOptById[eachobject.Id] = eachobject
            if eachobject.ProductId not in self.prodOptByProdId.keys():
                self.prodOptByProdId[eachobject.ProductId] = {}
            self.prodOptByProdId[eachobject.ProductId][
                eachobject.Name] = eachobject
            if eachobject.Name not in self.prodOptByName.keys():
                self.prodOptByName[eachobject.Name] = {}
            self.prodOptByName[eachobject.Name][
                eachobject.ProductId] = eachobject

    def downloadAllRecords(self):
        self.allRecords = self.server.getAllRecords(self.table)
        self.allObjects = [
            self.objectTemplate(record) for record in self.allRecords]

    def getObject(self, aProductOptionValues):
        if "Id" in aProductOptionValues.keys():
            if aProductOptionValues["Id"] in self.prodOptById.keys():
                return self.prodOptById[aProductOptionValues["Id"]]
            else:
                matchingrecords = self.server.getMatchingRecords(
                    "ProductOption", aProductOptionValues)
                if len(matchingrecords) > 0:
                    self.allRecords.append(matchingrecords[0])
                    thisProductOption = ProductOption(matchingrecords[0])
                    self.prodOptById[thisProductOption.Id] = thisProductOption
                    if thisProductOption.ProductId not in self.prodOptByProdId.keys():
                        self.prodOptByProdId[thisProductOption.ProductId] = {}
                    self.prodOptByProdId[thisProductOption.ProductId][
                        thisProductOption.Name] = thisProductOption
                    if html_parser.unescape(thisProductOption.Name) not in self.prodOptByName.keys():
                        self.prodOptByName[html_parser.unescape(thisProductOption.Name)] = {}
                    self.prodOptByName[html_parser.unescape(thisProductOption.Name)][
                        thisProductOption.ProductId] = thisProductOption
                    thisProductOption.register()
                    return thisProductOption
                else:
                    thisid = self.server.createNewRecord(
                        "ProductOption", aProductOptionValues)
                    thisProductOption = ProductOption(aProductOptionValues)
                    thisProductOption.Id = thisid
                    self.prodOptById[thisProductOption.Id] = thisProductOption
                    if thisProductOption.ProductId not in self.prodOptByProdId.keys():
                        self.prodOptByProdId[thisProductOption.ProductId] = {}
                    self.prodOptByProdId[thisProductOption.ProductId][
                        thisProductOption.Name] = thisProductOption
                    if html_parser.unescape(thisProductOption.Name) not in self.prodOptByName.keys():
                        self.prodOptByName[html_parser.unescape(thisProductOption.Name)] = {}
                    self.prodOptByName[thisProductOption.Name][
                        thisProductOption.ProductId] = thisProductOption
                    thisProductOption.register()
                    return thisProductOption
        else:
            if not len(str(aProductOptionValues["Name"]).strip(' \n')) > 0:
                return "This is an invalid Option name"
            else:
                if aProductOptionValues["ProductId"] in self.prodOptByProdId.keys():
                    for eachpotential in self.prodOptByProdId[aProductOptionValues["ProductId"]].keys():
                        if self.prodOptByProdId[aProductOptionValues["ProductId"]][eachpotential].Name == aProductOptionValues["Name"]:
                            return self.prodOptByProdId[aProductOptionValues["ProductId"]][self.prodOptByProdId[aProductOptionValues["ProductId"]].keys()[0]]
                thisProductOption = ProductOption(aProductOptionValues)
                thisProductOption.Name = html_parser.unescape(thisProductOption.Name)
                thisProductOption.Label = html_parser.unescape(thisProductOption.Label)
                thisProductOption.Id = self.server.createNewRecord(
                    "ProductOption", thisProductOption.prepare())
                self.prodOptById[thisProductOption.Id] = thisProductOption
                if thisProductOption.ProductId not in self.prodOptByProdId.keys():
                    self.prodOptByProdId[thisProductOption.ProductId] = {}
                self.prodOptByProdId[thisProductOption.ProductId][
                    thisProductOption.Name] = thisProductOption
                if thisProductOption.Name not in self.prodOptByName.keys():
                    self.prodOptByName[thisProductOption.Name] = {}
                self.prodOptByName[thisProductOption.Name][
                    thisProductOption.ProductId] = thisProductOption
                thisProductOption.register()
                return thisProductOption
