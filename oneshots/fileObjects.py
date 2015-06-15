#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-14 23:25:12
# @Last Modified 2015-06-15
# @Last Modified time: 2015-06-15 01:37:04
############################################################
##
##  This file is what actually processes eachline of the file
##  It will determine what type of line it is, and parse if 
##  accordingly.
##
############################################################

class product(object):

    def __init__(self, name):
        self.id=False
        self.name=name
        self.categories=None
        self.catStrings=[]
        self.sku=False
        self.description=False
        self.price=0.00
        self.isActive=1
        self.images=[]
        self.imageStrings=[]
        self.shortDescription=False
        self.taxable=-1
        self.cityTax=-1
        self.countryTax=-1
        self.stateTax=-1
        self.shippable=-1
        self.weight=False
        self.options=None
        self.optionsSettings=None
        self.optionsPriceChange={}
        ##self.

    def prepare(self):
        vals={}
        vals["ProductName"]=self.name
        if (self.sku):
            vals["Sku"] = self.sku
        if (self.description):
            vals["Description"] = self.description
        vals["ProductPrice"] = self.price
        if (self.isActive>=0):
            vals["Status"] = self.isActive
        if (self.shortDescription):
            vals["ShortDescription"]=self.shortDescription
        if (self.taxable>=0):
            vals["Taxable"]=self.taxable
        if (self.cityTax>=0):
            vals["CityTax"]=self.cityTax
        if (self.stateTax>=0):
            vals["StateTax"] = self.stateTax
        if (self.countryTax>=0):
            vals["CountryTax"] = self.countryTax
        if (self.shippable>=0):
            vals["Shippable"] = self.shippable
        if (self.weight):
            vals["Weight"] = self.weight
        return vals

    def getPublicPage(self):
        return "https://" + server.infusionsoftapp + ".infusionsoft.com/app/storeFront/showProductDetail?productId=" + str(self.id)

    def getInternalPage(self):
        return "https://" + server.infusionsoftapp + ".infusionsoft.com/app/product/manageProduct?productId=" + str(self.id)

class productCat(object):
    global productCatagories
    def __init__(self, name):
        self.name=name
        self.children=[]
        self.image=None
        self.order=None
        self.id=None
        self.parent=0

    def register(self):
        if self.parent in [None,0]:
            self.parent = 0
            self.path=""+self.name
        else:
            self.path=productCatagories[self.parent].path+"/"+self.name
        productCatagories[self.path]=self
        if self.id is not None:
            productCatagories[self.id]=self


    def prepare(self):
        vals={}
        vals["CategoryDisplayName"] = self.name
        if (self.order is not None):
            vals["CategoryOrder"] = self.order
        if self.parent is not None:
            vals["ParentId"] = self.parent
        if self.image is not None:
            vals["CategoryImage"]
        return vals

    def allVals(self):
        vals={}
        if self.id is not None:
            vals['Id'] = self.id
        vals.update(self.prepare)
        return vals

class prodCatAss(object):

    def __init__(self, productId, catId):
        self.pid = productId
        self.catId = catId
        self.id=None

    def prepare(self):
        vals = {}
        vals["ProductCategoryId"] = self.catId # I admit, I feel dirty using that as a variable
        vals["ProductId"] = self.pid
        return vals

    def allVals(self):
        vals={}
        if self.id is not None:
            vals['Id'] = self.id
        return vals.update(self.prepare())

class prodOption(object):

    def __init__(self, productId):
        self.ProductId = productId
        self.id=None
        self.allowSpaces=None
        self.canContain=None
        self.canEndWith=None
        self.maxChars=None
        self.minChars=None
        self.name=None
        self.label=None
        self.required=None
        self.order=None
        self.optionType=None
        self.textMessage=None
        self.values=[]

    def prepare(self):
        vals={}
        vals["ProductId"] = self.ProductId
        if self.allowSpaces is not None:
            vals["AllowSpaces"] = self.allowSpaces
        if self.canContain is not None:
            vals["CanContain"] = self.canContain
        if self.canEndWith is not None:
            vals["CanEndWith"] = self.canEndWith
        if self.maxChars is not None:
            vals["MaxChars"] = self.maxChars
        if self.minChars is not None:
            vals["MinChars"] = self.minChars
        if self.name is not None:
            vals["Name"] = self.name
        if self.label is not None:
            vals["Label"] = self.label
        if self.required is not None:
            vals["IsRequired"] = self.required
        if self.order is not None:
            vals["Order"] = self.order
        if self.optionType is not None:
            vals["OptionType"] = self.optionType
        if self.textMessage is not None:
            vals["TextMessage"] = self.textMessage
        return vals

    def allVals(self):
        vals={}
        if self.id is not None:
            vals["Id"] = self.id
        return vals.update(self.prepare())


