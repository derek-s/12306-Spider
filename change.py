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
    cursornew.execute('select Code from TrainList') #select数据库内的车次数据
    codeListnew = cursornew.fetchall()
    for TrainCode in codeListnew:
        #根据车次查找车次信息
        cursornew.execute(r"select * from Train where `Code` = '%s'" % (TrainCode[0]))
        trainInfoNew = cursornew.fetchall()
        cursorold.execute(r"select * from Train where `Code` = '%s'" % (TrainCode[0]))
        trainInfoOld = cursorold.fetchall()

        stopNew = len(trainInfoNew)
        stopOld = len(trainInfoOld)
        #标志位
        i = 0
        z = 0
        x = 0
        y = 0

        newFlag = False
        oldFlag = False
        #停站变化处理
        stationListN = []
        stationListO = []
        stationListX = []
        print '车次：',TrainCode[0]
        while i < stopNew:
            stationListN.append(trainInfoNew[i][3])
            i += 1
        stationListX = stationListN[:]
        while z < stopOld:
            stationListO.append(trainInfoOld[z][3])
            z += 1
        while x < len(stationListN):
            
            if stationListN[x] not in stationListO:
                print '新图增加停站:',stationListN[x],'到达时间：',trainInfoNew[x][5],' 开车时间：',trainInfoNew[x][6]
                newFlag = True
                stationListX.remove(stationListN[x])
                csvwriteproc(TrainCode[0],stationListN[x],'','','','','','','','','','','')
            x += 1
            
        while y < len(stationListO):
            if stationListO[y] not in stationListN:
                print '新图取消停站:',stationListO[y]
                oldFlag = True
                csvwriteproc(TrainCode[0],'',stationListO[y],'','','','','','','','','','')
            y += 1
        if(newFlag == False and oldFlag == False):
            print '停站无变化'
        #站站时间处理
        a = 0
        while a < len(stationListX):
            stationName = stationListX[a]
            if a > 0:
                laststationName = stationListX[a-1]
            cursorold.execute(r"select * from Train where `Code` = '%s' and Station = '%s'" % (TrainCode[0],stationName))
            tableOldselct=cursorold.fetchall()
            cursornew.execute(r"select * from Train where `Code` = '%s' and Station = '%s'" % (TrainCode[0],stationName))
            tableNewselct=cursornew.fetchall()

            oldStartTime = tableOldselct[0][6]
            newStartTime = tableNewselct[0][6]
            oldToTime = tableOldselct[0][5]
            newToTime = tableNewselct[0][5]

            if (oldToTime == '----'):
                if (newToTime == '----'):
                    print stationName,' 始发站开车 ',timeCount(newStartTime,oldStartTime)
                    csvwriteproc(TrainCode[0],'','',stationName,'-----','-----',newStartTime,timeCount(newStartTime,oldStartTime),'','','','','')
            elif(newStartTime == '----'):
                cursorold.execute(r"select * from Train where `Code` = '%s' and Station = '%s'" % (TrainCode[0],laststationName))
                lastStationold = cursorold.fetchall()
                cursornew.execute(r"select * from Train where `Code` = '%s' and Station = '%s'" % (TrainCode[0],laststationName))
                lastStationew = cursornew.fetchall()
                runo = tztimeCount(lastStationold[0][6],oldToTime)
                runw = tztimeCount(lastStationew[0][6],newToTime)
                print stationName,' 终点站 到达',timeCount(newToTime,oldToTime)
                csvwriteproc(TrainCode[0],'','',stationName,newToTime,timeCount(newToTime,oldToTime),'-----','-----','','','','','')
            else:
                cursorold.execute(r"select * from Train where `Code` = '%s' and Station = '%s'" % (TrainCode[0],laststationName))
                lastStationold = cursorold.fetchall()
                cursornew.execute(r"select * from Train where `Code` = '%s' and Station = '%s'" % (TrainCode[0],laststationName))
                lastStationew = cursornew.fetchall()
                tz = tztimeCount(newToTime,newStartTime)
                tzo = tztimeCount(oldToTime,oldStartTime)
                runo = tztimeCount(oldToTime,lastStationew[0][6])
                runw = tztimeCount(newToTime,lastStationew[0][6])
                print stationName,' 到达 ',timeCount(newToTime,oldToTime),' 开车 ',timeCount(newStartTime,oldStartTime),' 停站 ',tz,'分钟',tztimeChage(tz,tzo)
                csvwriteproc(TrainCode[0],'','',stationName,newToTime,timeCount(newToTime,oldToTime),newStartTime,timeCount(newStartTime,oldStartTime),tz,tztimeChage(tz,tzo),'','','')

            a += 1



def timeCount(a,b):
    timea = datetime.strptime(str(a),"%H:%M")
    timeb = datetime.strptime(str(b),"%H:%M")

    s = (timea-timeb).days

    if s == -1:
        t = (timeb-timea).seconds
        m = t / 60
        if m >= 60:
            h = m // 60
            m = (t % 3600) / 60
            return "提前%s小时%s分钟" % (h,m)
        return "提前%s分钟" % (m)
    elif s == 0:
        t = (timea-timeb).seconds
        if t == 0:
            return "时间不变"
        m = t / 60
        
        if m >= 60:
            h = m // 60
            m = (t % 3600) / 60
            return "延后%s小时%s分钟" % (h,m)
        return "延后%s分钟" % (m)


def tztimeCount(a,b):
    timea = datetime.strptime(str(a),"%H:%M")
    timeb = datetime.strptime(str(b),"%H:%M")

    t = (timeb-timea).seconds
    m = t / 60

    return m

def tztimeChage(a,b):
    timea = datetime.strptime(str(a),"%M")
    timeb = datetime.strptime(str(b),"%M")

    if timea > timeb:
        t = (timea-timeb).seconds
        m = t / 60
        if t == 0:
            return "时间不变"
        else:
            return "增加%s分钟" % (m)
    else:
        t = (timeb-timea).seconds
        m = t / 60
        if t == 0:
            return "时间不变"
        else:
            return "缩短%s分钟" % (m)

def runchage(a,b):
    if a>b:
        return "增加%s分钟" % (a-b)
    elif(a-b)==0:
        return "时间不变"
    else:
        return "缩短%s分钟" % (b-a)
   

def csvwriteproc(code,addststaoion,delstation,stationame,
            totime,totimechage,startime,statimechage,stoptime,stoptimechage,
            runtime,runtimechage,totaltime):

    with open('timechange.csv','ab+') as csvfile:
        csvwrite = csv.writer(csvfile,dialect='excel')
        csvwrite.writerow([code,addststaoion,delstation,stationame,
                           totime,totimechage,startime,statimechage,stoptime,stoptimechage,
                           runtime,runtimechage,totaltime])




if __name__ == '__main__':
    if os.path.exists('timechange.csv') == False:
        csvwriteproc('车次','新增停站','取消停站','站名','到达时间','到达时间变化','开车时间','开车时间变化','停站时间','停站时间变化','运行时间','运行时间变化','总计运行时间')
    stationChange()