#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-14 18:49:15
# @Last Modified 2015-06-16
# @Last Modified time: 2015-06-16 03:42:13
# This is the oneshot code for this product import

# Flow of operations:
    # Collect appname, apikey, username, password
        # Note: This will either assume that you have login
        # credentials to the account, or will automate image
        # upload based on internal access. This version, 
        # being public, will probably assume that you have 
        # access to the account. If you have internal access
        # contact me and we will talk about how to automate
        # that.
    # Retrieve current list of products via the API
        # Data needed: productID, productName, categories that
        #   product is assigned to, and produtSku. 
        #       TODO later: If the sku is NONE the program 
        #       should set the actual sku to ''. This would 
        #       allow it to change the SKU if desired
        #  Note that the sku is an optional identifier, however
        #  due to the concept of having a copy of a product
        #  show on your homepage, the categories are not.
    # Parse the csv file into a dictionaries that equate to SQL tables for 
    # Products, Product Categories, Product options, Products to product categories relationships, and product options to product relationships.
    # Dupe check the existing products based on SKU, Category assignment, and Name
    # Move found duplicates to a created dictionary which will include their ProductID
    # Create the products that were not moved, as they do not have duplicates
    # As they are created move the item to the created dictionary.
    # Check each item for assigned options.
        # If none exist:
            # If there is a path to an image, add the item
            #   to an imageupload dictionary.
        # If options exist:
            # check if any of the product options have  
            #   been created. 
            # Create product options which have not been created
            # If there is an image path, add the item to the
            #   imageupload dictionary.
        # remove the item from created dictionary.
    # upload image
import simpleIS
import productObjects
import csv
temhousingqueue={}
temhousingqueuecounter=0

try:
    from my_pw import pw
except:
    collectcredentials()

tables={}
tables["Product"] = ["BottomHTML", "CityTaxable", "CountryTaxable", "Description", "HideInStore", "Id", "InventoryLimit", "InventoryNotifiee", "IsPackage", "LargeImage", "NeedsDigitalDelivery", "ProductName", "ProductPrice", "Shippable", "ShippingTime", "ShortDescription", "Sku", "StateTaxable", "Status", "Taxable", "TopHTML", "Weight"]
tables['ProductOptValue'] = ["Id", "IsDefault", "Label", "Name", "OptionIndex", "PriceAdjustment", "ProductOptionId", "Sku",]
tables['ProductOption'] = ["AllowSpaces", "CanContain", "CanEndWith", "CanStartWith", "Id", "IsRequired", "Label", "MaxChars", "MinChars", "Name", "OptionType", "Order", "ProductId", "TextMessage"]
tables['ProductCategory'] = ["CategoryDisplayName", "CategoryImage", "CategoryOrder", "Id", "ParentId"]
tables["ProductCategoryAssign"]=["Id","ProductCategoryId","ProductId"]

