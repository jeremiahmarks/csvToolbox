#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-10-27 13:50:51
# @Last Modified 2015-10-27

import cgi
import cgitb

import htmlparts

cgitb.enable()

def applesauce(postdata):
  pagedata = htmlparts.prehead() + htmlparts.htmlHead() + htmlparts.gatherInfo() + htmlparts.footer()
  print pagedata

if __name__ == '__main__':
  postdata=cgi.FieldStorage()
  applesauce(postdata)
