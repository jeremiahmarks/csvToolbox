import os  
import csv  
import xmlrpclib  
import base64  
  
infusionsoftapp='ap187'  
apikey='b7311111523dc2af812ac501070baf65'  
  
pathtocsv='C:\\Users\\shane.marcotte\\Desktop\\DATAMIGRATION\\Completed\\fileimport.csv'  
pathtofilefolder='C:\\Users\\shane.marcotte\\Desktop\\DATAMIGRATION\\Completed\\ap187test' # Note:  this needs to end without a path seperator.  
  
appurl = "https://" + infusionsoftapp + ".infusionsoft.com:443/api/xmlrpc"  
connection = xmlrpclib.ServerProxy(appurl)  
  
  
  
  
with open(pathtocsv, 'rb') as infile:  
     thisreader = csv.DictReader(infile)  
     for eachrow in thisreader:  
          if eachrow['ContactId'] is not "#N/A":  
                contactid = eachrow['ContactId']  
                pathtofile = os.path.join(pathtofilefolder, eachrow['Filename'])
                try:
	                connection.FileService.uploadFile(apikey, contactid, eachrow['Filename'], base64.b64encode(open(pathtofile, 'rb').read()))
	            except Exception, e:
	            	print e, Exception, '\n\n',eachrow['Filename'], '\n\n'
