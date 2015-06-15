#!/usr/bin/python
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