# -*- coding: UTF-8 -*-
#列车时刻表信息抓取入库
__author__ = 'Derek.S'


import MySQLdb
import urllib2
import json
import sys 
import ssl
import time
import io

ssl._create_default_https_context = ssl._create_unverified_context
default_encoding = 'utf8'
default_decoding = 'utf8'
db = MySQLdb.connect("192.168.10.105","root","123a+-","12306")
cursor = db.cursor()
db.set_character_set('utf8')
#查询日期
date='2016-12-20'
#cui
xian = "-----------------------------------------------------"
xing = "*****************************************************"

def timetable():

    #获取表内第一行ID
    cursor.execute('select ID from TrainList limit 1')
    firstIDList = cursor.fetchall()
    #tableID = firstIDList[0][0]
    tableID = 7541
    #获取表内所有ID
    cursor.execute('select ID from TrainList')
    allID = cursor.fetchall()

    
    #url查询
    while(tableID <= allID[-1][0]):
        #打开一个文件用于记录已经采集过的车次
        tempFile = open('/home/derek/Code/Python/12306/temp.txt',"a+")
        temp = tempFile.read()
        #查询车次信息
        cursor.execute(r"select * from TrainList where ID = '%d'" % (tableID))
        trainNumInfo = cursor.fetchone()
        #查询出错则写入error文件
        if trainNumInfo == None:
            errorFile = open('/home/derek/Code/Python/12306/error.txt',"a+")
            errorFile.write(str(tableID) + ',\n')
            tableID += 1
            continue
        #print "车次信息：",trainNumInfo[1],trainNumInfo[2].decode('utf8'),trainNumInfo[3].decode('utf8')
        #print xian
        #获取列车No号字符串
        trainNoStr = trainNumInfo[4]
        #获取列车车次
        trainCodeStr = trainNumInfo[1]
        #解决一列车有多个车次的问题
        #临时文件做核实用，后面去掉
        trainNumFile = open('/home/derek/Code/Python/12306/train.txt',"a+")
        #临时文件结束
        lenCodeStr = len(trainCodeStr)
        #重复信息检测，在temp.txt文件中查找No号
        #根据车次长度来截取No号中对应部分来来检测是否为同一列车多个车次
        if lenCodeStr == 5:
            noCodeStr = trainNoStr[-7:-2]
            if noCodeStr != trainCodeStr:
                print "车次共用：",noCodeStr+'/'+trainCodeStr
                cursor.execute('insert into Code(CodeA,CodeB) values("%s","%s")'%(noCodeStr,trainCodeStr))
                db.commit()
            else:
                timetabledb(trainNoStr,trainNumInfo[2].decode('utf8'),trainNumInfo[3].decode('utf8'))
        elif lenCodeStr == 4:
            noCodeStr = trainNoStr[-6:-2] 
            if noCodeStr != trainCodeStr:
                print "车次共用：",noCodeStr+'/'+trainCodeStr
                cursor.execute('insert into Code(CodeA,CodeB) values("%s","%s")'%(noCodeStr,trainCodeStr))
                db.commit()
            else:
                timetabledb(trainNoStr,trainNumInfo[2].decode('utf8'),trainNumInfo[3].decode('utf8'))
        elif lenCodeStr == 3:
            noCodeStr = trainNoStr[-5:-2]
            if noCodeStr != trainCodeStr:
                print "车次共用：",noCodeStr+'/'+trainCodeStr
                cursor.execute('insert into Code(CodeA,CodeB) values("%s","%s")'%(noCodeStr,trainCodeStr))
                db.commit()
            else:
                timetabledb(trainNoStr,trainNumInfo[2].decode('utf8'),trainNumInfo[3].decode('utf8'))
        elif lenCodeStr == 2:
            noCodeStr = trainNoStr[-4:-2]
            if noCodeStr != trainCodeStr:
                print "车次共用：",noCodeStr+'/'+trainCodeStr
                cursor.execute('insert into Code(CodeA,CodeB) values("%s","%s")'%(noCodeStr,trainCodeStr))
                db.commit()
            else:
                timetabledb(trainNoStr,trainNumInfo[2].decode('utf8'),trainNumInfo[3].decode('utf8'))
        tableID += 1
    print 'done' 

def timetabledb(No,station,tostation):
    '12306时刻表查询'
    #查询始发站与终到站的电报码
    cursor.execute(r"select Telegraph from Station where Station = '%s'" % (station))
    sTeleCode = cursor.fetchone()
    print '始发站电报码：',sTeleCode[0]+'\n' + xian
    cursor.execute(r'select Telegraph from Station where Station = "%s"' % (tostation))
    tTeleCode = cursor.fetchone()
    print '终到站电报码：',tTeleCode[0]+'\n' + xian
    #合成查询地址
    url =  ("https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=%s" % (No,sTeleCode[0],tTeleCode[0],date))
    print '查询地址：'
    print url+'\n' + xian
    #抓取12306 json并解析
    data = urllib2.urlopen(url).read()
    jsonData = json.loads(data)
    keyList = jsonData.keys()
    rootData = jsonData['data']
    subData = rootData['data']
    i = 0
    while(i < len(subData)):
        if(i == 0):
            dbCode = subData[i]['station_train_code']
            print '车次：',dbCode
            dbType = subData[i]['train_class_name']
            print '列车等级：',dbType
            dbsStation = subData[i]['start_station_name']
            print '始发站：',dbsStation
        dbtoStation = subData[i]['station_name']
        print '车站名称：',dbtoStation
        dbA_Time =  subData[i]['arrive_time']
        print '到达时间：',dbA_Time
        dbD_Time = subData[i]['start_time']        
        if(dbA_Time == dbD_Time):
            dbD_Time = '-----'
        print '开车时间：',dbD_Time
        dbStationOrder = subData[i]['station_no']
        cursor.execute('insert into Train(Code,Type,Station,S_No,A_Time,D_Time) values("%s","%s","%s","%s","%s","%s")' % ( dbCode,dbType,dbtoStation,dbStationOrder,dbA_Time,dbD_Time ))
        db.commit()
        i += 1
    #print '抓取完成，等待2s'
    #time.sleep()
    

if __name__ == '__main__':
    timetable()