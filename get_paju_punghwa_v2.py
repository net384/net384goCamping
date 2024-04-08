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


##날짜 입력으로 seq 값 확인\\\
d = {}

try:
    with open("/root/script/get_paju_punghwa.in") as f:
        for line in f:
            (key, val) = line.split('=')
            d[str(key)] = val

    day1 = d.get('YYYY').rstrip('\r\n')+d.get('MM').rstrip('\r\n')+d.get('DD').rstrip('\r\n')

    ##날짜 조건절 체크 (오늘 보다 작으면 에러)
    
    YYYY = d.get('YYYY').rstrip('\r\n')
    MM = d.get('MM').rstrip('\r\n')
    DD = d.get('DD').rstrip('\r\n')

except FileNotFoundError:
    ##테스트 하는 경우
    day1 = "20240411"
    YYYY = "2024"
    MM = "04"
    DD = "11"
    pass

today = datetime.datetime.now().strftime('%Y%m%d')

print(day1)

if day1 <= today:
    print("예약 날짜("+today+")가 지났습니다. 프로그램을 종료 합니다.")
    sys.exit()


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

li_tags = resu1.select('li.s1, li.s2.zero, li.s3.zero, li.s4.zero, li.s5.zero, li.s6.zero, li.s7.zero, li.s8.zero')

for li in li_tags:
    a_tag = li.find('a')  # a 태그 찾기
    onclick_attr = a_tag['onclick']  # onclick 속성값 추출
    
    # onclick 속성값에서 필요한 데이터 추출
    # 정규 표현식 사용
    data = re.findall(r'f_SelectDateZone\((.*?)\);', onclick_attr)[0]
    
    # 데이터 정리
    data_list = [item.strip().strip('"') for item in data.split(',')]
    
    # a 태그 내의 span 태그 찾아서 제거
    span_tag = a_tag.find('span')
    if span_tag:
        span_tag.extract()
        
    # 결과 출력
    if day1 == data_list[0] and int(data_list[4]) > 0 :
        print(a_tag.text.strip()," == ",data_list)  # ["20240409", "CM000219", "SD60068", "2", "0"]
