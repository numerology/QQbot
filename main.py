# -*- coding: utf-8 -*-
__author__ = 'Nilk'

from qqbot import QQBotSlot as qqbotslot, RunBot
import csv
import tweepy
import datetime
import os
import json
import urllib2
import sys
import re as regex
import time
from bs4 import BeautifulSoup as BS

reload(sys)
sys.setdefaultencoding('utf-8')

CONSUMER_KEY = 'uWb94m6mwDnHOix6YAfMQ1ESt'
CONSUMER_SECRET = 'AHOrZYDUvskktLFIQRvXxnN7hDxtkaW8PZQsg1AatQfNGvbczQ'
ACCESS_TOKEN = '1936186141-P1P8jBW8gwcLVMOW3kzeSOoF8GXvkyCPYvq4uB9'
ACCESS_TOKEN_SECRET = 'aLyYUHTYXkS4VHdI8Wvf49ydOOWYjMldGrMeFSMukeWuU'
TULINGKEY = "0a3727130d754c8d95797977f8f61646"
TULINGURL = "http://www.tuling123.com/openapi/api?"
TIME_ONEDAY = datetime.timedelta(1)

KCWIKI_DATA = "http://kcwikizh.github.io/kcdata/slotitem/poi_improve.json"

GROUP_NUMBER = '337545621'

with open('responses.csv', mode = 'r') as infile:
	reader = csv.reader(infile)
	responses = {rows[0]:rows[1] for rows in reader}


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
repCounter = 0
prevMsg = ''



