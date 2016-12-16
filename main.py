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

from trainlist_process import trainlistProcess
from timetable import *


if __name__ == "__main__":
    
    trainlistProcess()
    #timetable()