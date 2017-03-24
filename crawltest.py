# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import re
content = urllib2.urlopen('https://zh.kcwiki.moe/wiki/南方海域/5-5').read()
soup = BeautifulSoup(content)
print(soup.title)
flag = False

pattern = re.compile(r'</?\w+[^>]*>|<br\s*?/?>|\n+')

for item in soup.find_all('div'):
	if(flag and item.ul is not None):
		for entry in item.ul:
			print(str(pattern.sub('',str(entry))))
		break

	if(item.b is not None and '海域情报' in str(item.b)):
		print(item.get('class'))
		flag = True