@qqbotslot
def onQQMessage(bot, contact, member, content):
	global api
	if (contact.qq == '1259276249'):
		content = {'userid':'123456', 'info':content, 'key':TULINGKEY}
		data = json.dumps(content)
		req = urllib2.Request(TULINGURL, data, {'Content-Type': 'application'})
		re = urllib2.urlopen(req)
		re = re.read()
		re_dict = json.loads(re)
		text = re_dict['text']
		bot.SendTo(contact, str(text.encode('utf-8', 'ignore')))
		if (content == '-stop'):
			bot.SendTo(contact, 'QQ Bot terminated')
			bot.Stop()

		
		if('@正规空母翔鹤' in content):
			for key, value in responses.iteritems():
				print(key)
				if key in content:

					bot.SendTo(contact, value)
					break

		if('抓取官推' in content):
			time_now = datetime.datetime.now()
			public_tweets = api.user_timeline('fgoproject')
			for tweet in public_tweets:
				if(time_now - tweet.created_at < TIME_ONEDAY):
					time.sleep(1)
					bot.SendTo(contact, str(tweet.text.encode('utf-8', 'ignore')))
					
    #testgroup '209127315' target 337545621
	if (contact.qq == GROUP_NUMBER and '@ME' in content): #info mode
		#check the info list
		
		for key, value in responses.iteritems():
			if key in content:
				bot.SendTo(contact, value)
				return

		if('攻略' in content or '配置' in content or '带路' in content):
			#turn to kcwiki pages
			area = ''
			if('1-' in content):
				area = urllib2.quote('镇守府海域')
			if('2-' in content):
				area = urllib2.quote('南西群岛海域')
			if('3-' in content):
				area = urllib2.quote('北方海域')
			if('4-' in content):
				area = urllib2.quote('西方海域')
			if('5-' in content):
				area = urllib2.quote('南方海域')
			if('6-' in content):
				area = urllib2.quote('中部海域')

			pattern = regex.compile(r'\d-\d')
			subarea = regex.search(pattern, content).group()
			print(subarea)

			html_content = urllib2.urlopen('https://zh.kcwiki.org/wiki/' + area + '/' + subarea).read()
			soup = BS(html_content)
			print(soup.title)
			flag = False

			pattern = regex.compile(r'</?\w+[^>]*>|<br\s*?/?>|\n+')

			for item in soup.find_all('div'):
				if(flag and item.ul is not None):
					for entry in item.ul:
						time.sleep(1)
						bot.SendTo(contact, str(pattern.sub('',str(entry))).encode('utf-8'))
						
					break

				if(item.b is not None and '海域情报' in str(item.b)):
					print(item.get('class'))
					flag = True
			return



		if('FGO' in content and '情报' in content):
			time_now = datetime.datetime.now()
			public_tweets = api.user_timeline('fgoproject')
			for tweet in public_tweets:
				if(time_now - tweet.created_at < TIME_ONEDAY):
					time.sleep(1)
					bot.SendTo(contact, str(tweet.text.encode('utf-8', 'ignore')))
			return


		if('舰' in content and '情报' in content):
			time_now = datetime.datetime.now()
			public_tweets = api.user_timeline('KanColle_STAFF')
			for tweet in public_tweets:
				if(time_now - tweet.created_at < TIME_ONEDAY):
					time.sleep(1)
					bot.SendTo(contact, str(tweet.text.encode('utf-8', 'ignore')))
			return

		#氪金信息
		if('充值' in content or '氪金' in content):
			print('check for current price')
			bot.SendTo(contact, 'FGO黑卡充值：'.encode('utf-8') + 'https://item.taobao.com/item.htm?spm=0.0.0.0.nBUIej&id=546772277736')
			bot.SendTo(contact, 'FGO白卡充值：'.encode('utf-8') + 'https://item.taobao.com/item.htm?spm=a1z0k.7628870.0.0.kayXcs&id=545942439642&_u=p2o03db0b500')
			bot.SendTo(contact, '舰娘氪金：'.encode('utf-8') + 'https://item.taobao.com/item.htm?spm=a1z10.5-c.w4002-15864276650.23.yejdE6&id=539141881167')
			return

		#if no keywords matched, turn to tuling123 api
		#the response categories: 100000 = text, 200000 = url, 302000 = news(return type is perhaps a list)
		if('改修' in content):
			print('checking for akashi factory list')
			req = urllib2.Request(KCWIKI_DATA)
			re = urllib2.urlopen(req)
			re = re.read()
			equip_list = json.loads(re)
			today_week = datetime.datetime.now() + datetime.timedelta(hours = 14)
			today_week = today_week.weekday()

			for equip in equip_list:
				current_requirement = equip[u'improvement'][0]
				days = current_requirement[u'req'][0][u'day']
				if(days[today_week]):
					# current item can be improved today
					info = equip[u'name'] + ' 秘书舰: '.encode('utf-8')
					secretary_list = current_requirement[u'req'][0][u'secretary']
					



		pure_content = content.decode('utf8')[6:].encode('utf8')
		print('pure_content = ' + pure_content.encode('gb2312'))
		content = {'userid':member.uin, 'info':pure_content, 'key':TULINGKEY}
		data = json.dumps(content)
		req = urllib2.Request(TULINGURL, data, {'Content-Type': 'application'})
		re = urllib2.urlopen(req)
		re = re.read()
		re_dict = json.loads(re)
		category = re_dict['code']
		print(category)
		if(category == 100000):
			text = re_dict['text']
			bot.SendTo(contact, str(text.encode('utf-8')))
		elif(category == 200000):
			text = re_dict['text']
			bot.SendTo(contact, str(text.encode('utf-8')))
			link = re_dict['url']
			bot.SendTo(contact, str(link.encode('utf-8')))
		elif(category == 308000): #the return type is a list
			text = re_dict['text']
			bot.SendTo(contact, str(text.encode('utf-8')))
			return_list = re_dict['list']
			print(len(return_list))
			counter = 0
			for item in return_list:
				time.sleep(1)
				bot.SendTo(contact, item['name'].encode('utf-8') + '用料: '.encode('utf-8')
					+ item['info'].encode('utf-8') + ' 详细做法: '.encode('utf-8') + item['detailurl'].encode('utf-8'))
				counter+=1
				if(counter > 2):
					break
		elif(category == 302000):
			text = re_dict['text']
			bot.SendTo(contact, str(text.encode('utf-8')))
			return_list = re_dict['list']
			print(len(return_list))
			counter = 0
			for item in return_list:
				time.sleep(1)
				bot.SendTo(contact, item['article'].encode('utf-8') + ' 消息来自: '.encode('utf-8')
					+ item['source'].encode('utf-8') + ' 详情请见: '.encode('utf-8') + item['detailurl'].encode('utf-8'))
				counter+=1
				if(counter > 2):
					break
	else:
		
		#trolling in chat
		#1. 复读
		# repeatition should be such that, once it has participated in a row, it should not say anything anymore
		global repCounter
		global prevMsg
		curMsg = content
		if(repCounter == 0):
			repCounter += 1
		else:
			if(curMsg == prevMsg):
				repCounter += 1
				print(repCounter)
			else:
				if(repCounter > 3):
					bot.SendTo(contact, '你们的复读坚持了' + str(repCounter + 1) + '次~人类的本质就是个复读机！')
				repCounter = 0
		if(repCounter == 3):
			bot.SendTo(contact, content)

		prevMsg = curMsg

