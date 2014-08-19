import urllib
from bs4 import BeautifulSoup
import urlparse
import mechanize
from lxml import etree
import re
from elasticsearch import Elasticsearch

url = "http://www.engineering.careers360.com/colleges/list-of-engineering-colleges-in-India?term_node_tid_depth=All&page="
br = mechanize.Browser()
count = 0
for pagecount in range(0,500):
	urlToVisit = url + str(pagecount)
	page = urllib.urlopen(urlToVisit)
	soup = BeautifulSoup(page)
	es = Elasticsearch()
	# html = etree.HTMLParser()
	# tree = etree.parse(page, html)
	# print tree.xpath("id('content')/x:div/x:div/x:div[2]/x:div[3]/x:div[2]/x:div/x:span/x:div/x:div[2]/x:div[1]/x:a")
#	print soup
	for x in soup.findAll('div'):
		try:
#			print x
	#		print "hit"
# 			title = ''
# 			if str(x['class'][0])=="title":
# 				if x.a:
# 					title = x.a.text.encode('utf-8').strip()
# 					print  x.a.text.encode('utf-8').strip() 
# 					#urllib.urlretrieve("http://www.gunnerkrigg.com//comics/00000001.jpg", "00000001.jpg")
# 			if str(x['class'][0])=="image-con":
# 				 print title
# #				 urllib.urlretrieve(x.img['src'] ,title+".jpg")
# 				 #print x.img['src']
			if str(x['class'][0]) == 'inner-div':
				image_url =  x.findAll('div')[0].find('img')['src']
				name_college = x.findAll('div')[1].findAll('div')[0].a.text.encode('utf-8').strip()
				location = x.findAll('div')[1].findAll('div')[1].text.replace('Location:' , "").encode('utf-8').strip()
				print name_college , image_url , location

				doc = { 'college_name' : name_college , 'image_url' : image_url , 'location':location }
				es.index( index = 'colleges' , doc_type = 'engineering' , body=doc )
				count = count + 1
		except KeyError :
#			print "execption"
			pass

print count
