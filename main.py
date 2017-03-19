# -*- coding: utf-8 -*-
__author__ = 'Nilk'

from qqbot import QQBot
import csv

class QQBotWithState(QQBot):
	def __init__(self, qq=None, user=None, conf=None, ai=None):
		QQBot.__init__(self, qq, user, conf, ai)
		with open('responses.csv', mode = 'r') as infile:
			reader = csv.reader(infile)
			self.responses = {rows[0]:rows[1] for rows in reader}
		self.repCounter = 0
		self.prevMsg = ''

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

	#in group chat
	#Keyword search
	if (message.contact.qq == '337545621' and ('@正规空母翔鹤' in message.content)): #info mode
		#check the info list
		for key, value in myqqbot.responses.iteritems():
			if key in message.content:
				bot.SendTo(message.contact, value)
				break

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
				if(myqqbot.repCounter > 6):
					bot.SendTo(message.contact, '你们的复读坚持了' + str(myqqbot.repCounter) + '次~人类的本质就是个复读机！')
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
	'''



myqqbot.LoginAndRun()



