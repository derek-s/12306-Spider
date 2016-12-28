# -*- coding:utf8 -*-
#test
__anthor__ = 'Derek.S'

import MySQLdb
import csv
import string
import io
import os
from datetime import datetime


with open('timechange.csv','ab+') as csvfile:
    if os.path.getsize('timechange.csv') == 0:
        csvwrite = csv.writer(csvfile,dialect='excel')
        csvwrite.writerow(['车次','新增停站','取消停站','站名','到达时间','到达时间变化','开车时间','开车时间变化','停站时间','停站时间变化','运行时间','运行时间变化','总计运行时间'])
        print '1111'    
            
    #inforead = csv.reader(csvfile,dialect='excel')
            
    #for row in inforead:
        #print row