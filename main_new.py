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

repCounter = 0
prevMsg = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

class QQBotWithState(QQBot):
	
	

	def onQQMessage(self, contact, member, content):
		if (contact.qq == '1259276249'):
			self.SendTo(contact, 'copy that')
			if (content == '-stop'):
				self.SendTo(contact, 'QQ Bot terminated')
				self.Stop()
		if (contact.qq == '209127315'): #info mode
			#check the info list
			#print(str(content))
			self.SendTo(contact, content)
			
			
			for key, value in responses.iteritems():
				if key in content:
					self.SendTo(contact, value)
					return

			'''
			if('FGO' in content and '情报' in content):
				time_now = datetime.datetime.now()
				public_tweets = self.api.user_timeline('fgoproject')
				for tweet in public_tweets:
					if(time_now - tweet.created_at < TIME_ONEDAY):
						self.SendTo(contact, str(tweet.text.encode('utf-8', 'ignore')))
				return


			if('舰' in message.content and '情报' in message.content):
				time_now = datetime.datetime.now()
				public_tweets = self.api.user_timeline('KanColle_STAFF')
				for tweet in public_tweets:
					if(time_now - tweet.created_at < TIME_ONEDAY):
						self.SendTo(contact, str(tweet.text.encode('utf-8', 'ignore')))
				return
			'''

			#if no keywords matched, turn to tuling123 api
			#the response categories: 100000 = text, 200000 = url, 302000 = news(return type is perhaps a list)
			'''
			content = {'userid':'123456', 'info':'你好', 'key':TULINGKEY}
	        data = json.dumps(content)
	        req = urllib2.Request(TULINGURL, data, {'Content-Type': 'application'})
	        re = urllib2.urlopen(req)
	        re = re.read()
	        re_dict = json.loads(re)
	        category = re_dict['code']
	        if(code == '100000'):
	        	text = re_dict['text']
	        	self.SendTo(contact, str(text.encode('utf-8', 'ignore')))
	       		return
	        elif(code == '200000'):
	        	text = re_dict['text']
	        	link = re_dict['url']
	        	self.SendTo(contact, str(text.encode('utf-8', 'ignore')) + ':' + str(link))
		        return
		    '''
			#trolling in chat
			#1. 复读
			# repeatition should be such that, once it has participated in a row, it should not say anything anymore
			'''
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
			'''
		

#open the info table



RunBot(QQBotWithState, qq='3407757156', user=None)

'''
Goal:
1. Nilk will be the only authorized person who has the ability to edit the response of it.
2. Can troll in the group chat
3. When called out by @, provide proper info
'''

'''
@myqqbot.On('qqmessage')
def handler(bot, message):
	#editing
	if (message.contact.qq == '1259276249'):
		bot.SendTo(message.contact, 'copy that')
		if (message.content == '-stop'):
			bot.SendTo(message.contact, 'QQ Bot terminated')
			bot.Stop()

		if('@正规空母翔鹤' in message.content):
			for key, value in myqqbot.responses.iteritems():
				print(key)
				if key in message.content:
					bot.SendTo(message.contact, value)
					break

		if('抓取官推' in message.content):
			time_now = datetime.datetime.now()
			public_tweets = bot.api.user_timeline('fgoproject')
			for tweet in public_tweets:
				if(time_now - tweet.created_at < TIME_ONEDAY):
					bot.SendTo(message.contact, str(tweet.text.encode('utf-8', 'ignore')))
		
		content = {'userid':'123456', 'info':message.content, 'key':TULINGKEY}
        data = json.dumps(content)
        req = urllib2.Request(TULINGURL, data, {'Content-Type': 'application'})
        re = urllib2.urlopen(req)
        re = re.read()
        re_dict = json.loads(re)
        text = re_dict['text']
        bot.SendTo(message.contact, str(text.encode('utf-8', 'ignore')))
    	return

	#in group chat
	#Keyword search
	if (message.contact.qq == '337545621' and ('@正规空母翔鹤' in message.content)): #info mode
		#check the info list
		for key, value in myqqbot.responses.iteritems():
			if key in message.content:
				flag = False
				bot.SendTo(message.contact, value)
				return


		if('FGO' in message.content and '情报' in message.content):
			time_now = datetime.datetime.now()
			public_tweets = bot.api.user_timeline('fgoproject')
			for tweet in public_tweets:
				if(time_now - tweet.created_at < TIME_ONEDAY):
					bot.SendTo(message.contact, str(tweet.text.encode('utf-8', 'ignore')))
			return


		if('舰' in message.content and '情报' in message.content):
			time_now = datetime.datetime.now()
			public_tweets = bot.api.user_timeline('KanColle_STAFF')
			for tweet in public_tweets:
				if(time_now - tweet.created_at < TIME_ONEDAY):
					bot.SendTo(message.contact, str(tweet.text.encode('utf-8', 'ignore')))
			return


		#if no keywords matched, turn to tuling123 api
		#the response categories: 100000 = text, 200000 = url, 302000 = news(return type is perhaps a list)
		content = {'userid':message.memberUin, 'info':message.content, 'key':TULINGKEY}
        data = json.dumps(content)
        req = urllib2.Request(TULINGURL, data, {'Content-Type': 'application'})
        re = urllib2.urlopen(req)
        re = re.read()
        re_dict = json.loads(re)
        category = re_dict['code']
        if(code == '100000'):
        	text = re_dict['text']
        	bot.SendTo(message.contact, str(text.encode('utf-8', 'ignore')))
       		return
        elif(code == '200000'):
        	text = re_dict['text']
        	link = re_dict['url']
        	bot.SendTo(message.contact, str(text.encode('utf-8', 'ignore')) + ':' + str(link))
	        return
	else:
		#trolling in chat
		#1. 复读
		# repeatition should be such that, once it has participated in a row, it should not say anything anymore
		curMsg = message.content
		if(myqqbot.repCounter == 0):
			myqqbot.repCounter += 1
		else:
			if(curMsg == myqqbot.prevMsg):
				myqqbot.repCounter += 1
				print(myqqbot.repCounter)
			else:
				if(myqqbot.repCounter > 3):
					bot.SendTo(message.contact, '你们的复读坚持了' + str(myqqbot.repCounter + 1) + '次~人类的本质就是个复读机！')
				myqqbot.repCounter = 0
		if(myqqbot.repCounter == 3):
			bot.SendTo(message.contact, message.content)

		myqqbot.prevMsg = curMsg
'''

'''
	TODO：
	1.点歌，发url
	
	3.氪金信息
	4.crawl for info, instead of hard coded csv
	5.今日改修，今日修炼场，今日种火
	6.定时提醒清本，上线清任务领奖励
	7.带33节奏

	舰娘信息可以用kcwiki api
'''



#myqqbot.LoginAndRun()



