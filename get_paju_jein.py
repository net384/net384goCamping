# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 14:12:06 2020

@author: net384


site 
20 A1~A20
21 A21~A40
22 A41~A60
23 A61~A78
24 A89~A100

"""

import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
import sys
from ast import literal_eval
import socket
import os

#day1 = "20201024"
start = time.time()  # 시작 시간 저장

hostname = socket.gethostname()
filename = os.path.split(sys.argv[0])[1].replace('.py','.in')


##날짜 입력으로 seq 값 확인\\\
DAYFILE_LIVE = '/root/script/'+filename
DAYFILE_DEV = filename
hostname = socket.gethostname()

if hostname == 'instance-20191108-1623-2388':
    DAYFILE = DAYFILE_LIVE
else:
    DAYFILE = DAYFILE_DEV
    
#print(DAYFILE)
    
##날짜 입력으로 seq 값 확인\\\  
d = {}
with open(DAYFILE) as f:
    for line in f:
        (key, val) = line.split('=')
        d[str(key)] = val


day1 = d.get('YYYY').rstrip('\r\n')+d.get('MM').rstrip('\r\n')+d.get('DD').rstrip('\r\n')
#print(day1)

##날짜 조건절 체크 (오늘 보다 작으면 에러)
today = datetime.datetime.now().strftime('%Y%m%d')
YYYY = d.get('YYYY').rstrip('\r\n')
MM = d.get('MM').rstrip('\r\n')
DD = d.get('DD').rstrip('\r\n')


#ROOM1 = '20'
zone1 = 0
zone2 = 0
zone3 = 0
zone4 = 0
zone5 = 0


if day1 <= today:
    print("예약 날짜("+today+")가 지났습니다. 프로그램을 종료 합니다.")
    sys.exit()

rooms = [20,21,22,23,24]

for i in rooms:
    url = 'http://www.namastte.kr/popup.php?s=step01&t=resve&innb=5b7d0fe8da05f5b7d0fe8da0a1&Y='+YYYY+'&m='+MM+'&searchRoomTy='+str(i)+''
    headers = {'Referer': 'http://www.namastte.kr/popup.php?s=step01&t=resve&innb=5b7d0fe8da05f5b7d0fe8da0a1&Y='+YYYY+'&m='+DD+'&searchRoomTy='+str(i)+''}
    
    res = requests.get(url,headers=headers)
    
    #raw = res.text
    
    soup1 = BeautifulSoup(res.content, 'html.parser')
    
    #print(soup1)
    #print(soup1.select('.btn-select-room'))
    #print(soup1.select_one('.btn-select-room'))
    #print(soup1.select_one('.btn-select-room').get_text())
    #print(soup1.select_one('div.btn-select-room '))
    
    '''
    select_v1 = soup1.select('div.btn-select-room')
    
    #get함수이용
    for title in select_v1:
        if title.get('data-date') == DD:
            #print(title.get('data-date'),title.get_text() )
            #print(DD)
            if str(i) == '20':
                #print('a')
                zone1 += 1
            elif str(i) ==  '21':
                zone2 += 1
            elif str(i) ==  '22':
                zone3 += 1
            elif str(i) ==  '23':
                zone4 += 1
            elif str(i) ==  '24':
                zone5 += 1
    #time.sleep(0.5)
    '''
    
    
    ##개선 버전 (조건절 속성을 추가하여 루프 횟수를 감소시킴)
    select_v1 = soup1.find_all("div", class_='btn-select-room', attrs={"data-date": DD})
    
    for title in select_v1:
        #print(title.get('data-date'),title.get_text() )
        #print(DD)
        if str(i) == '20':
            #print('a')
            zone1 += 1
        elif str(i) ==  '21':
            zone2 += 1
        elif str(i) ==  '22':
            zone3 += 1
        elif str(i) ==  '23':
            zone4 += 1
        elif str(i) ==  '24':
            zone5 += 1
    
    
    
    
print('cam_paju_jein,host=paju-jein,sitelocation=A1_A20 year='+YYYY+',month='+MM+',day='+DD+',vacancy='+str(zone1)+'')
print('cam_paju_jein,host=paju-jein,sitelocation=A21~A40 year='+YYYY+',month='+MM+',day='+DD+',vacancy='+str(zone2)+'')
print('cam_paju_jein,host=paju-jein,sitelocation=A41~A60 year='+YYYY+',month='+MM+',day='+DD+',vacancy='+str(zone3)+'')
print('cam_paju_jein,host=paju-jein,sitelocation=A61~A78 year='+YYYY+',month='+MM+',day='+DD+',vacancy='+str(zone4)+'')
print('cam_paju_jein,host=paju-jein,sitelocation=A89~A100 year='+YYYY+',month='+MM+',day='+DD+',vacancy='+str(zone5)+'')

#print("time :", time.time() - start) 