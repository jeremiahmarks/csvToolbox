#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-20 23:04:52
# @Last Modified 2015-06-21
# @Last Modified time: 2015-06-21 20:11:35
import my_pw as pw
import csv
import datetime
import allatonce
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

defaultrestkey="OutsideOfTable"
defaultrestval=""
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')
        
def getAllLinesAsDict(pathtofile):
  allrowsbynumber={}
  thisfile=open(pathtofile)
  thisreader=unicode_csv_reader(thisfile)
  for eachrownumber, eachrow in enumerate(thisreader):
    if eachrownumber==0:
      headings=eachrow
    thisrowsheadings=headings[:]
    extracols=[]
    for eachheading in range(len(eachrow) - len(thisrowsheadings)):
      extracols.append(str(eachheading))
    thisrowdict={}
    for eachcolset in zip(thisrowsheadings + extracols, eachrow):
      thisrowdict[eachcolset[0]]=eachcolset[1]
    thisrowdict['extra']=[thisrowdict.pop(k) for k in thisrowdict.keys() if k in extracols]
    allrowsbynumber[eachrownumber]=thisrowdict
  return allrowsbynumber


class csvFile(object):

    def getRowType(self, row):
        if len(row["Name"]) is 0:
            return "SkuPricing"
        elif (row["Name"][0] != "["):
            return "Product"
        elif (len(row["SKU"])==0) or len(row["Price"])>0:
            return "PricingRule"
        else:
            return "Option"

    def __init__(self, pathtofile):
        self.rows=getAllLinesAsDict(pathtofile)
        self.readerfieldnames=self.rows[0]
        self.parseRows()


    def parseRows(self):
        self.rowsbytype={}
        for eachline in self.rows.keys():
            if len(self.rows[eachline])>1:
                linetype=self.getRowType(self.rows[eachline])
                if linetype not in self.rowsbytype.keys():
                    self.rowsbytype[linetype]=[]
                self.rowsbytype[linetype].append(eachline)

    def printrows(self):
        for eachtype in self.rowsbytype.keys():
            print eachtype
            
            for eachrecord in self.rowsbytype[eachtype]:
                thisstr=''
                for eachcolumn in self.rows[eachrecord].keys():
                    thisstr+='\n'
                    thisstr += ','+ str(eachcolumn[0:30]).rjust(40,' ') + ',' + str(self.rows[eachrecord][eachcolumn][0:30]).rjust(40,' ')
                print thisstr
    def putrowsinfile(self):
        for eachtype in self.rowsbytype.keys():
            thisoutfile = open(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + eachtype +".csv", 'wb')
            thiswriter=csv.DictWriter(thisoutfile, self.readerfieldnames)
            thiswriter.writeheader()
            for eachlinenumber in self.rowsbytype[eachtype]:
                rowtowrite={}
                for eachcolumn in self.rows[eachlinenumber].keys():
                    rowtowrite[eachcolumn] = str(self.rows[eachlinenumber][eachcolumn][0:30]).rjust(40, ' ')
                thiswriter.writerow(rowtowrite)
            thisoutfile.close()

    def parseRowIntoProduct(self, row):
        thisproduct={}
        if row['SKU']:
            thisproduct['Sku']=row['SKU']
        thisproduct['Status']='1'
        if row["Price"]:
            thisproduct['ProductPrice']=row['Price']
        if row['Description']:
            thisproduct['Description']=row['Description']
        if row["Meta Description"]:
            thisproduct['ShortDescription'] = row["Meta Description"]
        thisproduct['ProductName']= row["Name"]
        thisProduct = allatonce.Product(thisproduct)
        thisProduct.Id = allatonce.getProductId(thisProduct)
        self.parseRowIntoCategories(row, thisProduct.getid())
        return thisProduct
        
    def parseRowIntoCategories(self, row, productId):
        if row['GPS Category']:
            gpscats="/GPS Category/" + row['GPS Category']
            thiscatid=allatonce.getCatId(gpscats)
            thiscatassign={}
            thiscatassign["ProductCategoryId"]=thiscatid
            thiscatassign["ProductId"]=productId
            thisAssignment=allatonce.ProductCategoryAssign(thiscatassign)
            thisAssignment.Id=allatonce.getCatAssiggnId(thisAssignment)
        if row["Brand"]:
            brandcats="/Brand/"+ row["Brand"]
            thiscatid=allatonce.getCatId(brandcats)
            thiscatassign={}
            thiscatassign["ProductCategoryId"]=thiscatid
            thiscatassign["ProductId"]=productId
            thisAssignment=allatonce.ProductCategoryAssign(thiscatassign)
            thisAssignment.Id=allatonce.getCatAssiggnId(thisAssignment)
        if row['Category String']:
            catstring=row['Category String'].replace('\\/', '_')
            catstrings=catstring.split(';')
            for eachcat in catstrings:
                thiscatid=allatonce.getCatId("/"+eachcat)
                thiscatassign={}
                thiscatassign["ProductCategoryId"]=thiscatid
                thiscatassign["ProductId"]=productId
                thisAssignment=allatonce.ProductCategoryAssign(thiscatassign)
                thisAssignment.Id=allatonce.getCatAssiggnId(thisAssignment)

    def parseOptionsRow(self, row, parentProductId):
        pass





    def processthings(self):

        for eachlinenumber in self.rows.keys():
            print eachlinenumber
            if eachlinenumber in self.rowsbytype["Product"]:
                thisProduct=self.parseRowIntoProduct(self.rows[eachlinenumber])
            elif eachlinenumber in self.rowsbytype["Option"]:
                self.parseOptionsRow(self.rows[eachlinenumber], thisProduct.Id)
            if eachlinenumber in self.rowsbytype["SkuPricing"]:
                pass
            if eachlinenumber in self.rowsbytype["PricingRule"]:
                pass
        




