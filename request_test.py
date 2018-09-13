'''
requests库   示例
'''
import requests
# from requests.packages import urllib3
from requests.exceptions import ReadTimeout
'''基本用法'''
response = requests.get("http://baidu.com",auth={('user','123')})#有的网站需要认证  auth  传入用户和密码
print(response.text)         #输出内容
print(response.status_code)  #输出状态码  200为成功  404   505 。。。。。。
# '''带参数用法'''   #这里用的是get方法
data = {
	'name':'germey',
	'age':'22'
}
response1 = requests.get('http://httpbin.org/get',params=data)
print(response1.text)

#h获取 图片 视频啥的
response3 = requests.get('https://github.com/favicon.ico')
with open('favicon.ico','wb') as f:
	f.write(response3.content)   #获取图片视频啥的可以用 content  方法
	f.close()

# #证书验证
#
# urllib3.disable_warnings()#不弹出警告
# response4 = requests.get('https://12306.cn',verify=False)#不验证
# print(response4.status_code)

#代理设置
proxies ={
	'http:':'http://127.0.0.1:9743',#有时用socks代理  则values为'socks://127.0.0.1:9743'
	'https:':'https://127.0.0.1:9743',
}
response5 = requests.get('http://www.taobao.com',proxies=proxies)
print(response5.status_code)
#timeout  超时设置
try:
	response6 = requests.get("http://baidu.com",timeout=1)
	print(response6.status_code)
except ReadTimeout:
	print('Timeout')
