import os
import sys
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser

pages={}
pages['queues'] = "http://support.infusiontest.com/csdashboard/queues.php"
pages['general'] = "http://support.infusiontest.com/csdashboard/general.php"
pages['stats'] = "http://support.infusiontest.com/csdashboard/stats.php"
pages['submit'] = "https://docs.google.com/forms/d/1UvD_au-S6YaDGQ-u23Lth5l-JFrrpUiQT6yVFrj64BA/viewform"
chat={}
phone={}

def main():
	browser = RoboBrowser(history=True)
	##
	# First to get the stuff off of the general page.  
	#
	# There is the Presented, Handled, abandoned
	browser.open("http://support.infusiontest.com/csdashboard/general.php")
	generalresults = BeautifulSoup(browser.response.content, 'html.parser')
	phone['presented'] = generalresults.find('div', {'id': 'presented'}).find('div', {'class': 'data'}).text.strip('\r\n ')
	phone['abandoned'] = generalresults.find('div', {'id': 'queued'}).find('div', {'class': 'data'}).text.strip('\r\n ')
	phone['handled'] = generalresults.findAll('div', {'id': 'handled'})[0].find('div', {'class': 'data'}).text.strip('\r\n ')
	phone['abandonedpct'] = generalresults.findAll('div', {'id': 'handled'})[1].find('div', {'class': 'data'}).text.strip('\r\n ')
	chat['presented'] = generalresults.find('div', {'id': 'diverted'}).find('div', {'class': 'data'}).text.strip('\r\n ')
	chat['abandoned'] = generalresults.find('div', {'id': 'sla'}).find('div', {'class': 'data'}).text.strip('\r\n ')
	chat['handled'] = generalresults.find('div', {'id': 'abandoned'}).find('div', {'class': 'data'}).text.strip('\r\n ')
	chat['abandonedpct'] = generalresults.find('div', {'id': 'asa'}).find('div', {'class': 'data'}).text.strip('\r\n ')
	print phone, chat

