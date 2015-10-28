
import csv
from lxml import etree
xmlp='c:\\users\\jeremiah.marks\\downloads\\content.xml'
apples = etree.parse(xmlp, etree.XMLParser(recover=True, remove_blank_text=True))
apples.docinfo
apples.xmlschema
apples
pp=apples.getiterator()
k=pp.next()
k.values()
apples.getpath(k)
pp=apples.getiterator('contact')
op=pp.next()
op.values()
op.attrib
op=pp.next()
op.attrib