@qqbotslot
def onInterval(bot):
	
	test_group = bot.List('group', '337545621')[0]
	#	bot.SendTo(test_group, 'interval method evoked')
	#execute per 5mins
	#sending debug info
	
	time_now = datetime.datetime.time(datetime.datetime.now())
	if(time_now >= datetime.time(0,50,0,0) and time_now < datetime.time(0,55,0,0)):
		bot.SendTo(test_group, 'Kancolle 演习马上更新， 请各位提督不要忘记演习~'.encode('utf-8'))
	if(time_now >= datetime.time(12,50,0,0) and time_now < datetime.time(12,55,0,0)):
		bot.SendTo(test_group, 'Kancolle 演习马上更新， 请各位提督不要忘记演习~'.encode('utf-8'))

	if(time_now >= datetime.time(6,50,0,0) and time_now < datetime.time(6,55,0,0)):
		public_tweets = api.user_timeline('fgoproject')
		for tweet in public_tweets:
			if(datetime.datetime.now() - tweet.created_at < TIME_ONEDAY):
				bot.SendTo(test_group, str(tweet.text.encode('utf-8', 'ignore')))
		public_tweets = api.user_timeline('KanColle_STAFF')
		for tweet in public_tweets:
			if(time_now - tweet.created_at < TIME_ONEDAY):
				bot.SendTo(test_group, str(tweet.text.encode('utf-8', 'ignore')))

	if(time_now >= datetime.time(10,0,0,0) and time_now < datetime.time(10,5,0,0)):
		bot.SendTo(test_group, 'FGO日常任务以及免费友情点十连已经更新~'.encode('utf-8'))

	if(time_now >= datetime.time(14,0,0,0) and time_now < datetime.time(14,5,0,0)):
		bot.SendTo(test_group, 'FGO日常登录奖励大家不要错过哦~'.encode('utf-8'))

	if(time_now >= datetime.time(15,0,0,0) and time_now < datetime.time(15,5,0,0)):
		bot.SendTo(test_group, 'Kancolle每日任务已经更新~'.encode('utf-8'))
	#some time point,
	#1am, kancolle drill
	#6am, check latest info
	#10am, FGO free summoning, daily quest update
	#1pm, kancolle drill
	#2pm, FGO login award
	#3pm, kancolle quest update

@qqbotslot
def onNewContact(bot, contact, owner):
	#exec when there is new member joining owner
	print('onNewContact evoked')
	if(owner is None): return
	if(owner.qq == GROUP_NUMBER):
		test_group = bot.List('group', GROUP_NUMBER)[0]
		new_member = bot.List(test_group, 'qq='+str(contact.qq))[0]
		bot.SendTo(owner, '欢迎新dalao~'.encode('utf-8'))
		bot.SendTo(owner, 'Hello '.encode('utf-8')+ contact.card.encode('utf-8')+'. 我是翔鹤，有什么问题可以at我，如果对于我的功能有什么建议的话请找nilk.'
			.encode('utf-8'))

#open the info table



RunBot(qq='3407757156', user = None)

'''
Goal:
1. Nilk will be the only authorized person who has the ability to edit the response of it.
2. Can troll in the group chat
3. When called out by @, provide proper info
'''

'''
	TODO：
	0. try to trim the @me before msg in group chat(done)
	1.点歌，发url
	
	3.氪金信息
	4.crawl for info, instead of hard coded csv(done)
	5.今日改修，今日修炼场，今日种火
	6.定时提醒清本，上线清任务领奖励（done）
	7.带33节奏

	舰娘信息可以用kcwiki api
'''