class temphousing(object):
    """This is just a simple class. It gives you a location
    to hold data. It will then process the data and crate the 
    appropriate records.
    """
    def __init__(self, productrow):
        global temhousingqueue
        global temhousingqueuecounter
        temhousingqueuecounter+=1
        temhousingqueue[temhousingqueuecounter]=self
        self.productrow=productrow
        self.childrow=0
        self.optionsrows={}
        self.pricingrulerows={}
        self.options={}
        self.processSelf()


    def addoptionsrow(self, optionsrow):
        self.optionsrows.append(optionsrow)

    def addpricingrulerow(self, pricingrulerow):
        self.pricingrulerows.append(pricingrulerow)

    def processSelf(self):
        self.productValues={}

        if len(self.productrow['SKU']) > 0:
            # something exists in  'SKU',
            self.productValues["Sku"] = self.productrow["SKU"]

        if len(self.productrow['Allow Purchases']) > 0:
            # something exists in  'Allow Purchases',
            if self.productrow["Allow Purchases"] == "1":
                self.productValues['Status']='1'

        if len(self.productrow['Meta Description']) > 0:
            # something exists in  'Meta Description',
            self.productValues["ShortDescription"]=self.productrow['Meta Description']

        if len(self.productrow['GPS Manufacturer Part Number']) > 0:
            # something exists in  'GPS Manufacturer Part Number',
            # check with email and verify how to process
            # until then
            pass

        if len(self.productrow['Brand']) > 0:
            # something exists in  'Brand',
            # check if there is a category created callend
            # "Brands". If there is not, create it.
            # Create the category "Brands"/self.productrow['Brand']
            # and assign self to that category
            pass

        if len(self.productrow['Product Images']) > 0:
            # something exists in  'Product Images',
            self.imagurl=self.productrow["Product Images"][self.productrow["Product Images"].find('URL:')+4: self.productrow["Product Images"].find(',',self.productrow["Product Images"].find('URL:'))]

        if len(self.productrow['GPS Category']) > 0:
            # something exists in  'GPS Category',
            # check if there is a category created callend
            # "GPS Category". If there is not, create it.
            # Create the category "GPS Category"/self.productrow['GPS Category']
            # and assign self to that category
            pass

        if len(self.productrow['Category String']) > 0:
            # something exists in  'Category String',
            # This breaks down all of the categories
            # Process these as categories
            ##
            pass

        if len(self.productrow['Product Files']) > 0:
            # something exists in  'Product Files',
            ##unknown
            pass

        if len(self.productrow['Option Set']) > 0:
            # something exists in  'Option Set',
            # potential categories or options related.
            pass

        if len(self.productrow['Description']) > 0:
            # something exists in  'Description',
            self.productValues["Description"]=self.productrow['Description']

        if len(self.productrow['Price']) > 0:
            self.productValues["ProductPrice"] = self.productrow['Price']

        if len(self.productrow['Name']) > 0:
            # something exists in  'Name'
            self.productValues["ProductName"] = self.productrow['Name']

    def processoptions(self):
        for eachnum, eachoptionrow in enumerate(self.optionsrows):
            self.options[eachnum]={}
            if len(eachoptionrow['SKU']) > 0:
                # something exists in  'SKU',
                self.options[eachnum]['SKU']= eachoptionrow['SKU']

            if len(eachoptionrow['Allow Purchases']) > 0:
                # something exists in  'Allow Purchases',
                self.options[eachnum]['Allow Purchases']= eachoptionrow['Allow Purchases']

            if len(eachoptionrow['Meta Description']) > 0:
                # something exists in  'Meta Description',
                self.options[eachnum]['Meta Description']= eachoptionrow['Meta Description']

            if len(eachoptionrow['GPS Manufacturer Part Number']) > 0:
                # something exists in  'GPS Manufacturer Part Number',
                # check with email and verify how to process
                # until then
                self.options[eachnum]['GPS Manufacturer Part Number']= eachoptionrow['GPS Manufacturer Part Number']

            if len(eachoptionrow['Brand']) > 0:
                # something exists in  'Brand',
                # check if there is a category created callend
                # "Brands". If there is not, create it.
                # Create the category "Brands"/eachoptionrow['Brand']
                # and assign self to that category
                self.options[eachnum]['Brand']= eachoptionrow['Brand']

            if len(eachoptionrow['Product Images']) > 0:
                # something exists in  'Product Images',
                self.options[eachnum]['Product Images']= eachoptionrow['Product Images']

            if len(eachoptionrow['GPS Category']) > 0:
                # something exists in  'GPS Category',
                # check if there is a category created callend
                # "GPS Category". If there is not, create it.
                # Create the category "GPS Category"/eachoptionrow['GPS Category']
                # and assign self to that category
                self.options[eachnum]['GPS Category']= eachoptionrow['GPS Category']

            if len(eachoptionrow['Category String']) > 0:
                # something exists in  'Category String',
                # This breaks down all of the categories
                # Process these as categories
                ##
                self.options[eachnum]['Category String']= eachoptionrow['Category String']

            if len(eachoptionrow['Product Files']) > 0:
                # something exists in  'Product Files',
                ##unknown
                self.options[eachnum]['Product Files']= eachoptionrow['Product Files']

            if len(eachoptionrow['Option Set']) > 0:
                # something exists in  'Option Set',
                # potential categories or options related.
                self.options[eachnum]['Option Set']= eachoptionrow['Option Set']

            if len(eachoptionrow['Description']) > 0:
                # something exists in  'Description',
                self.options[eachnum]['Description']= eachoptionrow['Description']

            if len(eachoptionrow['Price']) > 0:
                self.options[eachnum]['Price']= eachoptionrow['Price']

            if len(eachoptionrow['Name']) > 0:
                # something exists in  'Name'
                self.options[eachnum]['Name']= eachoptionrow['Name']


