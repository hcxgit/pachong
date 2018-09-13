#coding:utf-8
import urllib
import urllib2

url = 'https://www.zhihu.com/#signin'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
values = {'username': 'cqc', 'password': 'XXXX'}
headers = {'User-Agent': user_agent, 'Referer': 'https://www.zhihu.com/'}
data = urllib.urlencode(values)
request = urllib2.Request(url, data, headers)
try:
	response = urllib2.urlopen(request)
	page = response.read()
except urllib2.HTTPError, e:
	print e.code
except urllib2.URLError, e:
	print e.reason
else:
	print 'ok'

