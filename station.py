# -*- coding:utf-8 -*-
#站名提取

__author__ = 'Derek.S'

import MySQLdb
import re
import string
import urllib2
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
db = MySQLdb.connect("192.168.10.105","root","123a+-","12306")
cursor = db.cursor()
db.set_character_set('utf8')

def station():
    '抓取车站名'
    url = urllib2.urlopen("https://kyfw.12306.cn/otn/resources/js/framework/station_name.js").read()
    utf8info = url.decode('utf8')
    jsdata = re.findall(u"\w+\|[\u4e00-\u9fa5]*\|\w+\|\w+\|\w+\|\d",utf8info)
    #print jsdata[0].split('|')[1]
    print "共有车站：",len(jsdata),"个"
    i = 0
    while(i<len(jsdata)):
        print "拼音码：",jsdata[i].split('|')[0],"站名：",jsdata[i].split('|')[1],"电报码：",jsdata[i].split('|')[2],"拼音：",jsdata[i].split('|')[3]
        print "写入数据库"
        cursor.execute('insert into Station( Brevity, Station, Telegraph, Pinyin)  values( "%s", "%s", "%s", "%s")' % ( jsdata[i].split('|')[0] , jsdata[i].split('|')[1] , jsdata[i].split('|')[2] , jsdata[i].split('|')[3] ) )
        db.commit()
        i = i + 1
    print "写入完成"
    db.close()

if __name__ == "__main__":

    station()