def processproductsfile(pathtoproductfile):
    global temhousingqueue
    """This method will open a the specified file. 
    This method expects the file to be in a very particular format.
    """
    ########################################################
    ##
    ##  TL:DR - I established what the patterns where in the data
    ##  by making it binary , and then established three
    ##  basic types.
    ##
    ##
    ##  These are the various patterns that are anywhere
    ##  In the document.  
    ## A column with a "1" indicates there was data in the 
    ##  cell. A "0" indicates there is not. 
    ## This can be replicated using the "replacefieldnames"
    ##  function in this file:  
    ##  https://github.com/jeremiahmarks/csvToolbox/blob/e434bef57f254876848bed190656c5196fc00764/reduceCSVToFindPattern.py
    ##
    # product         01110111101010101110
    # product         01110111101010111110
    # product         01110111101110111110
    # product         01111111101110111110
    # product         11110011100010011110
    # product         11110111001010111110
    # product         11110111101010111110
    # product         11110111101110011110
    # product         11110111101110111110
    # product         11110111111010111110
    # product         11111011000110011110
    # product         11111011101110111110
    # product         11111111001110011110
    # product         11111111001110111110
    # product         11111111011110011110
    # product         11111111101110011110
    # product         11111111101110111110
    # product         11111111110110111110
    # product         11111111111110011110
    # product         11111111111110111110
    # product-DATED   11111111111111011110
    # product-TESTING 01110011001010011110
    # products meet this pattern. Basically,
    # if it is a product row it will meet 
    # this scheme
    #                 -111--11----1---1110
    # 
    # category        01110011001010001100
    # The category is a singluar item. It will get dropped
    # 
    # onlysku         11000000001010000100
    # These appear to be back up images for the main product
    #
    # option          01000000000010000101
    # option          01000000001010000101
    # option          10000000000010000101
    # option          11000000000010000101
    # All of these are options.
    # If it is an option, it will fit this
    # pattern         --00000000-010000101
    #
    # pricingrule    11000000000010000110
    # pricingrule     01000000000010000111
    # pricingrule     01000000001010000111
    # pricingrule     11000000000010000111
    # pricingrule     11000000001010000110
    # Here is this pattern:
    #                 -100000000-01000011-
    # Compare the four patterns   0 1 0
    #   product       - 1 1 1 - - 1 1 - - - - 1 - - - 1 1 1 0
    #   product       - - - - - - - - - - - - - - - - 1 - 1 -
    #   category      0 1 1 1 0 0 1 1 0 0 1 0 1 0 0 0 1 1 0 0
    #   option        - - 0 0 0 0 0 0 0 0 - 0 1 0 0 0 0 1 0 1
    #   option        - - - - - - - - - - - - - - - - 0 1 0 -
    #   pricingrule   - 1 0 0 0 0 0 0 0 0 - 0 1 0 0 0 0 1 1 -
    #   pricingrule   - - - - - - - - - - - - - - - - 0 1 1 -
    # note that product and category are the exact same
    # except for the name field
    #
    # These are our final templates to determine which type
    # of row we are working on. 
    #   product       ----------------1-1-
    #   category      01110011001010001100
    #   option        ----------------010-
    #   pricingrule   ----------------011-
    #
    # product: len(Product Images)>0 and len(Product Condition)>0
    # option: len(Product Images)==0 and len(Meta Description)>0  and len(Product Condition)==0
    # pricingrule: len(Product Images)==0 and len(Meta Description)>0  and len(Product Condition)==1


    csvColumns=[
                 'SKU',
                 'Allow Purchases',
                 'Product Condition',
                 'GPS Enabled',
                 'GPS Manufacturer Part Number',
                 'Meta Description',
                 'Category Details',
                 'Product URL',
                 'Brand',
                 'Product Availability',
                 'Product Images',
                 'GPS Category',
                 'Category String',
                 'Product Files',
                 'Option Set',
                 'Description',
                 'NameID',
                 'Price',
                 'Name'
                 ]



    with open(pathtoproductfile) as inputfile:
        thisreader=csv.DictReader(inputfile)
        thisproduct=None
        for eachrow in thisreader:
            print eachrow["NameID"], "NameID"
            print eachrow["Price"], "Price"
            print eachrow["Name"], "Name"
            if len(eachrow["NameID"]) > 0 and len(eachrow["Name"])>0 :
                thisproduct=temphousing(eachrow)
                print "product"
            if len(eachrow["NameID"])==0 and len(eachrow["Price"])>0  and len(eachrow["Name"])==0:
                thisproduct.addoptionsrow(eachrow)
                print "Images"
            if len(eachrow["NameID"])==0 and len(eachrow["Price"])>0  and len(eachrow["Name"])==1:
                thisproduct.addpricingrulerow(eachrow)
                print "pImagesp"
            else:
                print eachrow['SKU']
    return temhousingqueue

    # for eachproduct in temhousingqueue:
    #     if len(eachproduct.productrow["SKU"]) > 0:
    #         eachproduct.Sku=eachproduct.productrow["SKU"]







