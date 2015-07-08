A quickish walkthrough through how the little API engine works. 

[This is the master file.](https://github.com/jeremiahmarks/csvToolbox/blob/master/ISServer_master.py)
It is not a static link, so what I discuss here may not be the exact same, but it should probably follow
the same general methodology.

```python
import xmlrpclib
```

Our API uses xmlrpc, so we use a prebuilt library to work
with it easily.

```python
class ISServer:
```

In python classes are objects which can contain static or dynamic methods and values.
This class suffers from the misnomer of "Server" because from the endpoint that I use
it, it is "the server"

```python
    def __init__(self, infusionsoftapp, infusionsoftAPIKey):
        self.infusionsoftapp=infusionsoftapp
        self.infusionsoftAPIKey=infusionsoftAPIKey
        self.appurl = "https://" + self.infusionsoftapp + ".infusionsoft.com:443/api/xmlrpc"
        self.connection = xmlrpclib.ServerProxy(self.appurl)
```
In python you can define a method with the ```def``` keyword. Within this object (if you notice the 
indentation, I think that this makes sense to think of it this way) we define the method "__init__" which
requires two variables ```infusionsoftapp``` and ```infusionsoftAPIKey```.

In python, when building objects, ```self``` refers to self. So in the statement
```self.infusionsoftapp=infusionsoftapp``` we set the objects instance of the variable
```infusionsoftapp``` to the variable that was passed. (also named ```infusionsoftapp```. That
is probably bad.)

Pythons simple string building ability is used to build the URL for the applications API connection. 

The connection is then made using the xmlrpc library. That open connection is stored as an object
variable that anything in (or out of, for that matter) the object can use. 

```python
    def getMatchingRecords(self, tableName, criteria, desiredFields=None, orderedBy=None):
        """Search at table by criteria
        """
        return self.getAllRecords(tableName, searchCriteria=criteria, interestingData=desiredFields, orderedBy=orderedBy)
    def getTagCats(self):
        return self.getAllRecords("ContactGroupCategory")
    def getAllTags(self):
        return self.getAllRecords("ContactGroup")
    def getAllProductCats(self):
        return self.getAllRecords("ProductCategory")
    def getAllProducts(self):
        return self.getAllRecords("Product")
```
These are all different methods that go written at one time or another that re implement the getAllRecords
method. The getAllRecords methods could be called with the same data as most of these methods and will
provide the same interaction, but these may be easier to remember.  (With the tables at the end of this
file, though, I hope that they really are not.)

```python
    def getAllRecords(self, tableName, interestingData=None, searchCriteria=None, orderedBy=None):
        if interestingData is None:
            interestingData = tables[tableName]
        if searchCriteria is None:
            searchCriteria={}
        if orderedBy is None:
            orderedBy = interestingData[0]
        records = []
        p=0
        while True:
            listOfDicts = self.connection.DataService.query(self.infusionsoftAPIKey, tableName, 1000, p, searchCriteria, interestingData, orderedBy, True)
            for each in listOfDicts:
                thisRecord={}
                for eachbit in interestingData:   # this should be records.append(zip(interestingData, each)) perhaps
                    if not each.has_key(eachbit):   # TODO: research THIS
                        each[eachbit]=None
                    thisRecord[eachbit] = each[eachbit]
                records.append(thisRecord)
            if not(len(listOfDicts)==1000):
                break
            p+=1
        return records
```

* In python, you need to pass yourself to yourself in order to access yourself. Basically, when you are 
creating methods within an object, you need to pass the method a copy of itself so it knows who it is. 
I have a rough idea of why you need it.  You just need to always have self in the things that a method
within an object expects. 
* tableName is the name of the table that you are wanting to get records for. it will be a string, ie: 
```GroupAssign```. 'This is because the table names are used as keys to lists of columns.
* interestingData is a python list of table columns that you are interested in. ex:
```["Admin", "GroupId", "Id", "UserId"]```
* searchCriteria is a python dictionary of keys/pairs. if you were looking for GroupAssign Records where
```UserId``` is '1', it would look like this ```{"UserId": 1}```
* orderedBy is just the column name that you want the results ordered by.  If you want it reversed, you
can change the "True" to "False" at the end of the query line.
* Ideally, I wanted this object to be able to function easily. That is why the only thing that is needed
is the tablename, but you can add other things. The ```if``` statements basically set the defaults
if nothing is passed for those variables
* ```records = [] ``` in python a list is an ordered, mutable data structure. basically, if you put an
object into it you can go back and work with that object later on. A couple of words:
    * A NOTE: positional operators and slices do not modify the object. They only return the specified
    values from a list.
    * python uses a positional operator to access things positionally. for instance, in ```yourlist=['a','b','c','d']```
    you can access 'a' with ```yourlist[0]```, 'b' with ```yourlist[1]```, the last element with ```yourlist[-1]```
    * python uses the positional operator in conjunction with ':' to use the slice operator. 
        * if we wanted a list of all but the first operator, we can use ```yourlist[1:]```. this will return
        the list starting at the first (after the zeroth) variable all the way up to the end of the list.
        * if we wanted all but the last two values, we could use ```yourlist[:-2]```. This returns all
        but the last two items of the list.
        * if we wanted to trim the first and last objects in the list, we could use ```yourlist[1:-1]```
* ```p=0``` : the infusionsoft api paginates returns. The first values are on page zero, so that is 
where we start. 
* ```while True:
``` this basically is 'run until told to stop'
* ```python
listOfDicts = self.connection.DataService.query(self.infusionsoftAPIKey, tableName, 1000, p, searchCriteria, interestingData, orderedBy, True)
```
    * the variable name ```listOfDicts``` is a description of exactly what it is. A list (mutable, positional(did I really use that word, is that right?) data structure)
    where the objects at each location are dicts (an unordered key->value data structure that I probably use too much.)
    * ```self.connection.DataService.query()``` basically, a query to the data service.
    * ```python
        (self.infusionsoftAPIKey, tableName, 1000, p, searchCriteria, interestingData, orderedBy, True)
    ```
        * Authenticate
        * table desired data is on
        * number of records to return (1000 is the max)
        * what page to return.
            * note I am not sure how that would work with liveupdating at a peak time.
        * searchCriteria in {Key: Value} form
        * a list of the columns that you want back. 
        * which column to order the results by
        * whether the results should be in ascending order or not. 
*
```python
for each in listOfDicts:
    thisRecord={}
    for eachbit in interestingData:   # this should be records.append(zip(interestingData, each)) perhaps
        if not each.has_key(eachbit):   # TODO: research THIS
            each[eachbit]=None
        thisRecord[eachbit] = each[eachbit]
    records.append(thisRecord)
```
* basically: iteratre through the list of dicts. For each record that is in the list, we create
a new, empty dictionary named ```thisRecord``` to manages the values. We then iterate through the 
list of columns we requested. If the value exists, we set that value within ```thisRecord```.
* a core tennant of csv.DictWriter is that each row have every column. That is why when the interestingData
is not in the returned record, we add a value of ```None```
* finally, we append the completed ```thisRecord``` to the list that we completed near step 3.
* ```python
            if not(len(listOfDicts)==1000):
                break
            p+=1
```
We assume that if there were not 1000 records returned, there must not be another page. If there were 1000
records returned, we will loop through automagically. By looping, we increment the page counter, so we will get the 
next page. 
* ```python
        return records
```
This is what we return.

--------------------------------
Whew, time for a breather. 

--------------------------
Welcomeback!


```python
    def createNewRecord(self, table, recordvalues):
        return self.connection.DataService.add(self.infusionsoftAPIKey, table, recordvalues)
```
This method accepts a tablename as a string and a key-> value map (dictionary    {}  ) of the column
data. it will then create the record. 

```python
    def updateRecord(self, tableName, recordId, updateValues):
        return self.connection.DataService.update(self.infusionsoftAPIKey, tableName, recordId, updateValues)
```
Accepts the tablename, the integer that is the id of the record, and a dict of values to update.

```python
    def deleteRecordsOnTable(self, tableName):
        allTableIds=self.getAllRecords(tableName, ["Id"])
        for eachid in allTableIds:
            try:
                self.connection.DataService.delete(tablename, eachid)
            except:
                print "Cannot Delete " + str(eachid)
```
If you are playing, you are going to need it.  Sadly you cannot delete records from every table.  you can 
iterate through the keys of the tables data structure that is in the file.
```python
    def getCount(self, tableName, query):
        return self.connection.DataService.count(self.infusionsoftAPIKey, tableName, query)
```
Basically, just get the number of records that meet the dict query.  if will tell you how many records you
will need to be ready to get.


with the included ```tables``` variable, one can easily do somthing like this
```python
import csv
import sys
sys.path.append('/home/jlmarks/csvToolbox/')
import ISServer_master as ISServer
appname="if188"
apikey='c5029ec5d3188d90cbb3a4fcd5c17674'
thisserver = ISServer.ISServer(appname, apikey)
for eachkey in ISServer.tables.keys():
    with open(eachkey,'wb') as outfile:
        thiswriter=csv.DictWriter(outfile, ISServer.tables[eachkey])
        thiswriter.writeheader()
        theserecords = thisserver.getAllRecords(eachkey)
        thiswriter.writerows(theserecords)
```
which will pull all of the data that you can through the api into home files in the python installs cwd
you may need to look for it the first time or two.


All of that said, I am out.