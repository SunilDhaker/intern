import urllib
import BeautifulSoup
from elasticsearch import Elasticsearch


url = "http://www.aises.nic.in/schooldirectoryforviewonly?pu=true"
es = Elasticsearch()
page = urllib.urlopen(url)
soup = BeautifulSoup(page)
count = 1247024
stateList = {}
options = soup.findAll('select')[0].findAll('option')
print('entering in stateList')
for  i in range(33 , len(options)) :
	option = options[i]
	if option['value'] != '-1':
		print('currunt state ' , option.text)
		stateList[str(option['value'])] = option.text
		distList = {}
		distData = urllib.urlopen("http://www.aises.nic.in/populatedistrictsinlisting?stateCode=" + str(option['value']) )
		soupofdist = BeautifulSoup(distData)
		distoptions =  soupofdist.findAll('select')[0].findAll('option')
		for distoption in distoptions:
			print(count)
			if distoption['value'] != '-1':
				print('current dist ' , distoption.text)
				distList[distoption['value']] = distoption.text
				formData = 'cv=1&pu=true&stateCode=' + option['value'] + '&districtCode=' + distoption['value'] +'&Schooltype=2&blockCode=0&villageCode=0&townCode=0&wardCode=0&schoolCategory=0&search=Search'
				school_list =  BeautifulSoup(urllib.urlopen("http://www.aises.nic.in/schooldirectoryforviewonly?pu=true" , formData))
				for tr in school_list.findAll('tr'):
					try:
						if tr['class'][0] == 'gradeA':
							count = count + 1
							tds = tr.findAll('td')
							schoolType = tds[1].text
							schoolName = tds[2].text
							schoolAdd = tds[3].text
							schoolTown = tds[4].text
							schoolWard = tds[5].text
							doc = { 'name':schoolName , 'type' :schoolType , 'address': schoolAdd , 'town' : schoolTown , 'ward': schoolWard , 'area':'urban' , 'dist' : distoption.text , 'state' : option.text }
							es.index( index = 'school' , doc_type = 'mhrd' , id=count , body = doc )
					except Exception as e:
						pass
				distList[distoption['value']] = distoption.text
				formData = 'cv=1&pu=true&stateCode=' + option['value'] + '&districtCode=' + distoption['value'] +'&Schooltype=1&blockCode=0&villageCode=0&townCode=0&wardCode=0&schoolCategory=0&search=Search'
				school_list =  BeautifulSoup(urllib.urlopen("http://www.aises.nic.in/schooldirectoryforviewonly?pu=true" , formData))
				for tr in school_list.findAll('tr'):
					try:
						if tr['class'][0] == 'gradeA':
							count = count + 1
							tds = tr.findAll('td')
							schoolType = tds[1].text
							schoolName = tds[2].text
							schoolAdd = tds[3].text
							schoolTown = tds[4].text
							schoolWard = tds[5].text
							doc = { 'name':schoolName , 'type' :schoolType , 'address': schoolAdd , 'town' : schoolTown , 'ward': schoolWard ,'area':'rural' , 'dist' : distoption.text , 'state' : option.text }
							es.index( index = 'school' , doc_type = 'mhrd' , id=count , body = doc )
					except :
						pass

print(count)