def collectcredentials():
    global pw
    if 'pw' not in globals():
        pw={}
    pw['appname']=raw_input("\nAppname: ").strip(' \n')
    pw['apikey']=raw_input('\napikey: ').strip(' \n')
    pw['un']=raw_input('\nUsername: ').strip(' \n')
    pw['pw']=raw_input('\nPassword: ').strip(' \n')
    pw['inputfilepath']=raw_input('\nFull path to inputFile: ').strip(' \n')

def getAllProducts():
    """
        This method expects a dictionary containing ['appname'] and ['apikey'] is
        available in the global pw variable.
        If there is not a global dictionary named "productsbyid". If there is
        not it will create one. 
        This global variable will allow other methods to access the products by ID
        It will also create a global dictionary named categories, options, category assignment
        and option assignement. It will populate those as though they were a sql database.
        tables["Product"] =
        [
                       "BottomHTML",  "ProductName"
                      "CityTaxable",  "ProductPrice"
                   "CountryTaxable",  "Shippable"
                      "Description",  "ShippingTime"
                      "HideInStore",  "ShortDescription"
                               "Id",  "Sku"
                   "InventoryLimit",  "StateTaxable"
                "InventoryNotifiee",  "Status"
                        "IsPackage",  "Taxable"
                       "LargeImage",  "TopHTML"
             "NeedsDigitalDelivery",  "Weight"
        ]
    """
    global integration
    global products
    if 'integration' not in globals():
        integration=simpleIS.ISinteract(pw['appname'], pw['apikey'])
    if 'products' not in globals():
        products={}
        products['Id']={}
        products['ProductName']={}

    if 'Id' not in products.keys():
        products['Id']={}
    if 'ProductName' not in products.keys():
        products['ProductName']=[]
    theserecords=integration.getAllRecords("Product", simpleIS.tables["Product"])
    # This pulls all of the fields for all of the created products. If you have a billion
    # products this should be reconsidered, but 10k products is only 10 API calls.
    for eachrecord in theserecords:
        thisproduct = productObjects.Product(eachrecord)
        products['Id'][thisproduct.Id]=thisproduct
        if thisproduct.ProductName not in products['ProductName'].keys():
            products['ProductName'][thisproduct.ProductName]=[]
        products['ProductName'][thisproduct.ProductName].append(thisproduct)

