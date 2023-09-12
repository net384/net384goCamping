# -*- coding: utf-8 -*-
"""
@author: net384
"""
import c_GetCampDay 
import requests
import json
import sys
import re
from bs4 import BeautifulSoup as bs
import os
import datetime
import time


#login_html = 'https://reservation.knps.or.kr/member/memberLogin.action'
#crawl_html = 'https://reservation.knps.or.kr/reservation/searchSimpleCampReservation.action'

gs = c_GetCampDay.GetCampDay()
print ()
filename = os.path.split(sys.argv[0])[1].replace('.py','.in')

##날짜 입력으로 seq 값 확인\\\
#hostname = gs.hostname
DAYFILE = gs.CheckExecServer(gs.hostname,filename)
COOK_FILE = gs.GetCookieDir(gs.hostname,filename)
#print(COOK_FILE)

gs.ExecParserIn(DAYFILE)
gs.GetLastDay()

#print(gs.day1)
daycount = gs.days
#해당월 마이막 일자 가져오기
#print(gs.this_month_last)

##박수에 따라서 끝날짜 계산하기
dayadd = datetime.datetime.strptime(gs.day1,'%Y%m%d')  + datetime.timedelta(days=daycount)  
day2 = dayadd.strftime('%Y%m%d')

#print(day1)  
##날짜 조건절 체크 (오늘 보다 작으면 에러)    
today = datetime.datetime.now().strftime('%Y%m%d')
#today = '20210815'
'''
if gs.day1 <= today:
    print("예약 날짜("+gs.day1+")가 지났습니다. 프로그램을 종료 합니다.")
    sys.exit()
'''    
#gs.CheckBookDay(gs.day1,today,DAYFILE)

'''
data = {'areaCode' : area[i]['areaCode'] ,
        'rsrvtQntt': '',
        'rsrvtType': 'RSRVT',
        'checkYn': '',
        'index': 1,
        'elementPerPage': 50,
        'indexPerPage': 10,
        'hdnAvailDate': ''+gs.this_month_last+'',
        'hdnAvailStartDate': ''+ today +'',
        'hdnToday': ''+ today +'',
        'fclt': '',
        'selCnt': 3,
        'selArea': '',
        'period': 1,
        'sDate': '',
        'useBgnDtm': ''+gs.day1+'',
        'dprtmId': area[i]['dprtmId'],
        'fcltMdclsCd':  area[i]['fcltMdclsCd'],
    }
'''

#print(paramDict)

## 메인 크롤##############################################    
url="https://reservation.knps.or.kr/reservation/campsite/campList.do"



headers2 = {'Host': 'reservation.knps.or.kr',
                'Origin': 'https://reservation.knps.or.kr',
                'Referer': 'https://reservation.knps.or.kr/',
                'Content-Type': 'application/json;charset=UTF-8',}
#쿠키 재사용
res=requests.post(url,  headers=headers2) 

#쿠키 미사용
#res=requests.post(url, data=data, headers=headers2)
#res.raise_for_status()

#resu1 = str(res.text)
resu2 = res.json()

#print(resu2)

print(resu2['campGroupList'])
#soup = bs(resu1, 'html.parser')

