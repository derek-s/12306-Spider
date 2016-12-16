# -*- coding:utf8 -*-
#时刻表信息比较，用于了解调图内容
__anthor__ = 'Derek.S'

import MySQLdb
import csv
import string
import io
import os
from datetime import datetime

dbnew = MySQLdb.connect("192.168.10.105","root","123a+-","12306")
dbold = MySQLdb.connect("192.168.10.105","root","123a+-","PythonTest")

cursornew = dbnew.cursor()
cursorold = dbold.cursor()

dbnew.set_character_set('utf8')
dbold.set_character_set('utf8')


def stationChange():

    code = 'K1010'
    #code = 'C1001'
    cursornew.execute(r"select * from Train where `Code` = '%s'" % (code))
    trainInfoNew = cursornew.fetchall()

    cursorold.execute(r"select * from Train where `Code` = '%s'" % (code))
    trainInfoOld = cursorold.fetchall()
    
    
    stopNew = len(trainInfoNew)
    stopOld = len(trainInfoOld)

    i = 0
    z = 0
    x = 0
    y = 0
    
    newFlag = False
    oldFlag = False
    stationListN = []
    stationListO = []

    while i < stopNew:
        stationListN.append(trainInfoNew[i][3])
        i += 1
    while z < stopOld:
        stationListO.append(trainInfoOld[z][3])
        z += 1

    while x < len(stationListN):
        if stationListN[x] not in stationListO:
            print '新图增加停站:',stationListN[x],'到达时间：',trainInfoNew[x][5],' 开车时间：',trainInfoNew[x][6]
            newFlag = True
        x += 1
    while y < len(stationListO):
        if stationListO[y] not in stationListN:
            print '新图取消停站:',stationListO[y]
            oldFlag = True
        y += 1
    if(newFlag == False and oldFlag == False):
        print '停站无变化'
    
    a = 0
    while a < stopNew:
        stationName = stationListN[a]
        cursorold.execute(r"select * from Train where `Code` = '%s' and Station = '%s'" % (code,stationName))
        tableOldselct=cursorold.fetchall()
        cursornew.execute(r"select * from Train where `Code` = '%s' and Station = '%s'" % (code,stationName))
        tableNewselct=cursornew.fetchall()
        if(cursorold.rowcount != 0):
            if(tableOldselct[0][5] == '----'):
                if(tableNewselct[0][5] == '----'):
                    print stationName,' 始发站开车 ',timeCount(tableNewselct[0][6],tableOldselct[0][6])
            elif(tableNewselct[0][6] == '----'):
                print stationName,' 终点站 到达',timeCount(tableNewselct[0][5],tableOldselct[0][5])
            else:
                print stationName,' 到达 ',timeCount(tableNewselct[0][5],tableOldselct[0][5]),' 开车 ',timeCount(tableNewselct[0][6],tableOldselct[0][6])
        a += 1
    
    
def timeCount(a,b):
    timea = datetime.strptime(str(a),"%H:%M")
    timeb = datetime.strptime(str(b),"%H:%M")

    s = (timea-timeb).days

    if s == -1:
        t = (timeb-timea).seconds
        m = t / 60
        if m >= 60:
            h = t1 // 60
            m = (t % 3600) / 60
            return "提前%s小时%s分钟" % (h,m)
        return "提前%s分钟" % (m)
    elif s == 0:
        t = (timea-timeb).seconds
        if t == 0:
            return "时间不变"
        m = t / 60
        
        if m >= 60:
            h = t1 // 60
            m = (t % 3600) / 60
            return "延后%s小时%s分钟" % (h,m)
        return "延后%s分钟" % (m)



if __name__ == "__main__":
    
    stationChange()