class prodOptVal(object):

    def __init__(self, optionID):
        self.id=None
        self.optionID = optionID
        self.label=None
        self.sku=None
        self.isdefault=None
        self.name=None
        self.optionIndex=None
        self.adjustment=None

    def prepare(self):
        vals={}
        vals["ProductOptionId"] = self.optionID
        if self.label is not None:
            vals["Label"] = self.label
        if self.sku is not None:
            vals["Sku"] = self.sku
        if self.isdefault is not None:
            vals["IsDefault"] = self.isdefault
        if self.name is not None:
            vals["Name"] = self.name
        if self.optionIndex is not None:
            vals["OptionIndex"] = self.optionIndex
        if self.adjustment is not None:
            vals["PriceAdjustment"] = self.adjustment
        return vals

    def allVals(self):
        vals={}
        if self.id is not None:
            vals["Id"] = self.id
        return vals.update(self.prepare())



    def __init__(self, optionID):
        self.id=None
        self.optionID = optionID
        self.label=None
        self.sku=None
        self.isdefault=None
        self.name=None
        self.optionIndex=None
        self.adjustment=None

    def prepare(self):
        vals={}
        vals["ProductOptionId"] = self.optionID
        if self.label is not None:
            vals["Label"] = self.label
        if self.sku is not None:
            vals["Sku"] = self.sku
        if self.isdefault is not None:
            vals["IsDefault"] = self.isdefault
        if self.name is not None:
            vals["Name"] = self.name
        if self.optionIndex is not None:
            vals["OptionIndex"] = self.optionIndex
        if self.adjustment is not None:
            vals["PriceAdjustment"] = self.adjustment
        return vals

    def allVals(self):
        vals={}
        if self.id is not None:
            vals["Id"] = self.id
        return vals.update(self.prepare())



def buildCategories(force=False):
    global productCatagories
    global server
    global tables
    if (len(productCatagories)==0 or force):
        allCategories=server.getAllRecords('ProductCategory', tables['ProductCategory'])
        catHold=[]
        for eachCategory in allCategories:
            thisCat = productCat(eachCategory['CategoryDisplayName'])
            thisCat.id=eachCategory['Id']
            if eachCategory["ParentId"] is not None:
                thisCat.parent=eachCategory["ParentId"]
            if eachCategory["CategoryImage"] is not None:
                thisCat.CategoryImage=eachCategory["CategoryImage"]
            if eachCategory["CategoryImage"] is not None:
                thisCat.order=eachCategory["CategoryImage"]
            catHold.append(thisCat)
        for eachCat in [cat for cat in catHold if cat.parent in[None,0]]:
            eachCat.register()
        while True:
            repeat=False
            for eachCategory in catHold:
                try:
                    eachCategory.register()
                except KeyError:
                    # print KeyError.args
                    # print KeyError.message
                    repeat=True
            if not repeat:
                break


def getCatId(pathToCat):
    global productCatagories
    global iditerator
    global server
    buildCategories()
    checkPath = '/'+pathToCat
    # if (checkPath[0] != '/'):
    #     checkPath = '/' + pathToCat
    if pathToCat in productCatagories.keys():
        return productCatagories[pathToCat].id
    else:
        pathData=pathToCat.rsplit('/',1)
        if len(pathData)==1:
            thisCat = productCat(pathData[0])
        else:
            thisCat = productCat(pathData[1])
            thisCat.parent=getCatId(pathData[0])
        thisCat.id=server.createNewRecord('ProductCategory', thisCat.prepare())
        thisCat.register()
        return thisCat.id

