# -*- coding: utf-8 -*-
import os
import re
import json
import time
import string
import random
import urllib
import hashlib
import requests
import schedule
import datetime
from urllib.parse import quote
from pyserverchan import pyserver

# *********************************************************
# 函数说明：青云客机器人的简单对话
# 函数输入：想要的对话（utf-8编码的）
# 函数输出：AI对话的结果
# *********************************************************
def qingyunkeAI(msg):
	url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(urllib.parse.quote(msg))
	html = requests.get(url)
	return html.json()["content"]
# msg = '武汉的天气怎么样'
# print("原话>>", msg)
# res = qingyunkeAI(msg)
# print("青云客>>", res)

# *********************************************************
# 函数说明：腾讯AI的简单对话
# 函数输入：想要的对话（utf-8编码的）
# 函数输出：AI对话的结果
# 备注:	腾讯闲聊机器人的凭证如下：
# 		App_ID: 123456
# 		App_Key: 123456
# *********************************************************
def tencentAI(msg):
	APPID = "123456"	#替换成自己申请的ID
	APPKEY = "123456"	#替换成自己申请的KEY
	url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
	params = {
		"app_id": APPID,
		"time_stamp": str(int(time.time())),
		"nonce_str": "".join(random.choice(string.ascii_letters + string.digits) for x in range(16)),
		"session": "10000".encode("utf-8"),
		"question": msg.encode("utf-8")
	}
	sign_before = ""
	for key in sorted(params):
		# 键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8。quote默认大写。
		sign_before += "{}={}&".format(key, urllib.parse.quote(params[key], safe=""))
	# 将应用密钥以app_key为键名，拼接到字符串sign_before末尾
	sign_before += "app_key={}".format(APPKEY)
	# 对字符串sign_before进行MD5运算，得到接口请求签名
	sign = hashlib.md5(sign_before.encode("UTF-8")).hexdigest().upper()
	params["sign"] = sign
	# print(params)
	html = requests.post(url, data=params).json()
	return html["data"]["answer"]
# msg= "讲一个笑话"
# print("原话>>", msg)
# res = tencentAI(msg)
# print("腾讯>>", res)

# *********************************************************
# 函数说明：获取一言接口的数据，并存储到全局的字符串OneWord中
# 函数输入：无
# 函数输出：True/False
# *********************************************************
def getOneWord():
	# 1. 请求一言的接口
	url = "https://v1.hitokoto.cn/"
	response = requests.get(url)
	# 2. 获取响应数据，并解析JSON，转化为python字典
	result = response.json()
	# 3. 打印结果中的"hitokoto"（想要的句子）
	print(result["hitokoto"])	# Json解析

	if response.status_code == 200 :
		return result["hitokoto"]
	else :
		return ""
# getOneWord()		# 测试获取一言数据

# *********************************************************
# 函数说明：将一言数据发送到Server酱，即微信的提醒
# 函数输入：无
# 函数输出：无
# *********************************************************
def sendOneWord():
	# 1. 获取sckey，具体请见：http://sc.ftqq.com/3.version
	sckeyDC = "XXX"
	sckeyLL = "XXX"
	# 2. 拼接url并且发送请求，text为推送的title,desp为推送的描述
	OneWord = getOneWord()
	# print(OneWord)

	if(OneWord == ""):
		print(" 不好啦，服务器疯了： 未能正确获取一言的数据")
		requests.get("https://sc.ftqq.com/%s.send?text=不好啦，服务器崩了！&desp=未能正确获取一言的数据"%sckeyLL)
		requests.get("https://sc.ftqq.com/%s.send?text=不好啦，服务器崩了！&desp=未能正确获取一言的数据"%sckeyDC)
	else:
		url = "https://sc.ftqq.com/%s.send?text=程序的测试&desp=%s" % (sckeyLL, OneWord)
		requests.get(url)
		url = "https://sc.ftqq.com/%s.send?text=程序的测试&desp=%s" % (sckeyDC, OneWord)
		requests.get(url)
# sendOneWord()		# 测试发送到Server酱




# *********************************************************
# 函数说明：把获取的结果保存到md文件中，方便发送
# 函数输入：无
# 函数输出：全部内容都在README.md文件中
# *********************************************************
def all2md():
	with open("README.md", mode='w', encoding='utf-8') as f:	# 'w'是写模式，会清空内容
		f.write("# 知心一言\n")
		f.write("  " + getOneWord() + "\n\n")
	f.close()

	msg = "武汉的天气怎么样"
	print("原话>>", msg)
	res = qingyunkeAI(msg)
	print("青云客>>", res)
	with open("README.md", mode='a', encoding='utf-8') as f:	# 'a'是追加模式
		f.write("# 最近天气\n")
		f.write("  " + re.sub('{br}', '\n  ', res) + "\n\n")
	f.close()


	msg = "讲一个笑话"
	print("原话>>", msg)
	res = tencentAI(msg)
	print("腾讯>>", res)

	with open("README.md", mode='a', encoding='utf-8') as f:	# 'a'是追加模式
		f.write("# 每日笑话\n")
		f.write("  " + res + "\n\n")
	f.close()

	sckeyDC = "XXX"
	sckeyLL = "XXX"

	user_URL = 'https://sc.ftqq.com/' + sckeyLL + '.send'
	svc = pyserver.ServerChan(user_URL)
	svc.output_to_weixin_markdown("README.md", title='豆豆眼儿早安呀╰(*°▽°*)╯')

	user_URL = 'https://sc.ftqq.com/' + sckeyDC + '.send'
	svc = pyserver.ServerChan(user_URL)
	# svc.output_to_weixin("ATestMessage.")
	# svc.output_to_weixin_picture("http://sc.ftqq.com/static/image/bottom_logo.png")
	svc.output_to_weixin_markdown("README.md", title='豆豆儿早安呀╰(*°▽°*)╯')

# *********************************************************
# 函数说明：定时执行任务（schedule模块）
# 函数输入：无
# 函数输出：无
# 函数说明：schedule模块只能用于轻量的任务调度，务必保持执行的
# 		   小于
# *********************************************************
if __name__ == "__main__":
	print(" main ")
	# schedule.every(1).minutes.do(all2md)
	# schedule.every().hour.do(all2md)
	# schedule.every().day.at("07:30").do(all2md)
	# schedule.every(5).to(10).days.do(all2md)
	# schedule.every().monday.do(all2md)
	# schedule.every().wednesday.at("13:15").do(all2md)
	
	schedule.every().day.at("07:30").do(all2md)
	while True:
		schedule.run_pending()
		time.sleep(1)
