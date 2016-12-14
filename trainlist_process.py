# -*- coding:utf-8 -*-


__author__ = 'Derek.S'


import MySQLdb
import urllib2
import json
import sys 
import ssl
import time
import re
import io

db = MySQLdb.connect("192.168.10.105","root","123a+-","12306")
cursor = db.cursor()
db.set_character_set('utf8')

ssl._create_default_https_context = ssl._create_unverified_context

def trainlistProcess():
    '12306车次js文件处理函数'
    listjs = urllib2.urlopen("http://192.168.231.2/train_list.js").read()
    listdata = listjs.replace('var train_list =','')
    listjson = json.loads(listdata)

    dayslist = listjson.keys()
    print "当前js文件中存在的日期:"
    print dayslist
    day = raw_input("请输入需要抓取的日期:")
    traininfo = listjson[day]
    info = json.dumps(traininfo,encoding='utf-8',ensure_ascii=False)

    pattern = re.finditer(ur".station_train_code.:\s.(?P<code>[^\(]+)\((?P<shifa>[\u4e00-\u9fa5]+)-(?P<zhongdao>[\u4e00-\u9fa5]+)\)..\s.train_no.:\s.(?P<no>[\w]+).",info)
    #print pattern
    for match in pattern:
        print "写入数据库:",match.group(1),match.group(2),match.group(3),match.group(4)
        cursor.execute('insert into TrainList( Code, Terminus, Origin, No)  values( "%s", "%s", "%s", "%s")' % ( match.group(1) , match.group(2) , match.group(3) , match.group(4) ) )
        db.commit()
    print "写入完成"
    db.close()
    
