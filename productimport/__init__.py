#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-21 20:31:15
# @Last Modified 2015-06-22
# @Last Modified time: 2015-06-22 01:39:40

import my_pw
import ISServer
from Managers import ProductManager as pm
from Managers import ProductCatMan as pcm
from Managers import ProdCatAssMan as pcam
from Managers import ProductOptMan as pom
from Managers import ProdOptValMan as povm
server=ISServer.ISServer(my_pw.passwords['appname'],my_pw.passwords['apikey'])
thispm=pm.ProductManager(server)
thispcm=pcm.ProductCategoryManager(server)
thispcam=pcam.ProductCategoryAssignManager(server)
thispom = pom.ProductOptionManager(server)
thispovm = povm.ProductOptValueManager(server)