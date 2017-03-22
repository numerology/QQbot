# -*- coding: utf-8 -*-
__author__ = 'Nilk'

from qqbot import QQBot, RunBot
import csv
import tweepy
import datetime
import os
import json
import urllib2
import sys

reload(sys)
sys.setdefaultencoding('utf8')

CONSUMER_KEY = 'uWb94m6mwDnHOix6YAfMQ1ESt'
CONSUMER_SECRET = 'AHOrZYDUvskktLFIQRvXxnN7hDxtkaW8PZQsg1AatQfNGvbczQ'
ACCESS_TOKEN = '1936186141-P1P8jBW8gwcLVMOW3kzeSOoF8GXvkyCPYvq4uB9'
ACCESS_TOKEN_SECRET = 'aLyYUHTYXkS4VHdI8Wvf49ydOOWYjMldGrMeFSMukeWuU'
TULINGKEY = "0a3727130d754c8d95797977f8f61646"
TULINGURL = "http://www.tuling123.com/openapi/api?"
TIME_ONEDAY = datetime.timedelta(1)

with open('responses.csv', mode = 'r') as infile:
	reader = csv.reader(infile)
	responses = {rows[0]:rows[1] for rows in reader}


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

class QQBotWithState(QQBot):
	def __init__(self):
		self.repCounter = 0
		self.prevMsg = ''

	def onQQMessage(self, contact, member, content):
		if (contact.qq == '1259276249'):
			content = {'userid':'123456', 'info':content, 'key':TULINGKEY}
			data = json.dumps(content)
			req = urllib2.Request(TULINGURL, data, {'Content-Type': 'application'})
			re = urllib2.urlopen(req)
			re = re.read()
			re_dict = json.loads(re)
			text = re_dict['text']
			self.SendTo(contact, str(text.encode('utf-8', 'ignore')))
			if (content == '-stop'):
				self.SendTo(contact, 'QQ Bot terminated')
				self.Stop()

			
			if('@正规空母翔鹤' in content):
				for key, value in responses.iteritems():
					print(key)
					if key in content:
						self.SendTo(contact, value)
						break

			if('抓取官推' in content):
				time_now = datetime.datetime.now()
				public_tweets = api.user_timeline('fgoproject')
				for tweet in public_tweets:
					if(time_now - tweet.created_at < TIME_ONEDAY):
						self.SendTo(contact, str(tweet.text.encode('utf-8', 'ignore')))
			
			
	            	
		if (contact.qq == '337545621' and '@ME' in content): #info mode
			#check the info list
			print(str(content[8:-1]))
			
			for key, value in responses.iteritems():
				if key in content:
					self.SendTo(contact, value)
					return


			if('FGO' in content and '情报' in content):
				time_now = datetime.datetime.now()
				public_tweets = api.user_timeline('fgoproject')
				for tweet in public_tweets:
					if(time_now - tweet.created_at < TIME_ONEDAY):
						self.SendTo(contact, str(tweet.text.encode('utf-8', 'ignore')))
				return


			if('舰' in content and '情报' in content):
				time_now = datetime.datetime.now()
				public_tweets = api.user_timeline('KanColle_STAFF')
				for tweet in public_tweets:
					if(time_now - tweet.created_at < TIME_ONEDAY):
						self.SendTo(contact, str(tweet.text.encode('utf-8', 'ignore')))
				return
			

			#if no keywords matched, turn to tuling123 api
			#the response categories: 100000 = text, 200000 = url, 302000 = news(return type is perhaps a list)
			content = {'userid':member.uin, 'info':content, 'key':TULINGKEY}
			data = json.dumps(content)
			req = urllib2.Request(TULINGURL, data, {'Content-Type': 'application'})
			re = urllib2.urlopen(req)
			re = re.read()
			re_dict = json.loads(re)
			category = re_dict['code']
			print(category)
			if(category == 100000):
				text = re_dict['text']
				self.SendTo(contact, str(text.encode('utf-8')))
			elif(category == 200000):
				text = re_dict['text']
				self.SendTo(contact, str(text.encode('utf-8')))
				link = re_dict['url']
				self.SendTo(contact, str(link.encode('utf-8')))
			
		else:
			
			#trolling in chat
			#1. 复读
			# repeatition should be such that, once it has participated in a row, it should not say anything anymore
			
			curMsg = content
			if(self.repCounter == 0):
				self.repCounter += 1
			else:
				if(curMsg == self.prevMsg):
					self.repCounter += 1
					print(self.repCounter)
				else:
					if(self.repCounter > 3):
						self.SendTo(contact, '你们的复读坚持了' + str(self.repCounter + 1) + '次~人类的本质就是个复读机！')
					self.repCounter = 0
			if(self.repCounter == 3):
				self.SendTo(contact, content)

			self.prevMsg = curMsg
			
		

#open the info table



RunBot(QQBotWithState, qq='3407757156', user=None)

'''
Goal:
1. Nilk will be the only authorized person who has the ability to edit the response of it.
2. Can troll in the group chat
3. When called out by @, provide proper info
'''

'''
	TODO：
	0. try to trim the @me before msg in group chat
	1.点歌，发url
	
	3.氪金信息
	4.crawl for info, instead of hard coded csv
	5.今日改修，今日修炼场，今日种火
	6.定时提醒清本，上线清任务领奖励
	7.带33节奏

	舰娘信息可以用kcwiki api
'''



#myqqbot.LoginAndRun()



