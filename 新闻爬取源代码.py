# -*-coding:utf-8-*-

from bs4 import BeautifulSoup#导入bs4模块，用BeautifulSoup分析网页
import requests#导入requests模块，用于向服务器发送请求
import os#导入os模块，用于文件处理(未系统学习，参照慎用)
import re#导入re模块，实现正则表达式的使用
import webbrowser#导入webbrowser模块，用于使用用户的默认浏览器打开网页
import time#导入time模块，用于实现程序延迟
import sys#导入sys模块，用于实现程序重启(重启程序楼主在网上找的，也不知道具体用法)

def url_open(url):#使用定义函数
	headers = {}#创建Headers,用于模拟浏览器发送请求
	headers["Accept"] = "image/webp,image/apng,image/*,*/*;q=0.8"
	headers["Accept-Encoding"] = "gzip, deflate, br"
	headers["Accept-Language"] = "zh-CN,zh;q=0.9"
	headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
	response = requests.get(url, headers=headers)#用requests模块下的get命令，请求服务器，同时发送headers以模拟浏览器
	response.encoding = "utf-8"#将从服务器获取到的内容转化为utf-8编码

	html = response.text#使用text命令将二进制编码转换为文本

	return html#函数输出命令，输出html

def restart_program():
	print("restart program")
	python = sys.executable #获取当前执行python 
	os.execl(python, python, *sys.argv)  #执行命令

print("本程序使用爬虫爬取，新闻内容来自澎湃新闻。\n")
time.sleep(1)
print("本程序读取新闻时会爬取来源，如需转载请注明来源！\n")
time.sleep(1)
print("感谢使用本程序，本程序由北斗工作室开发，如需转载或引用，请标注来源！\n\n\n")
time.sleep(2)

print("以下是爬取的热点前20新闻：\n")
time.sleep(1)

base_url = "https://www.thepaper.cn/"#设定主链接变量

web = url_open(base_url)#引用自己编写的函数模块，获取网页html

soup = BeautifulSoup(web, features='lxml')#使用bs4中的BeautifulSoup解析网页，引用lxml格式的解析器
all_h2 = soup.find_all('h2')#找到所有带h2标签的html语言，即澎湃新闻官网的大新闻标题

all_title = []#创建一个新的list
for each_h2 in all_h2:#使用for in循环，逐个去除每一个h2标签下的语言，获得标题
	title = each_h2.get_text()#对每一个标签用Get_text命令获取文本
	all_title.append(title)#将获取到的标题添加到All_title中

price = [x.strip() for x in all_title if x.strip() != '']#引用自网友的命令，去除all_title里的所有换行符

links = re.findall(r"newsDetail_forward_\d{7}", str(all_h2))#使用正则表达式获取所有标题对应的链接，并返回一个list，注意！正则表达式要求一个str格式！

for m in range(20):#创建一个20次的循环，输出20条新闻
	this_title = price[m]#输出price(去除过换行符后的list)的第m项
	this_link = links[m]#输出links里的第m项
	n = m + 1#创建n,用于标注序号，因为range是从0开始，所以m+1表示序号
	print (n, this_title + "\n")#输出新闻标题 + 链接
	time.sleep(1)

choice = input("请输入您感兴趣的新闻序号：")#请求输入，获得用户所需新闻
num = int(choice) - 1#将输入的str转化为int并进行-1使之转化为list的索引序号
news_link = links[num]#用输入的结果生成的索引，在links这个list里索引对应的网址
news_url = base_url + news_link#将索引到的网址与澎湃官网的base url合并，生成完整的地址

time.sleep(1)
print("1 使用默认浏览器访问新闻网页\n")
time.sleep(1)
print("2 爬取新闻内容并展示\n\n")#打印出选项，让用户选择进行新闻访问/直接爬取新闻
time.sleep(1)

choice2 = input("请输入数字选择：")#使用input函数获取用户选择
a = int(choice2)#将获得的选择转化为int形式，便于使用if else进行比较

if a == 1:#引入if条件判断，判断用户选择是多少
	webbrowser.open(news_url)#使用webbrowser模块，唤起默认浏览器，打开页面
elif a == 2:#再用elif判断
	html2 = url_open(news_url)#用自己定义的url_open函数获得news_url的页面
	soup2 = BeautifulSoup(html2, features='lxml')#使用BeautifulSoup解析新闻页面
	title2 = soup2.find('h1')#找到h1标题
	laiyuan = soup2.find('div', {"class":"news_about"})#找到class标签为news_about的div标签
	time2 = laiyuan.find_all('p')#找到div标签下的p标签
	v = []#创建一个空的list——v
	for z in time2:#for in 函数输出
		u = z.get_text()#用get_text()命令获得文本
		v.append(u)#将获得的文本添加进v这个list中
	price2 = [y.strip() for y in v if y.strip() != '']#引用自网友的命令，去除all_title里的所有换行符
	news_text = soup2.find('div', {"class":"news_txt"})#找到网页所有的div标签下class = news_txt的标签
	news_list_dealt = news_text.get_text()#使用get_text命令获得新闻正文
	news_list = list(news_list_dealt)#将新闻正文转化为list
	for i in range(29):#循环29次，用于去除澎湃下载下来自带的广告(字符正好是29个)
		news_list.pop()#使用pop指令去除正文list中的最后一项
	news_str = "".join(news_list)#引自网友，将list合并为string
	print ("\n\n标题：" + title2.get_text() + "\n\n来源&时间：" + price2[0] + "\n" + price2[1] + "\n\n正文：" + news_str)#输出标题，来源，正文
