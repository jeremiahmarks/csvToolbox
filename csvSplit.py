import urllib2
import filecmp
import os

LOCALFILENAME="005HistoryExport.csv"
NUMBEROFLOCALFILES=0
LOCALFILEPATH="C:\Users\jeremiah.marks\Desktop\Portable Python 2.7.6.1"

def getRemoteFile():
	global LOCALFILENAME
	global LOCALFILEPATH
	print """Please input the location of the remote file.
	Example:  http://jlmarks.org/randomname/Fielding.csv
	"""
	floc=raw_input("Please provide location of file:\t").strip()
	cfile= urllib2.urlopen(str(floc))
	LOCALFILENAME = floc[floc.rindex('/')+1:]
	outputFile = open(os.path.abspath(os.path.join(LOCALFILEPATH, LOCALFILENAME)),'wb')
	outputFile.write(cfile.read())
	outputFile.close()

def processFile():
	global LOCALFILENAME
	global NUMBEROFLOCALFILES
	numberOfLines=sum(1 for line in open(LOCALFILENAME)) - 1
	print """
	There are %s lines in this file.  How many files would you like this file broken into?
	""" %(str(numberOfLines))
	NUMBEROFLOCALFILES = int(raw_input())
	linesPerNormalFile=numberOfLines/NUMBEROFLOCALFILES
	linesPerFirstFile= linesPerNormalFile+numberOfLines%NUMBEROFLOCALFILES
	localFile=open(os.path.abspath(os.path.join(LOCALFILEPATH, LOCALFILENAME)))
	firstLine=localFile.readline()
	for x in range(NUMBEROFLOCALFILES):
		smallerFileName="%03d" % x + LOCALFILENAME
		smallerFile=open(os.path.abspath(os.path.join(LOCALFILEPATH, smallerFileName)),'wb')
		smallerFile.write(firstLine)
		if (x == 0):
			for y in range(linesPerFirstFile):
				smallerFile.write(localFile.readline())
		else:
			for y in range(linesPerNormalFile):
				smallerFile.write(localFile.readline())
		smallerFile.close()
	localFile.close()

def recombineAndDiff():
	global LOCALFILENAME
	global NUMBEROFLOCALFILES
	recombinedFileName="recombinedFile.csv"
	recombinedFile=open(os.path.abspath(os.path.join(LOCALFILEPATH, recombinedFileName)),'wb')
	for x in range(NUMBEROFLOCALFILES):
		smallerFileName="%03d" % x + LOCALFILENAME
		smallerFile=open(os.path.abspath(os.path.join(LOCALFILEPATH, smallerFileName)))
		if (x==0):
			recombinedFile.write(smallerFile.read())
		else:
			firstline=smallerFile.readline()
			recombinedFile.write(smallerFile.read())
		smallerFile.close()
	recombinedFile.close()
	if filecmp.cmp(os.path.abspath(os.path.join(LOCALFILEPATH, LOCALFILENAME)),os.path.abspath(os.path.join(LOCALFILEPATH, recombinedFileName))):
		print """
		The file has been sucessfully broken into several smaller files and then rebuilt from
		those smaller files. The rebuilt file is the same as the original file, so data integrity
		appears intact.
		"""
	else:
		print """
		The file has been broken into several smaller files and then rebuilt from those
		smaller files.  The rebuilt file does not appear to be the same file as the original
		so data integrity is in question
		"""


if __name__ == '__main__':
	downloaded=raw_input("Is file downloaded and in current directory currently? \n\n (y or n): ")
	if (downloaded=='y' or downloaded=='Y'):
		LOCALFILENAME=raw_input("please enter file name")
	else:
		getRemoteFile()
	processFile()
	recombineAndDiff()