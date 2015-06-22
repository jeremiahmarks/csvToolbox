#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-06-21 20:31:15
# @Last Modified 2015-06-21
# @Last Modified time: 2015-06-21 23:47:54

import my_pw
import ISServer
from Managers import ProductManager as pm
from Managers import ProductCatMan as pcm
from Managers import ProdCatAssMan as pcam
server=ISServer.ISServer(my_pw.passwords['appname'],my_pw.passwords['apikey'])
thispm=pm.ProductManager(server)
thispcm=pcm.ProductCategoryManager(server)
thispcam=pcam.ProductCategoryAssignManager(server)