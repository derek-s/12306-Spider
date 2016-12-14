# -*- coding: UTF-8 -*-
#列车时刻表信息
__author__ = 'Derek.S'


import MySQLdb
import urllib2
import json
import sys 
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context
default_encoding = 'utf8'
default_decoding = 'utf8'
db = MySQLdb.connect("192.168.10.105","root","123a+-","12306")
cursor = db.cursor()
db.set_character_set('utf8')

xian = "-----------------------------------------------------"
def timetable():
    cursor.execute('select count(*) from TrainList')
    tableall = cursor.fetchone()
    cursor.execute('select ID from TrainList limit 1')
    firstRow = cursor.fetchone()
    allRows = firstRow[0] + tableall[0]
    i = firstRow[0]
    while (i < allRows):
        #print i
    
        cursor.execute(r"select * from TrainList where ID = '%d'" % (i))
        No = cursor.fetchone()
        print u"车次信息".encode('gbk')
        print No[1],No[2].decode('utf8'),No[3].decode('utf8') 
        print xian 
        cursor.execute(r"select Telegraph from Station where Station = '%s'" % (No[2].decode('utf8')) )
        shifaT = cursor.fetchone()
        print u'始发站电报码'.encode('gbk')
        print shifaT[0]
        print xian
        cursor.execute(r"select Telegraph from Station where Station = '%s' " % (No[3].decode('utf8')) )
        zhongdao = cursor.fetchone()
        print u'终到站电报码'.encode('gbk')
        print zhongdao[0]
        print xian
        print u'url查询地址'.encode('gbk')
        url =  ("https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=2016-12-10" % (No[4],shifaT[0],zhongdao[0]))
        print url
        print xian
        data = urllib2.urlopen(url).read()
        print u'json信息'
        print data.decode('utf8')
        print xian
        print u'写入json文件'.encode('gbk')
        print xian
        print xian
        print u'关闭文件'.encode('gbk')
        print xian
        print u'查询等待5s'.encode('gbk')
        print xian
        time.sleep(10)
        i = i+1