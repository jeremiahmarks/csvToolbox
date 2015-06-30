#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-21 20:31:15
# @Last Modified 2015-06-24
# @Last Modified time: 2015-06-24 23:55:48
import HTMLParser
import my_pw
import ISServer
tablesOfInterest = ["Product", "ProductCategory", "ProductCategoryAssign", "ProductOptValue", "ProductOption"]
from Managers import ProductManager as pm
from Managers import ProductCatMan as pcm
from Managers import ProdCatAssMan as pcam
from Managers import ProductOptMan as pom
from Managers import ProdOptValMan as povm
from Managers import csvFileMan as csvMan


server = ISServer.ISServer(my_pw.passwords['appname'],
                           my_pw.passwords['apikey'])
print "Current records per table"
for eachtable in tablesOfInterest:
    print eachtable, server.getCount(eachtable, {})
thispm = pm.ProductManager(server)
server.callTotal()
thispcm = pcm.ProductCategoryManager(server)
server.callTotal()
thispcam = pcam.ProductCategoryAssignManager(server)
server.callTotal()
thispom = pom.ProductOptionManager(server)
server.callTotal()
thispovm = povm.ProductOptValueManager(server)
server.callTotal()
thiscsvman = csvMan.csvFile(my_pw.passwords['inputfilepath'])

server.callTotal()

HOLDER = {}
HOLDER['SkuPricing'] = []
HOLDER['PricingRule'] = []

