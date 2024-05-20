# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 14:12:06 2020

@author: net384

변경 날짜 : 23.3.13 코드 수정
            다시 체크
"""

import requests
import re
import json
import datetime
import sys
from ast import literal_eval
from bs4 import BeautifulSoup
import sys
import c_GetCampDay 
import os


gs = c_GetCampDay.GetCampDay()
filename = os.path.split(sys.argv[0])[1].replace('.py','.in')

##날짜 입력으로 seq 값 확인\\\
hostname = gs.hostname
DAYFILE = gs.CheckExecServer(gs.hostname,filename)
COOK_FILE = gs.GetCookieDir(gs.hostname,filename)
#print(filename)

gs.ExecParserIn(DAYFILE)
gs.GetLastDay()

#print(gs.day1)
daycount = gs.days
#해당월 마이막 일자 가져오기
#print(gs.this_month_last)

##박수에 따라서 끝날짜 계산하기
dayadd = datetime.datetime.strptime(gs.day1,'%Y%m%d')  + datetime.timedelta(days=daycount)  
day2 = dayadd.strftime('%Y%m%d')
day1 = gs.day1
CampType = gs.CampType

#print(day1)  
##날짜 조건절 체크 (오늘 보다 작으면 에러)    
today = datetime.datetime.now().strftime('%Y%m%d')
#today = '20210815'
   
gs.CheckBookDay(gs.day1,today,DAYFILE)
YYYY=gs.day1[:4]
MM=gs.day1[4:6]
DD=gs.day1[6:]

#print ('yyyy:',YYYY , 'mm:',MM ,'dd:', DD)
#print(gs.day1)

url="https://forest.maketicket.co.kr/camp/reserve/calendar.jsp"

data = {
    'idkey': '5M4400',
    'gd_seq': 'GD123',
    'yyyymmdd': ''+day1+'',
    'sd_date': ''+day1+'',
}

headers2 = {'Host': 'forest.maketicket.co.kr',
                'Origin': 'https://forest.maketicket.co.kr',
                'Referer': 'https://forest.maketicket.co.kr/ticket/GD123',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',}
#쿠키 재사용
res=requests.post(url,  headers=headers2, data=data) 

#쿠키 미사용
#res=requests.post(url, data=data, headers=headers2)
#res.raise_for_status()

resu1 = BeautifulSoup(res.text, 'html.parser')
#print(resu1)
#resu2 = res.json()
#print(resu2)


li_tags = resu1.select('li.s1, li.s2, li.s3, li.s4, li.s5, li.s6, li.s7, li.s8')

#print(li_tags)


for li in li_tags:
    a_tag = li.find('a')  # a 태그 찾기
    onclick_attr = a_tag['onclick']  # onclick 속성값 추출
    
    # onclick 속성값에서 필요한 데이터 추출
    # 정규 표현식 사용
    data = re.findall(r'f_SelectDateZone\((.*?)\);', onclick_attr)[0]
    #print(data)
    # 데이터 정리
    data_list = [item.strip().strip('"') for item in data.split(',')]
    
    # a 태그 내의 span 태그 찾아서 제거
    span_tag = a_tag.find('span')
    if span_tag:
        span_tag.extract()
    
    #print(a_tag.text.strip()," == ",data_list)
        
    # 결과 출력
    ''' 일반캠핑 A존, 일반캠핑 A존, 오토캠핑만  출력 
            일반캠핑 A존  ==  ['20240418', 'CM000214', 'SD60077', '1', '19']
            일반캠핑 B존  ==  ['20240418', 'CM000219', 'SD60077', '2', '7']
            타프존  ==  ['20240418', 'CM000215', 'SD60077', '3', '4']
            오토캠핑  ==  ['20240418', 'CM000216', 'SD60077', '4', '22']
            카라반 D존  ==  ['20240418', 'CM000217', 'SD60077', '5', '10']
            카라반 M존  ==  ['20240418', 'CM000220', 'SD60077', '6', '3']
            카라반 Z존  ==  ['20240418', 'CM000221', 'SD60077', '7', '5']
            글램핑  ==  ['20240418', 'CM000218', 'SD60077', '9', '1']
    '''
    
    if day1 == data_list[0] and int(data_list[4]) > 0 and (data_list[1] == 'CM000214' or data_list[1] == 'CM000219' or data_list[1] == 'CM000216'):
        #print('cam_paju_punghwa,host=paju-zone,sitelocation=Zone애코 year='+YYYY+',month='+MM+',day='+DD+',vacancy='+str(cnt4)+'')
        #print(a_tag.text.strip()," == ",data_list)  # ["20240409", "CM000219", "SD60068", "2", "0"]
        
        site = a_tag.text.strip().replace(" ", "")
        print(f'cam_paju_punghwa,host=paju-zone,sitelocation={site} year={YYYY},month='+MM+',day='+DD+',vacancy='+data_list[4]+'')
        
        
        
        
         