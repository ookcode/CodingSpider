#!/usr/bin/python
#coding=utf-8
###########################################################
#
#2016年抓周活动自动化脚本
#
###########################################################
from __future__ import unicode_literals

import cookielib
import datetime
import hashlib
import json
import os
import sys
import urllib
import urllib2
import time

USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/45.0.2454.93 Safari/537.36'
)

class APIError(Exception):
    pass

class Client(object):
    def __init__(self):
        self.cookiejar = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.cookiejar),
        )
        self.opener.addheaders = [
            ('User-Agent', USER_AGENT),
        ]
        self.global_key = None

    def load_cookies(self, path):
        self.cookiejar.load(path)

    def save_cookies(self, path):
        self.cookiejar.save(path)

    def request(self, method, url, data=None):
        payload = urllib.urlencode(data) if data else None
        request = urllib2.Request(url, payload)
        request.get_method = lambda: method
        #网络错误自动重试
        for i in range(0,3):
            try:
                response = self.opener.open(request)
                break
            except Exception as e:
                if i == 2 :
                    print '网络错误，重试次数过多，跳过该操作'
                    return ''
                else :
                    print "网络错误，正在进行第{}次重试".format(i + 1)
                    time.sleep(1)
        data = json.loads(response.read())
        if data['code'] != 0:
            if 'msg' in data :
                raise APIError(data['msg'])
            else :
                raise APIError("unknow error")
        if 'data' in data :
            return data['data']
        return ''
        
    def get_account_info(self):
        return self.request('GET', 'https://coding.net/api/account/current_user')

    def login(self, username, password):
        page = self.request('GET', 'https://coding.net/api/captcha/login')
        #assert not page

        if len(password) == 40 :
            password_hash = password
        else :
            password_hash = hashlib.sha1(password).hexdigest()

        payload = {
            'email': username,
            'password': password_hash,
            'remember_me': True,
        }
        page = self.request('POST', 'https://coding.net/api/login', data=payload)
        self.global_key = page['global_key']
        self.id = page['id']

    def join_event(self):
        payload = {
            'lang': "paython",
        }
        resp = self.request('POST', 'https://coding.net/api/marketing/lottery/go', data=payload)
        return resp

def routine(username, password, save_cookies):

    client = Client()
    cookies_path = os.path.expanduser('~/.{}.cookies'.format(username))
    
    try:
        try:
            if not save_cookies :
                raise APIError('')
            #载入缓存的cookies
            #发送请求账户信息的get请求，获取key与id
            client.load_cookies(cookies_path)
            print 'Cookies已装载'
            info = client.get_account_info()
            client.global_key = info['global_key']
            client.id = info['id']
            print '账户ID确认: "{}"'.format(client.global_key)
        except (IOError, APIError):
            #cookies无效，重新登录
            client.login(username, password)
            print '账户: "{}" 登陆成功'.format(client.global_key)
            if save_cookies :
                client.save_cookies(cookies_path)
                print 'Cookies已存储.'

        for i in range(0,10):
        	data = client.join_event()
    		print "恭喜您获得 " + data["prize"]["name"]
    		time.sleep(1)

    except APIError as e:
        print 'Error:'
        for k, v in e.message.iteritems():
            print k, v

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    config_path = os.path.expanduser('~/.coding.config')

    if not os.path.exists(config_path):
        print '错误：配置文件 ' + config_path + ' 未找到'
        return

    with open(config_path, 'r') as f:
        try:
            config = json.load(f)
        except Exception,e :
            print "错误：配置文件格式不正确"
            return

    count = 0
    for account in config:
        if 'username' in account and 'password' in account :
            print "--------------------------------------------------------"
            print '{}: 正在召唤 {}'.format(count,account['username'])
            print "--------------------------------------------------------"
            routine(
                username = account['username'],
                password = account['password'],
                save_cookies = True
            )
            count = count + 1
        else:
            print '错误：未能在配置文件中读取账号密码'
    
if __name__ == '__main__':
    main()