def getallcategories():
    """This method executes (as will all of the getall* methods) in 
    a manner very similar to the getAllProducts method.
    product categories contain:
    [
        "CategoryDisplayName"
        "CategoryImage"
        "CategoryOrder"
        "Id"
        "ParentId"
     ]
    """
    # The first thing we are going to do is ensure that the
    # the data structures that we need are in place. I am 
    # making the assumption that the variable is the correct
    # data structure before working with it, which could
    # be bad especially since these are globals, but this
    # is a oneshot, so .... "Don't do this at home"
    global categories
    if 'categories' not in globals():
        categories = {}
    if "CategoryDisplayName" not in categories.keys():
        categories["CategoryDisplayName"]={}
    if "Id" not in categories.keys():
        categories["Id"]={}
    if "ParentId" not in categories.keys():
        categories["ParentId"]={}
        # This may be a little counter intuitive. I intend the
        # data structure be categories["ParentId"][parentbyid]=set(childrenbyid)

    theserecords=integration.getAllRecords("ProductCategory", simpleIS.tables["ProductCategory"])
    # This pulls all of the fields for all of the created products. If you have a billion
    # products this should be reconsidered, but 10k products is only 10 API calls.
    for eachrecord in theserecords:
        thisproductcategory = productObjects.ProductCategory(eachrecord)
        #This creates a product object in the style defined in the productObjects.py file.

        if thisproductcategory.CategoryDisplayName not in categories["CategoryDisplayName"].keys():
            # If this is the first time that this category name has been seen,
            categories["CategoryDisplayName"][thisproductcategory.CategoryDisplayName] ={}
            # Add a dictionary with its name to the global
        categories["CategoryDisplayName"][thisproductcategory.CategoryDisplayName][thisproductcategory.Id]=thisproductcategory
        #No matter what this id used to point to, it will now point to this product category.
        # cross my fingers this never befomes a problem
        categories["Id"][thisproductcategory.Id] = thisproductcategory
        if thisproductcategory.ParentId not in categories["ParentId"].keys():
            categories["ParentId"][thisproductcategory.ParentId]=[]
        categories["ParentId"][thisproductcategory.ParentId].append(thisproductcategory)





    # tablesNeeded=["Product", "ProductCategory", "ProductCategoryAssign", "ProductOptValue", "ProductOption"]
    # # This is basically a list of the various tables needed for this import
    # for eachtable in tablesNeeded:
    #     globalname = eachtable.lower()
    #     # this takes the all lower case version of the name
    #     if str(globalname) not in globals():
    #         # See's if the variable has already been created
    #         exec("global "+ globalname)
    #         # If it has not, it declares itself a global variable
    #         exec(globalname + "= {}")
    #         # and sets itself to be an empty dictionary.
    #     theseRecords=integration.getAllRecords(eachtable, simpleIS.tables[eachtable])
    #     exec(globalname + "['allrecords']=theseRecords")

def getallcatassign():
    """this method will download all of the existing category
    assignments and create objects out of them.
    The available rows are
    tables["ProductCategoryAssign"]=["Id","ProductCategoryId","ProductId"]
    """
    global catassigns
    if 'catassigns' not in globals():
        catassigns={}
    if "Id" not in catassigns.keys():
        catassigns["Id"]={}
    if "ProductCategoryId" not in catassigns.keys():
        catassigns["ProductCategoryId"]={}
    if "ProductId" not in catassigns.keys():
        catassigns["ProductId"]={}

    theserecords=integration.getAllRecords("ProductCategoryAssign", simpleIS.tables["ProductCategoryAssign"])
    # This pulls all of the fields for all of the created products. If you have a billion
    # products this should be reconsidered, but 10k products is only 10 API calls.
    for eachrecord in theserecords:
        thisproductcategoryassign = productObjects.ProductCategoryAssign(eachrecord)
        catassigns['Id'][thisproductcategoryassign.Id]=thisproductcategoryassign

        if thisproductcategoryassign.ProductCategoryId not in catassigns['ProductCategoryId'].keys():
            catassigns['ProductCategoryId'][thisproductcategoryassign.ProductCategoryId]=[]
        catassigns['ProductCategoryId'][thisproductcategoryassign.ProductCategoryId].append(thisproductcategoryassign)

        if thisproductcategoryassign.ProductId not in catassigns['ProductId'].keys():
            catassigns['ProductId'][thisproductcategoryassign.ProductId]=[]
        catassigns['ProductId'][thisproductcategoryassign.ProductId].append(thisproductcategoryassign)