else:
	print("请按要求输入文本！")#使用else判断出用户输入其他字符
	time.sleep(1)
	print("程序即将重启！请重新选择！")#告诉用户即将重启
	restart_program()#通过重启模块实现重新选择，偷懒。。。。

print ("\n请选择:\n")
time.sleep(1)
print("1 选择另一条新闻\n")
time.sleep(1)
print("2 退出程序\n")
time.sleep(1)
print("3 关于\n")
time.sleep(1)
print("4 在默认浏览器里浏览该新闻\n")

choice3 = input("\n请输入数字选项：")#获得用户选择
b = int(choice3)#将用户的结果转化为整数形式！很重要！input获得的结果是string

if b == 1:#继续判断
	restart_program()#通过重启程序让用户选择另一条新闻，又偷懒。。
elif b == 2:
	print("感谢使用本程序，欢迎下次使用！")
	time.sleep(2)#使用time函数，实现程序延迟2秒
	print("再见，本程序将在3秒后自动退出！")
	count = 0#从本行到第98行，实现倒计时并倒数
	b = 3
	while (int(count) < int(b)):
		ncount = int(b) - int(count) 
		print (ncount)
		time.sleep(1)
		count += 1 
elif b == 3:
	print("本程序由北斗工作室开发！\n")
	time.sleep(1)#使用time函数，实现程序延迟1秒
	print("Triones Studio .Inc\n")
	time.sleep(1)#使用time函数，实现程序延迟1秒
	print("如需搬运，请标注来源！谢谢！\n")
	time.sleep(1)#使用time函数，实现程序延迟1秒
	print("本程序作者学习来自莫烦python,主页：https://morvanzhou.github.io/")
	time.sleep(1)#使用time函数，实现程序延迟1秒
	print("本程序引用的重启函数，来自博客园网站某博主，感谢！")
	time.sleep(1)#使用time函数，实现程序延迟1秒
	print("程序即将重启！请重新选择！")
	restart_program()#通过重启模块实现重新选择，偷懒。。。。
elif b == 4:
	webbrowser.open(news_url)#使用webbrowser模块，唤起默认浏览器，打开页面
	print ("\n请选择:\n")
	time.sleep(1)
	print("1 选择另一条新闻\n")
	time.sleep(1)
	print("2 退出程序\n")
	time.sleep(1)
	print("3 关于\n")
	choice3 = input("\n请输入数字选项：")#获得用户选择
	c = int(choice3)#将用户的结果转化为整数形式！很重要！input获得的结果是string

	if c == 1:#继续判断
		restart_program()#通过重启程序让用户选择另一条新闻，又偷懒。。
	elif c == 2:
		print("感谢使用本程序，欢迎下次使用！")
		time.sleep(2)#使用time函数，实现程序延迟2秒
		print("再见，本程序将在3秒后自动退出！")
		count = 0#从本行到第98行，实现倒计时并倒数
		c = 3
		while (int(count) < int(c)):
			ncount = int(c) - int(count) 
			print (ncount)
			time.sleep(1)
			count += 1 
	elif c == 3:
		print("本程序由北斗工作室开发！\n")
		time.sleep(1)#使用time函数，实现程序延迟1秒
		print("Triones Studio .Inc\n")
		time.sleep(1)#使用time函数，实现程序延迟1秒
		print("如需搬运，请标注来源！谢谢！\n")
		time.sleep(1)#使用time函数，实现程序延迟1秒
		print("本程序作者学习来自莫烦python,主页：https://morvanzhou.github.io/")
		time.sleep(1)#使用time函数，实现程序延迟1秒
		print("本程序引用的重启函数，来自博客园网站某博主，感谢！")
		time.sleep(1)#使用time函数，实现程序延迟1秒
		print("程序即将重启！请重新选择！")
		restart_program()#通过重启模块实现重新选择，偷懒。。。。
	else:
		print("请输入数字1/2/3！谢谢！")
		time.sleep(1)
		print("程序即将重启！请重新选择！")
		restart_program()#通过重启模块实现重新选择，偷懒。。。。
else:
	print("请输入数字1/2/3！谢谢！")
	time.sleep(1)
	print("程序即将重启！请重新选择！")
	restart_program()#通过重启模块实现重新选择，偷懒。。。。