def getCatAssiggnId(productCatAssRecord):
    global server
    global tables
    matchingRecords=server.getMatchingRecords( "ProductCategoryAssign", productCatAssRecord.prepare(), tables["ProductCategoryAssign"])
    if len(matchingRecords)>0:
        return matchingRecords[0]["Id"]
    else:
        return server.createNewRecord("ProductCategoryAssign", productCatAssRecord.prepare())

def sampleData(productsExport=pw.passwords['importFile'], ISinteract=None):
    if ISinteract is None:
        return "I must have an ISinteract instance to run"
    global server
    global products
    global productCatagories
    blankProd=product("")
    server = ISinteract
    thisProduct=None
    with open(productsExport) as datas:
        reader = csv.DictReader(datas)
        for row in reader:
            if (len(row["Name"])>0 and row["Name"][0]=="["):
                #This indicates that it is not a product
                if (row["Price"]==""):
                    # If the price value is blank, this means
                    # that it is an option, not a pricing rule
                    optionString=row["Name"]
                while(len(optionString)>0):
                    # Basically we are going to eat and parse
                    # the string from the beginning. While it
                    # still exists we are going to continue to eat
                    # Every series of options
                    # follows the similar pattern
                    # "[RB]Center Hole=5/8-11 thread,[RB]# Segment=12"
                    # "[RB]Glass Weight=10 lb bag,[CS]Colors=Premium- Pineapple:2037.preview.jpg,Colors=Premium- Strawberry:2038.preview.jpg,Colors=Premium- Tangerine:2039.preview.jpg"
                    # Our first objective will be to split the string by its options.
                    # An option actually exists between "]" and ",["
                    # This may be counterintuitive because we are starting at the "]"
                    # and not the "[", but we do not use the tag for anything
                    optionStartCharacter="]"
                    optionEndCharacter="["
                    optionString=optionString[optionString.find(optionStartCharacter):]
                    nextOption=optionString.find(optionEndCharacter)
                    fulloption=optionString[:nextOption-1] #This minus one is an attempt to leave the next "[" intact
                    theseoptions=fulloption.split(",")
                    for eachoption in theseoptions:
                        optionName, eachoptionValue=eachoption.split("=")
                        if ":" in eachoptionValue:
                            eachoptionValue=eachoptionValue.split(":")[0]
                        if thisProduct.optionsSettings is None:
                            thisProduct.optionsSettings={}
                        if optionName not in thisProduct.optionsSettings.keys():
                            thisProduct.optionsSettings[optionName] = set()
                        thisProduct.optionsSettings[optionName.replace('-_-',",")].add(eachoptionValue.replace('-_-',","))
                else:
                    # This is a pricing rule
                    # This could also be a special pricing rule, like these:
                    # 3204,,,,,"[RB]Size=9"",Size=9.5"",Size=10.5""",,,,,[ADD]24,1,,,,,,,,"  Rule",Y,0
                    # 54,,,,,"[RB]Diameter=5"" (125mm)",,,,,[ADD]16,1,,,,,,,,"['  Rule', '[ADD]1', 'Y', '0']"
                    # 55,,,,,"[RB]Diameter=7"" (180mm)",,,,,[REMOVE]33,1,,,,,,,,"['  Rule', '[ADD]2', 'Y', '0']"
                    # The way to approach these will be remove the tag id
                    # Split on commas to get the correct options
                    # for each of the options, make sure that the option is created in the product
                    # And then set a price rule to it.
                    priceChange = row["Price"][row["Price"].find("]"):]
                    optionsN
                    optionChoice, optionChoiceValue = row["Name"][4:].split("=",1)
                    if thisProduct.optionsPriceChange is None:
                        thisProduct.optionsPriceChange={}
                    if optionChoice not in thisProduct.optionsPriceChange.keys():
                        thisProduct.optionsPriceChange[optionChoice]={}
                    thisProduct.optionsPriceChange[optionChoice][optionChoiceValue] = priceChange
            else:
                #this is a product
                if thisProduct is not None:
                    # This is to save the just completed product. 
                    # so that we can access it later, and assign its variable to 
                    # a different object. (Okay, really assign a different object
                    # to this variable ) We do not want to call it before the first
                    # product is created, hence the if to check.
                    products.append(thisProduct)
                thisProduct = product(row["Name"].translate(stringTranslation))
                for column in ["GPS Category", "Brand", "Category String"]:
                    thisProduct.catStrings.append(row[column].translate(stringTranslation))
                if row["SKU"]:
                    thisProduct.sku = row["SKU"].translate(stringTranslation)
                if row['Description']:
                    thisProduct.description=row['Description'].translate(stringTranslation)
                if row["Price"]:
                    thisProduct.price = row["Price"]
                if row["Product Images"]:
                    thisProduct.imageStrings.append(row["Product Images"])
                if row["Meta Description"]:
                    thisProduct.shortDescription = row["Meta Description"].translate(stringTranslation)
                if row["Product Images"]:
                    imageStrings=row["Product Images"].split("|")
                    for eachS in imageStrings:
                        for eachVal in eachS.split(","):
                            if "Product Image URL: " in eachVal:
                                thisProduct.images.append(eachVal.replace("Product Image URL: ","").strip())

                thisProduct.id = server.cnp(thisProduct.prepare())
                values=thisProduct.prepare()
                print "Product Created: " + str(thisProduct.id) 
                for x in values:
                    print(x + ":"+ str(values[x]))
                print "Product Created: " + str(thisProduct.id) 
                print thisProduct.getPublicPage()
                print thisProduct.getInternalPage()
                # if thisProduct.images:
                #     productImage.addImageToProduct(thisProduct.id, thisProduct.images[0])
                # thisProduct.id=iditerator.next()
    # we need to save the last product somewhere after it gets created. 
    products.append(thisProduct)
    ####
    ##
    # Products have been created and have their optionsp set up.
    # Let's create the actual optionsp.
    for eachProduct in products:
        if eachProduct.optionsSettings:
            if eachProduct.options is None:
                eachProduct.options = {}
            counter=0
            for eachOption in eachProduct.optionsSettings.keys():
                counter+=1
                thisOption = prodOption(eachProduct.id)
                thisOption.name=eachOption
                thisOption.label = eachOption
                thisOption.required = 1
                thisOption.order = counter
                thisOption.optionType='FixedList'
                thisOption.id = server.createNewRecord("ProductOption", thisOption.prepare())
                # thisOption.id=iditerator.next()
                eachProduct.options[eachOption] = thisOption
                optionCounter=0
                for eachValue in eachProduct.optionsSettings[eachOption]:
                    optionCounter+=1
                    newOptionValue=prodOptVal(thisOption.id)
                    newOptionValue.optionIndex=optionCounter
                    newOptionValue.label = eachValue
                    newOptionValue.isdefault=0
                    newOptionValue.name=eachValue
                    if eachOption in eachProduct.optionsPriceChange.keys():
                        if eachValue in eachProduct.optionsPriceChange[eachOption].keys():
                            newOptionValue.adjustment=eachProduct.optionsPriceChange[eachOption][eachValue]
                    newOptionValue.id = server.createNewRecord("ProductOptValue", newOptionValue.prepare())
                    # newOptionValue.id = iditerator.next()
                    thisOption.values.append(newOptionValue)
        # each product option has been created and assigned. 
        # lets take care of the categories.
        for eachString in eachProduct.catStrings:
            if eachProduct.categories is None:
                eachProduct.categories={}
            eachString.replace("\\/", " - ")
            for eachSubstring in eachString.split(";"):
                #The string should now be something like
                # ParentCat/ChildCat/grandChildCat
                thiscatid=getCatId(eachSubstring)
                thisAssignment=prodCatAss(eachProduct.id, thiscatid)
                thisAssignment.id=getCatAssiggnId(thisAssignment)
                eachProduct.categories[eachSubstring]=eachProduct.categories[int(thiscatid)]=thisAssignment
        # for lastEachProduct in products:
        #     if lastEachProduct.images:
        #         print "uploading image from " + lastEachProduct.images[0]
        #         productImage.addImageToProduct(lastEachProduct.id, lastEachProduct.images[0])
    return products