def getallproductoptions():
    """
    This method does what you expect it to.
    tables['ProductOption'] = 
    [
     "AllowSpaces"
     "CanContain"
     "CanEndWith"
     "CanStartWith"
     "Id"
     "IsRequired"
     "Label"
     "MaxChars"
     "MinChars"


     "Name"
     "OptionType"
     "Order"
     "ProductId"
     "TextMessage"
    ]
    Important for identification:
        Id
        Name
        ProductId
    """
    global productoptions
    if 'productoptions' not in globals():
        productoptions={}
    if "Id" not in productoptions.keys():
        productoptions['Id']={}
    if "Name" not in productoptions.keys():
        productoptions['Name']={}
    if "ProductId" not in productoptions.keys():
        productoptions['ProductId']={}

    theserecords=integration.getAllRecords("ProductOption", simpleIS.tables["ProductOption"])
        # This pulls all of the fields for all of the created products. If you have a billion
        # products this should be reconsidered, but 10k products is only 10 API calls.
    for eachrecord in theserecords:
        thisproductoption = productObjects.ProductOption(eachrecord)

        productoptions["Id"][thisproductoption.Id]=thisproductoption
        if eachrecord["Name"] not in productoptions["Name"].keys():
            productoptions["Name"][eachrecord["Name"]]=[]
        productoptions["Name"][eachrecord["Name"]].append(thisproductoption)
        if thisproductoption.ProductId not in productoptions["ProductId"].keys():
            productoptions["ProductId"][thisproductoption.ProductId]=[]
        productoptions["ProductId"][thisproductoption.ProductId].append(thisproductoption)

def getprooptval():
    """
    this works as expected. Available values are
    tables['ProductOptValue'] = 
    [
         "Id"
         "IsDefault"
         "Label"
         "Name"
         "OptionIndex"
         "PriceAdjustment"
         "ProductOptionId"
         "Sku"
    ]
    Ids of interest (I really need to formalize this description)
        "Id"
        "Name"
        "ProductOptionId"


        "Sku"
    """
    global prooptvals
    if "prooptvals" not in globals():
        prooptvals={}
    if "Id" not in prooptvals.keys():
        prooptvals["Id"]={}
    if "Name" not in prooptvals.keys():
        prooptvals["Name"]={}
    if "ProductOptionId" not in prooptvals.keys():
        prooptvals["ProductOptionId"]={}
    if "Sku" not in prooptvals.keys():
        prooptvals["Sku"]={}

        theserecords=integration.getAllRecords("ProductOption", simpleIS.tables["ProductOption"])
            # This pulls all of the fields for all of the created products. If you have a billion
            # products this should be reconsidered, but 10k products is only 10 API calls.
        for eachrecord in theserecords:
            thisproductoptionvalue = productObjects.ProductOptValue(eachrecord)

            prooptvals['Id'][thisproductoptionvalue.Id]=thisproductoptionvalue
            prooptvals['ProductOptionId'][thisproductoptionvalue.ProductOptionId]=thisproductoptionvalue
            # I expect ID to be unique to this product option value.
            # I also expect that it will only be associated with one product option id. 
            # If I am wrong on this, you may need to let me know.
            if thisproductoptionvalue.Name not in prooptvals["Name"].keys():
                prooptvals['Name'][thisproductoptionvalue.Name]=[]
            prooptvals['Name'][thisproductoptionvalue.Name].append(thisproductoptionvalue)
            if thisproductoptionvalue.Sku not in prooptvals["Sku"].keys():
                prooptvals['Sku'][thisproductoptionvalue.Sku]=[]
            prooptvals['Sku'][thisproductoptionvalue.Sku].append(thisproductoptionvalue)

#   We have built the method for querying and storing all of the applicable tables.
#   Now we will call for each of them to build

def buildTables():
    global products
    global categories
    global catassigns
    global productoptions
    global prooptvals

    getAllProducts()
    getallcategories()
    getallcatassign()
    getallproductoptions()
    getprooptval()


