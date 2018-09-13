'''
抓取天气
'''
import requests
import bs4
def get_html(url):
	'''
	封装请求
	:param url:http://www.weather.com.cn/weather1d/101120201.shtml
	:return:
	'''
	headers={
		'Content-type':'text/html',
		'Accept - Encoding': 'gzip, deflate, sdch',
		'Accept - Language': 'zh - CN, zh;q = 0.8',
		'Connection': 'keep - alive',
		'User - Agent': 'Mozilla / 5.0(WindowsNT10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 55.0.2883.87Safari / 537.36',
	}
	try:
		htmlcontent = requests.get(url,headers=headers,timeout=30)
		htmlcontent.raise_for_status()
		htmlcontent.encoding = 'utf-8'
		return htmlcontent.text
	except:
		return "请求失败"
def get_content(url):
	'''抓取页面天气数据'''
	weather_list = []
	html = get_html(url)
	soup = bs4.BeautifulSoup(html,'lxml')#lxml解析网页
	content_ul = soup.find('div',class_='t').find('ul',class_='clearfix').find_all('li')
	# print(content_ul)
	for content in content_ul:
		try:
			weather = {}
			weather['day'] = content.find('h1').text
			weather['temputer'] = content.find('p',class_='tem').span.text + content.find('p',class_='tem').em.text
			weather_list.append(weather)
		except:
			print()
	print(weather_list)
if __name__ == '__main__':
	url = 'http://www.weather.com.cn/weather1d/101120201.shtml'
	get_content(url)