# -*- coding: utf-8 -*-
"""
Created on Thu May 27 09:21:09 2021

@author: net384
"""
import socket
import os
import sys
from datetime import datetime, timedelta
from dateutil import relativedelta



class GetCampDay:
    def __init__(self):
        self.result = 0
        self.hostname = socket.gethostname()

    def add(self, num):
        self.result += num
        return self.result
    
    def GetHostName(self, v_hostname):
        self.hostname = v_hostname
        return self.hostname
    
    def CheckExecServer(self,hostname,filename):
        if hostname == 'instance-20191108-1623-2388':
            self.DAYFILE = '/root/script/' + filename
        else:
            self.DAYFILE = filename            
        
        return self.DAYFILE
        
    def CheckBookDay(self,day1,today,DAYFILE):
        if  day1 <= today:
            print('예약 날짜 : ['+day1+'] 가 지났습니다. 설정파일 : ['+DAYFILE+ '] 프로그램을 종료 합니다.')
            sys.exit()          
        else :
            #print(day1, today) 
            pass
        
    def GetCookieDir(self,hostname,filename):
        self.filename1 = filename.replace('.in','_cookie.txt')
        
        if hostname == 'instance-20191108-1623-2388':
            self.COOKFILE = '/root/script/' + self.filename1
        else:
            self.COOKFILE = self.filename1          
        
        return self.COOKFILE
        
    def ExecParserIn(self,DAYFILE):
        try:
            d = {}
            with open(DAYFILE) as f:
                for line in f:
                    # 공백, '#', '\r', 또는 빈 라인은 무시합니다.
                    if line.startswith(' ') or line.startswith('#')  or line.startswith('\r') or line.startswith('\r\n')  or line.strip() == '':
                        continue                    
                    
                    (key, val) = line.split('=')
                    d[str(key)] = val.rstrip('\r\n')

            self.day1 = d.get('YYYY')+d.get('MM')+d.get('DD')
            self.days = int(d.get('DAYS'))
            self.CampType = d.get('CMPTP')
        except:
            print('파일이 없거나 권한이 불충분 합니다. 또는 파일에 #,빈공백 외 다른값이 존재합니다. 파일명 : [' + DAYFILE+ ']')
            print('프로그램을 종료 합니다.')
            sys.exit()
    
    def GetLastDay(self):
        self.now = datetime.today()
        #print("현재 시간:", now.strftime('%Y%m%d'))
         
        self.this_month_first = datetime(self.now.year, self.now.month, 1)
        #print("이번달 첫시간:", this_month_first.strftime('%Y%m%d'))

        self.next_month_first = self.this_month_first + relativedelta.relativedelta(months=1)
        #print("다음달 첫시간:", next_month_first.strftime('%Y%m%d'))
         
        self.this_month_last = self.next_month_first - timedelta(seconds=1)
        #print("이번달 마지막 시간:", this_month_last.strftime('%Y%m%d'))
        self.this_month_last = self.this_month_last.strftime('%Y%m%d')
        
        
        