#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-21 20:31:15
# @Last Modified 2015-06-22
# @Last Modified time: 2015-06-22 18:01:44
import HTMLParser
import my_pw
import ISServer


from Managers import ProductManager as pm
from Managers import ProductCatMan as pcm
from Managers import ProdCatAssMan as pcam
from Managers import ProductOptMan as pom
from Managers import ProdOptValMan as povm
from Managers import csvFileMan as csvMan


server = ISServer.ISServer(my_pw.passwords['appname'],
                           my_pw.passwords['apikey'])

thispm = pm.ProductManager(server)
thispcm = pcm.ProductCategoryManager(server)
thispcam = pcam.ProductCategoryAssignManager(server)
thispom = pom.ProductOptionManager(server)
thispovm = povm.ProductOptValueManager(server)
thiscsvman = csvMan.csvFile(my_pw.passwords['inputfilepath'])


for eachrow in thiscsvman:
    if eachrow[0] == "Product":
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
    if eachrow[0] == "Option":
        thisoptrow = eachrow[1]
        thissku = thisoptrow["SKU"]
        thisoptnames = thisoptrow["Name"].replace('\\,', '_')
        thisoptnames = thisoptnames.split(',')
        for eachoptionname in thisoptnames:
            eachoptionname = eachoptionname.replace('_', ',')
            if eachoptionname.count("=") == 0:
                print eachoptionname, eachrow[1]
            optionname, optionvalue = eachoptionname.split("=", 1)
            thisproductoption = {}
            thisproductoption["Label"] = optionname
            thisproductoption["Name"] = optionname
            thisproductoption["OptionType"] = "FixedList"
            thisproductoption["ProductId"] = thisProduct.Id
            thisProductOption = thispom.getObject(thisproductoption)
            thisproductiontionvalue = {}
            thisproductiontionvalue["Label"] = optionvalue
            thisproductiontionvalue["Name"] = optionvalue
            if thisoptrow["SKU"]:
                thisproductiontionvalue["Sku"] = thisoptrow["SKU"]
            thisproductiontionvalue["ProductOptionId"] = thisProductOption.Id
            thisProductOptVal = thispovm.getObject(thisproductiontionvalue)
