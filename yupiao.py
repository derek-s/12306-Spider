# -*- coding:utf8 -*-
# 12306 余票查询
__author__ = 'Derek.S'

import ssl
import urllib2
import json
import re
import time
import pygame

ssl._create_default_https_context = ssl._create_unverified_context





fromstation = 'CAY'
tostation = 'HRX'

data = ['2017-01-16','2017-01-17','2017-01-18']

i = 0
while True:
    while i < len(data): 
        url = ("https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=%s&from_station=%s&to_station=%s" % (data[i],fromstation,tostation))
        piaoData = urllib2.urlopen(url).read()
        jsData = json.loads(piaoData)
        rootdata = jsData['data']
        subdata = rootdata['datas']
        print subdata[0]['start_train_date']
        print subdata[0]['yw_num']
        if subdata[0]['yw_num'].encode('utf8') != '无':
            pygame.mixer.init()
            pygame.mixer.music.load("2207.wav")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
        i += 1
    print '查询一次,暂停60秒后第二次查询'    
    time.sleep(60)
    i = 0