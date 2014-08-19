import urllib2
import BeautifulSoup
from urlparse import urlparse
import socket
import nltk



def getUerlfromHref(url , new_url):
	parsed_uri = urlparse( url )
	domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

	if new_url.startswith('/') :
		return domain + new_url[1:]
	elif new_url.startswith('#'):
		return domain
	elif new_url.startswith('./'):
		return url + new_url[1:]
	elif 'http://shilloi.iitg.ernet.in/~ace/intranet/forums//memberlist.php' in new_url :
		return str('http://shilloi.iitg.ernet.in/~ace/intranet/forums//memberlist.php')
	else :
		return new_url


def isAfile(url):
	if url.endswith('.iso') or url.endswith('.chm') or url.endswith('.jpg') or url.endswith('.mobi') or url.endswith('.epub') or url.endswith('.deb') or url.endswith('.zip') or url.endswith('JPG') or url.endswith('.mov') or url.endswith('.ttf') or url.endswith('.psd') or url.endswith('.TTF') or url.endswith('.atn') or url.endswith('.NEF') or url.endswith('.swf') or url.endswith('.fla') or url.endswith('.swf') or url.endswith('.aif') or url.endswith('.wav') or url.endswith('.mp3') or url.endswith('.mp4') or url.endswith('.ai') or url.endswith('wmv') or url.endswith('f4v') or url.endswith('.tar') or url.endswith('.bz2') or url.endswith('.MD5') or url.endswith('.png') or url.endswith('.dng') or url.endswith('.flv') or url.endswith('.avi') or url.endswith('.Zip') or url.endswith('dir=') or url.endswith(".rar") or url.endswith(".ISO") or url.endswith(".ova")  or url.endswith(".djvu")  or url.endswith(".nrg") or url.endswith(".tgz") or url.endswith(".gz") or ' ' in url or '@' in url or '#' in url or 'repo.cse.iitg.ernet.in' in url or '.iitg.ernet.in/news/' in url or 'csea.iitg.ernet.in' in url or 'shilloi.iitg.ernet.in/~ace/intranet/forums' in url:
		return True
	return False




url = "http://202.141.80.14"

visited_url = []
urlTovist = []
urlTovist.append(url)

proxy_handler = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)
# url = str(urlTovist.pop(0))
# print url
# page = urllib.urlopen(url)
# print page.read()

while len(urlTovist) > 0:
	try :
		url = str(urlTovist.pop(0))
		print url
		visited_url.append(url)
		page = urllib2.urlopen(url , timeout=1).read()
		bs = BeautifulSoup.BeautifulSoup(page)
		aTAGs = bs.findAll('a' , href=True)
		for atag in aTAGs:
			new_url = atag.get('href')
			new_url = getUerlfromHref(url , new_url)
			if (new_url not in visited_url) and (new_url not in urlTovist) and ( '.iitg.ernet.in' in new_url ) and ('facebook.com' not in new_url) and ('mailto:' not in new_url) and "http://repo.cse.iitg.ernet.in/index.php?archive=true" not in new_url and 'http://www.iitg.ernet.in/civil/saswati-webpage/frontpage.htm' not in new_url and 'activities/all-events' not in new_url and 'http://www.iitg.ernet.in/DAE-HEP2014/public/accommodation.php/general-information.php/general-information.php/general-information.php' not in new_url and (not (new_url.endswith('.pdf') or new_url.endswith('.mp4') or new_url.endswith('.docx') or new_url.endswith('.ppt') or new_url.endswith('.PDF') or new_url.endswith(".doc") or new_url.endswith(".exe") or isAfile(new_url))):
				urlTovist.append(new_url) 
		print 'ok'
		print bs.findAll('title')[0].text
		print nltk.clean_html(page)
		print len(urlTovist) , len(visited_url)


	except ValueError : 
		print 'value error'
	except urllib2.URLError :
		print 'url error'
	except  socket.timeout:
		print 'timeout error'
	# except:
	# 	pass
