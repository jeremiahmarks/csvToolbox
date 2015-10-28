#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-10-26 10:24:40
# @Last Modified 2015-10-26


user="Robot@jlmarks.org"
pasw="62IS1DSDBgyTM8b7GUl"


client_id = "aa8fnmbza344ypd9anqeq62v"
redirect_uri = "http://jlmarks.org/infusionsoftcallback"
response_type = "code"
scope = "all"
permissionparams={}
permissionparams['client_id'] = client_id
permissionparams['redirect_uri'] = redirect_uri
permissionparams['response_type'] = response_type
permissionparams['scope'] = scope

requestparams={}
requestparams['client_id'] = client_id
requestparams['client_secret'] = client_secret
requestparams['code'] = code
requestparams['grant_type'] = 'authorization_code'
requestparams['redirect_uri'] = 'redirect_uri'

refreshparams={}
refreshparams['grant_type']='refresh_token'
refreshparams['refresh_token']=''
refreshHeaderInfo="""Header: Authorization: string (required)
The word "Basic" concatenated with a base64 encoded string of your client_id, a colon, and your client_secret passed via the Authorization header. 

Example pseudo code: 'Basic ' + base64_encode(CLIENT_ID + ':' + CLIENT_SECRET)"""
from robobrowser import RoboBrowser

class oauthtest:
	"""This is a basic OAuth example for the Infuisionsoft
	API written in Python.
	"""
	permissionsurl='https://signin.infusionsoft.com/app/oauth/authorize'
	accesstokenurl='https://api.infusionsoft.com/token'

	def __init__(self, un="Robot@jlmarks.org", pw='62IS1DSDBgyTM8b7GUl', appname='if188', **kwargs):
		self.un = un
		self.pw = pw
		self.appname=appname
		self.client_id="aa8fnmbza344ypd9anqeq62v"
		self.secret="VsNrwPpHDN"
		self.redirect_uri = "http://jlmarks.org/infusionsoftcallback"
		self.browser = RoboBrowser(history=True)

	def get_permission(self):
		permissionsdata={"client_id": "aa8fnmbza344ypd9anqeq62v" , "redirect_uri": "http://jlmarks.org/infusionsoftcallback" , "response_type": "code" , "scope": "full"}
		self.browser._update_state(self.browser.session.request("post", oauthtest.permissionsurl, data=permissionsdata))
		thisform = self.browser.get_form()
		thisform.fields['username'].value=self.un
		thisform.fields['password'].value = self.pw
		self.browser.submit_form(thisform)


