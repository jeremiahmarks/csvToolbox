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
# 1210668230 = 5pm
# 1210668230 = 6pm
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
	browser.open("http://support.infusiontest.com/csdashboard/stats.php")
	statsresults = BeautifulSoup(browser.response.content, 'html.parser')
	phone['asa'] = statsresults.find('div', {'id': 'phone'}).find('div', {'class': 'data'}).text.strip('\r\n ')
	chat['asa'] = statsresults.find('div', {'id': 'phone'}).find('div', {'class': 'data'}).text.strip('\r\n ')
	browser.open("https://docs.google.com/forms/d/1UvD_au-S6YaDGQ-u23Lth5l-JFrrpUiQT6yVFrj64BA/viewform")
	submitform = browser.get_form()	
	submitform.fields['entry.1210668230'].value = '5pm'
	submitform.fields['entry.339838906'].value = phone['asa']
	submitform.fields['entry.335804195'].value = phone['presented']
	submitform.fields['entry.950389349'].value = phone['handled']
	submitform.fields['entry.125377286'].value = phone['abandoned']
	submitform.fields['entry.73700777'].value = phone['abandonedpct']
	submitform.fields['entry.941849183'].value = chat['asa']
	submitform.fields['entry.1083299158'].value = chat['presented']
	submitform.fields['entry.487211652'].value = chat['handled']
	submitform.fields['entry.1724578827'].value = chat['abandoned']
	submitform.fields['entry.1590181783'].value = chat['abandonedpct']
	browser.submit_form(submitform)


if __name__ == '__main__':
	main()