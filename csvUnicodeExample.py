import csv
pathtofile="products.csv"


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


with csv.DictReader(open(pathtofile)) as thiscsvreader:
    fileholder=[] # just a place to put open files
    readers={} # a place to store in use csv.DictReaders
    writers={} # a place to store writers

    for eachheading in thiscsvreader.fieldnames:
        thisfile=open(eachheading + ".csv", 'wb')
        thisfilesvals=['rownumber', eachheading]
        thiswriter=csv.DictWriter(thisfile, thisfilesvals)