thisproductsoptions = {}
for eachrow in thiscsvman:
    server.callTotal()
    if eachrow[0] == "Product":
        if len(thisproductsoptions.keys()) > 0:
            for eachoption in thisproductsoptions.keys():
                for eachvalue in thisproductsoptions[eachoption].keys():
                    thisobject=thispovm.getObject(thisproductsoptions[eachoption][eachvalue])
            thisproductsoptions = {}

        prodrow = eachrow[1]
        thisproduct = {}
        if prodrow['SKU']:
            thisproduct['Sku'] = prodrow['SKU']
        thisproduct['Status'] = '1'
        if prodrow["Price"]:
            thisproduct['ProductPrice'] = prodrow['Price']
        if prodrow['Description']:
            thisproduct['Description'] = prodrow['Description']
        if prodrow["Meta Description"]:
            thisproduct['ShortDescription'] = prodrow["Meta Description"]
        thisproduct['ProductName'] = prodrow["Name"]
        thisProduct = thispm.getObject(thisproduct)

        if prodrow['GPS Category']:
            lastcat = None
            gpscats = "GPS Category/" + prodrow['GPS Category']
            gpscats = gpscats.replace('\\/', '_')
            gpscats = gpscats.split('/')
            for eachcatposition in range(len(gpscats)):
                thiscat = gpscats[eachcatposition].replace('_', '/')
                thisproductcategory = {}
                thisproductcategory["CategoryDisplayName"] = thiscat
                if lastcat is not None:
                    thisproductcategory["ParentId"] = lastcat.Id
                lastcat = thispcm.getObject(thisproductcategory)
            thisprodcatass = {}
            thisprodcatass["ProductId"] = thisProduct.Id
            thisprodcatass["ProductCategoryId"] = lastcat.Id
            thisProdCatAss = thispcam.getObject(thisprodcatass)

        if prodrow["Brand"]:
            lastcat = None
            brandcats = "Brand/" + prodrow["Brand"]
            brandcats = brandcats.replace('\\/', '_')
            brandcats = brandcats.split('/')
            for eachcatposition in range(len(brandcats)):
                thiscat = brandcats[eachcatposition].replace('_', '/')
                thisproductcategory = {}
                thisproductcategory["CategoryDisplayName"] = thiscat
                if lastcat is not None:
                    thisproductcategory["ParentId"] = lastcat.Id
                lastcat = thispcm.getObject(thisproductcategory)
            thisprodcatass = {}
            thisprodcatass["ProductId"] = thisProduct.Id
            thisprodcatass["ProductCategoryId"] = lastcat.Id
            thisProdCatAss = thispcam.getObject(thisprodcatass)

        if prodrow['Category String']:
            catstring = prodrow['Category String'].replace('\\/', '_')
            catstrings = catstring.split(';')
            for eachcat in catstrings:
                lastcat = None
                catstrs = eachcat.split('/')
                for eachcatposition in range(len(catstrs)):
                    thiscat = catstrs[eachcatposition].replace('_', '/')
                    thisproductcategory = {}
                    thisproductcategory["CategoryDisplayName"] = thiscat
                    if lastcat is not None:
                        thisproductcategory["ParentId"] = lastcat.Id
                    lastcat = thispcm.getObject(thisproductcategory)
                thisprodcatass = {}
                thisprodcatass["ProductId"] = thisProduct.Id
                thisprodcatass["ProductCategoryId"] = lastcat.Id
                thisProdCatAss = thispcam.getObject(thisprodcatass)

    elif eachrow[0] == "Option":
        thisoptrow = eachrow[1]
        thissku = thisoptrow["SKU"]
        thisoptnames = thisoptrow["Name"].replace(
            '\\,', '_').replace(', ', "::")
        thisoptnames = thisoptnames.split(',')
        for eachoptionname in thisoptnames:
            if eachoptionname[0] == '[':
                eachoptionname = eachoptionname[eachoptionname.find(']') + 1:]
            eachoptionname = eachoptionname.replace(
                '_', ',').replace("::", ", ")
            if eachoptionname.count("=") == 0:
                print eachoptionname, eachrow[1]
            optionname, optionvalue = eachoptionname.split("=", 1)
            optionvalue = optionvalue.split(':')[0]
            print optionname, '\t\t\t', optionvalue
            thisproductoption = {}
            thisproductoption["Label"] = optionname
            thisproductoption["Name"] = optionname
            thisproductoption["OptionType"] = "FixedList"
            thisproductoption["ProductId"] = thisProduct.Id
            if optionname not in thisproductsoptions.keys():
                thisproductsoptions[optionname] = {}
            thisProductOption = thispom.getObject(thisproductoption)
            thisproductiontionvalue = {}
            thisproductiontionvalue["Label"] = optionvalue
            thisproductiontionvalue["Name"] = optionvalue
            if thisoptrow["SKU"]:
                thisproductiontionvalue["Sku"] = thisoptrow["SKU"]
            thisproductiontionvalue["ProductOptionId"] = thisProductOption.Id
            thisproductsoptions[optionname][
                optionvalue] = thisproductiontionvalue
            thisProductOptVal = thispovm.getObject(thisproductiontionvalue)
            # This was removed in order to allow all of the pricing rules to be
            # factored in first
    elif eachrow[0] == "PricingRule":
        thispricingrow = eachrow[1]
        thissku = thispricingrow["SKU"]
        thisoptnames = thispricingrow["Name"].replace(
            '\\,', '_').replace(', ', "::")
        for eachoptionname in thisoptnames.split(','):
            print '\n\n' + eachoptionname
            if eachoptionname[0] == '[':
                eachoptionname = eachoptionname[eachoptionname.find(']') + 1:]
            eachoptionname = eachoptionname.replace(
                '_', ',').replace("::", ", ")
            optionname, optionvalue = eachoptionname.split("=", 1)
            optionvalue = optionvalue.split(':')[0]
            thisproductoption = {}
            thisproductoption["Label"] = optionname
            thisproductoption["Name"] = optionname
            thisproductoption["OptionType"] = "FixedList"
            thisproductoption["ProductId"] = thisProduct.Id
            if optionname not in thisproductsoptions.keys():
                thisproductsoptions[optionname] = {}
            thisProductOption = thispom.getObject(thisproductoption)
            thisprice = thispricingrow["Price"]

            if thisprice and len(thisprice) > 0 and thisprice[0] == '[':
                thispriceaction, thisprice = thisprice[1:].split(']')
                if thispriceaction == "ADD":
                    thisprice = thisprice
                if thispriceaction == "REMOVE":
                    thisprice = '-' + thisprice
                if thispriceaction == "FIXED":
                    thisprice = str(
                        float(thisprice) - float(thisProduct.ProductPrice))
            if optionname not in thisproductsoptions.keys():
                thisproductsoptions[optionname] = {}
            if optionvalue not in thisproductsoptions[optionname].keys():
                thisproductsoptions[optionname][optionvalue] = {}
                thisproductsoptions[optionname][
                    optionvalue]["Label"] = optionvalue
                thisproductsoptions[optionname][
                    optionvalue]["Name"] = optionvalue
                thisproductsoptions[optionname][optionvalue][
                    "Sku"] = thispricingrow["SKU"]
                thisproductsoptions[optionname][optionvalue][
                    "ProductOptionId"] = thisProductOption.Id

            thisproductsoptions[optionname][optionvalue][
                "PriceAdjustment"] = thisprice
            thisproductsoptions[optionname][optionvalue][
                "Sku"] = thispricingrow["SKU"]
            thisproductsoptions[optionname][optionvalue][
                "OptionIndex"] = len(thisproductsoptions[optionname])

    elif eachrow[0] == "SkuPricing":
        thisskupricingrow = eachrow[1]
        thissku = thisskupricingrow["SKU"]
        thisoption = None
        thisoptionvalue = None
        for eachoption in thisproductsoptions.keys():
            for eachoptionvalue in thisproductsoptions[eachoption].keys():
                if thissku == thisproductsoptions[eachoption][eachoptionvalue]["Sku"]:
                    thisoption = eachoption
                    thisoptionvalue = eachoptionvalue
                    break
            if thisoption is not None:
                break
        if thisoption is not None:
            thisprice = thisskupricingrow["Price"]

            if thisprice and len(thisprice) > 0 and thisprice[0] == '[':
                thispriceaction, thisprice = thisprice[1:].split(']')
                if thispriceaction == "ADD":
                    thisprice = thisprice
                if thispriceaction == "REMOVE":
                    thisprice = '-' + thisprice
                if thispriceaction == "FIXED":
                    thisprice = str(
                        float(thisprice) - float(thisProduct.ProductPrice))
                thisproductsoptions[eachoption][eachoptionvalue][
                    "PriceAdjustment"] = thisprice

print "Current records per table"
for eachtable in tablesOfInterest:
    print eachtable, server.getCount(eachtable, {})
