# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 10:25:02 2021

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

gs = c_GetCampDay.GetCampDay()
filename = os.path.split(sys.argv[0])[1].replace('.py','.in')

##날짜 입력으로 seq 값 확인\\\
#hostname = gs.hostname
DAYFILE = gs.CheckExecServer(gs.hostname,filename)
COOK_FILE = gs.GetCookieDir(gs.hostname,filename)
#print(COOK_FILE)

gs.ExecParserIn(DAYFILE)
gs.GetLastDay()

##캠핑 체크인 월 저장
checkinMonth = str(gs.day1[:6])
checkinMonthDay = str(gs.day1[:8])

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
gs.CheckBookDay(gs.day1,today,DAYFILE)
   
##SSL 경고 메시지 없애
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
      
      
#세션만들기
session=requests.session()
#로그인 하는 페이지의 general-requestURL에서 url 가져옴
url="https://camp.xticket.kr/web/main"

params = {'shopEncode' : '3ca13d7e35f571dd445d29950216553a5ece8a50aa56784c7a287e2f4f438131'} 
#가져오고 싶은 데이터 (form data)
headers1 = {'Accept-Encoding':'gzip, deflate, br',
           'Referer' : 'http://www.joongrangsoop.com/',
           'Host' : 'Host: camp.xticket.kr'
           } 


## allow_redirects=False 이 옵션이 중요함.
#  경우에 따라서 해당페이지에서 리다이렉션이 되는 것을 방지하고자 할때 allow_redirects 매개변수를 사용합니다
res = session.get(url,   params=params)

#redirect_cookie = res.headers['Set-Cookie']
#cookie = res.headers.get('Set-Cookie')

#print(res.text)

#위의 세션 객체 생성 후 아래 URL 호출하여 해당 날짜의 결과 값 도
url="https://camp.xticket.kr/Web/Book/GetBookProduct010001.json"
          
#가져오고 싶은 데이터 (form data)
#월 매개변수로 해당 월 잔여일자 한번에 가져오는 방식임.
data1={
'product_group_code': '0001',
'start_date': checkinMonthDay,
'end_date': checkinMonthDay,
'book_days': 1,
'two_stay_days': 0,
'shopCode': '214881968700',
}

headers1 = {'Accept-Encoding':'gzip, deflate, br',
           'Origin':'https://camp.xticket.kr',
           'Referer': 'https://camp.xticket.kr/web/main?shopEncode=3ca13d7e35f571dd445d29950216553a5ece8a50aa56784c7a287e2f4f438131',
           }         

## allow_redirects=False 이 옵션이 중요함.
#  경우에 따라서 해당페이지에서 리다이렉션이 되는 것을 방지하고자 할때 allow_redirects 매개변수를 사용합니다

res = session.post(url, data=data1, verify=False,headers=headers1 , allow_redirects=False)
#redirect_cookie = res.headers['Set-Cookie']
#cookie = res.headers.get('Set-Cookie')

#print(res.text[-100:])
#print(res.json())
#print(res.cookies)

result_f = res.json()

#print(result_f["data"]["bookPlayDateList"])
resutl_x = result_f["data"]["bookProductList"]

x = 0

for i in resutl_x:
    if i['select_yn'] != '0':
        #print(i['select_yn'],i['product_name'])
        x += 1

print('cam_jungrang year='+gs.day1[0:4]+',month='+gs.day1[4:6]+',day='+gs.day1[6:8]+',vacancy='+str(x))

            