def writeToCsv():

    global products
    global categories
    global catassigns
    global productoptions
    global prooptvals

    with open('products_EXISTALREADY.csv','wb') as productsfile:
        productswriter=csv.DictWriter(productsfile, tables['Product'], extrasaction='ignore')
        productswriter.writeheader()
        for eachproductsid in products['Id'].keys():
            productswriter.writerow(products['Id'][eachproductsid].prepare())
    with open('categories_EXISTALREADY.csv','wb') as categoriesfile:
        categorieswriter=csv.DictWriter(categoriesfile, tables['ProductCategory'])
        categorieswriter.writeheader()
        for eachcategoriesid in categories["Id"].keys():
            categorieswriter.writerow(categories["Id"][eachcategoriesid].prepare())
    with open('catassigns_EXISTALREADY.csv','wb') as catassignsfile:
        catassignswriter=csv.DictWriter(catassignsfile, tables['ProductCategoryAssign'])
        catassignswriter.writeheader()
        for eachcatassignsid in catassigns["Id"]:
            catassignswriter.writerow(catassigns["Id"][eachcatassignsid].prepare())
    with open('productoptions_EXISTALREADY.csv','wb') as productoptionsfile:
        productoptionswriter=csv.DictWriter(productoptionsfile, tables['ProductOption'])
        productoptionswriter.writeheader()
        for eachproductoptionsid in productoptions['Id']:
            productoptionswriter.writerow(productoptions['Id'][eachproductoptionsid].prepare())
    with open('prooptvals_EXISTALREADY.csv','wb') as prooptvalsfile:
        prooptvalswriter=csv.DictWriter(prooptvalsfile, tables['ProductOptValue'])
        prooptvalswriter.writeheader()
        for eachprooptvalsid in prooptvals['Id']:
            prooptvalswriter.writerow(prooptvals['Id'][eachprooptvalsid].prepare())

def openinputcsv():
    with open(pw['inputfilepath']) as inputfile:
        inputReader=csv.DictReader(inputfile, restkey="unkeyed", restval=" ")
        for row in inputReader:
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
                # Example, complex pricing rule
                # 3204,,,,,"[RB]Size=9"",Size=9.5"",Size=10.5""",,,,,[ADD]24,1,,,,,,,,"  Rule",Y,0
                # Example options with sku that I need to get, and average pricing example
                # 63,DR04A,,,,"[RB]Diameter=4"" (100mm),[RB]Center Hole=5/8-11 thread",,,,,,,,,,,,,,"['  SKU', '', '0.00', '']"
                # 64,DR04K,,,,"[RB]Diameter=4"" (100mm),[RB]Center Hole=7/8""-5/8"" bore",,,,,,,,,,,,,,"['  SKU', '', '0.00', '']"
                # 65,DR05A,,,,"[RB]Diameter=5"" (125mm),[RB]Center Hole=5/8-11 thread",,,,,,,,,,,,,,"['  SKU', '', '0.00', '']"
                # 66,DR05K,,,,"[RB]Diameter=5"" (125mm),[RB]Center Hole=7/8""-5/8"" bore",,,,,,,,,,,,,,"['  SKU', '', '0.00', '']"
                # 67,DR07A,,,,"[RB]Diameter=7"" (180mm),[RB]Center Hole=5/8-11 thread",,,,,,,,,,,,,,"['  SKU', '', '0.00', '']"
                # 68,DR07K,,,,"[RB]Diameter=7"" (180mm),[RB]Center Hole=7/8""-5/8"" bore",,,,,,,,,,,,,,"['  SKU', '', '0.00', '']"
                # 54,,,,,"[RB]Diameter=5"" (125mm)",,,,,[ADD]16,1,,,,,,,,"['  Rule', '[ADD]1', 'Y', '0']"
                # 55,,,,,"[RB]Diameter=7"" (180mm)",,,,,[ADD]33,1,,,,,,,,"['  Rule', '[ADD]2', 'Y', '0']"
                priceChange = row["Price"][5:]
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
            thisProduct = product(row["Name"])
            for column in ["GPS Category", "Brand", "Category String"]:
                thisProduct.catStrings.append(row[column])
            if row["SKU"]:
                thisProduct.sku = row["SKU"]
            if row['Description']:
                thisProduct.description=row['Description']
            if row["Price"]:
                thisProduct.price = row["Price"]
            if row["Product Images"]:
                thisProduct.imageStrings.append(row["Product Images"])
            if row["Meta Description"]:
                thisProduct.shortDescription = row["Meta Description"]
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












if __name__ == '__main__':
    buildTables()
    writeToCsv()
    openinputcsv()