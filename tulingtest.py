# -*- coding: utf-8 -*-
import os
import json
import urllib2
import sys

reload(sys)
sys.setdefaultencoding('utf8')
print sys.getdefaultencoding()

class Chat(object):
    key = "0a3727130d754c8d95797977f8f61646"
    apiurl = "http://www.tuling123.com/openapi/api?"
    userId = '123456'

    def __init__(self):
        os.system("clear")
        print("尽情调教我吧!".encode('GBK'))
        print("-" * 60)   

    def get(self):
    	
        print("> "),
        info = raw_input()
        if info == 'q' or info == 'exit' or info == "quit":
            print("- Goodbye")
            return
        self.send(unicode(info.decode("gb2312")))

    def send(self, info):
    	print(info)
        #url = self.apiurl + 'key=' + self.key + '&' + 'info=' + info
        content = {'userid':self.userId, 'info':info, 'key':self.key}
        data = json.dumps(content)
        req = urllib2.Request(self.apiurl, data, {'Content-Type': 'application'})
        re = urllib2.urlopen(req)
        re = re.read()
        re_dict = json.loads(re)
        text = re_dict['text']
        print '- ', text
        self.get()

if __name__ == "__main__":
    chat = Chat()
    chat.get()