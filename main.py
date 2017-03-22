# -*- coding: utf-8 -*-
__author__ = 'Nilk'

from qqbot import QQBot
import csv
import tweepy
import datetime

CONSUMER_KEY = 'uWb94m6mwDnHOix6YAfMQ1ESt'
CONSUMER_SECRET = 'AHOrZYDUvskktLFIQRvXxnN7hDxtkaW8PZQsg1AatQfNGvbczQ'
ACCESS_TOKEN = '1936186141-P1P8jBW8gwcLVMOW3kzeSOoF8GXvkyCPYvq4uB9'
ACCESS_TOKEN_SECRET = 'aLyYUHTYXkS4VHdI8Wvf49ydOOWYjMldGrMeFSMukeWuU'
TIME_ONEDAY = datetime.timedelta(1)

class QQBotWithState(QQBot):
	def __init__(self, qq=None, user=None, conf=None, ai=None):
		QQBot.__init__(self, qq, user, conf, ai)
		with open('responses.csv', mode = 'r') as infile:
			reader = csv.reader(infile)
			self.responses = {rows[0]:rows[1] for rows in reader}
		self.repCounter = 0
		self.prevMsg = ''

		self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

		self.api = tweepy.API(self.auth)

#open the info table



myqqbot = QQBotWithState(qq = '3407757156')

'''
Goal:
1. Nilk will be the only authorized person who has the ability to edit the response of it.
2. Can troll in the group chat
3. When called out by @, provide proper info
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

	#in group chat
	#Keyword search
	if (message.contact.qq == '337545621' and ('@正规空母翔鹤' in message.content)): #info mode
		#check the info list
		for key, value in myqqbot.responses.iteritems():
			if key in message.content:
				bot.SendTo(message.contact, value)
				break

		if('FGO' in message.content and '情报' in message.content):
			time_now = datetime.datetime.now()
			public_tweets = bot.api.user_timeline('fgoproject')
			for tweet in public_tweets:
				if(time_now - tweet.created_at < TIME_ONEDAY):
					bot.SendTo(message.contact, str(tweet.text.encode('utf-8', 'ignore')))

		if('舰' in message.content and '情报' in message.content):
			time_now = datetime.datetime.now()
			public_tweets = bot.api.user_timeline('KanColle_STAFF')
			for tweet in public_tweets:
				if(time_now - tweet.created_at < TIME_ONEDAY):
					bot.SendTo(message.contact, str(tweet.text.encode('utf-8', 'ignore')))


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
	TODO：
	1.点歌，发url
	2.最新运营情报，舰娘官推，FGO活动公告
	3.氪金信息
	4.crawl for info, instead of hard coded csv
	5.今日改修，今日修炼场，今日种火
	6.定时提醒清本，上线清任务领奖励
	7.带33节奏

	舰娘信息可以用kcwiki api
	'''



myqqbot.LoginAndRun()



