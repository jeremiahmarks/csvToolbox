#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-16 04:02:35
# @Last Modified 2015-06-16>
# @Last Modified time: 2015-06-16 04:03:12

from my_pw import passwords

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib2
import urllib
import os
loggedIn=False

def login():
    global loggedIn
    global driver
    global passwords
    if not loggedIn:
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get("https://" + passwords['appname'] + ".infusionsoft.com")
        elem = driver.find_element_by_id('username')
        elem.send_keys(passwords["username"])
        elem = driver.find_element_by_id('password')
        elem.send_keys(passwords["password"])
        elem.send_keys(Keys.RETURN)
        loggedIn=True

def downloadImage(imageurl):
    file_name = imageurl.split('/')[-1]
    urllib.urlretrieve(imageurl, file_name)
    return file_name

def addImageToProduct(productID, imageurl):
    global loggedIn
    global passwords
    if not loggedIn:
        login()
    file_name = downloadImage(imageurl)
    folderPath = os.getcwd()
    filePath=folderPath+"/"+file_name
    driver.get("https://" + passwords['appname'] + ".infusionsoft.com/app/product/manageProduct?productId="+str(productID))
    elem=driver.find_element_by_link_text("Product Image")
    elem.click()
    driver.execute_script("document.getElementsByClassName('inf-fileupload-text')[0].setAttribute('readonly', 'false')")
    #driver.find_element_by_id("productImage").clear()
    driver.find_element_by_id("productImage").send_keys(filePath)
    driver.find_element_by_id("uploadStyledCartImageButton").click()
