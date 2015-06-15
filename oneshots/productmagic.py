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


try:
    from my_pw import pw
except:
    collectcredentials()

def collectcredentials():
    global pw
    if 'pw' not in globals():
        pw={}
    pw['appname']=raw_input("\nAppname: ")
    pw['apikey']=raw_input('\napikey: ')
    pw['un']=raw_input('\nUsername: ')
    pw['pw']=raw_input('\nPassword: ')

def getAllExistingProducts():
    """
        This method expects a dictionary containing ['appname'] and ['apikey'] is
        available in the global pw variable.
        If there is not a global dictionary named "productsbyid". If there is
        not it will create one. 
        This global variable will allow other methods to access the products by ID
        It will also create a global dictionary named categories, options, category assignment
        and option assignement. It will populate those as though they were a sql database.
    """
    global productsbyid
    if 'productsbyid' not in globals():
        productsbyid={}
    
