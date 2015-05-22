import urllib2
import filecmp
import os

SETTINGSFILE="csvsplittersettings"

class CSVSplitter(object):
	global SETTINGSFILE

	def loadSettings(self):
		cwd = os.getcwd()
		settingsFileName=os.path.abspath(os.path.join(cwd, SETTINGSFILE))
		if not os.path.isfile(settingsFileName):
			self.settingsFile=open(settingsFileName,'w+')
		else:
			self.settingsFile=open(settingsFileName,'r+')
		for eachline in self.settingsFile:
			lineInfo = self.settingsFile.readline()
			if (lineInfo[0]=="#"):
				pass
			else:
				[setting, value] = [x.lower().strip() for x in lineInfo.split(':',1)]




	def __init__(self):
		self.knownAccounts={}

		self.loadSettings()