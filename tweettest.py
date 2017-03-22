# -*- coding: utf-8 -*-
import tweepy
import datetime

CONSUMER_KEY = 'uWb94m6mwDnHOix6YAfMQ1ESt'
CONSUMER_SECRET = 'AHOrZYDUvskktLFIQRvXxnN7hDxtkaW8PZQsg1AatQfNGvbczQ'
ACCESS_TOKEN = '1936186141-P1P8jBW8gwcLVMOW3kzeSOoF8GXvkyCPYvq4uB9'
ACCESS_TOKEN_SECRET = 'aLyYUHTYXkS4VHdI8Wvf49ydOOWYjMldGrMeFSMukeWuU'
TIME_NOW = datetime.datetime.now()
TIME_ONEDAY = datetime.timedelta(1)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

#crawl the latest twitter, within 24h
public_tweets = api.user_timeline('fgoproject')
for tweet in public_tweets:
	if(TIME_NOW - tweet.created_at < TIME_ONEDAY):
		print tweet.text.encode('GBK', 'ignore')
