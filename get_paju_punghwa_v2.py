# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 14:12:06 2020

@author: net384

변경 날짜 : 23.3.13 코드 수정
            다시 체크
"""

import requests
import json
import datetime
import sys
from ast import literal_eval

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
    'yyyymmdd': '20240408',
    'sd_date': '20240408',
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

resu1 = str(res.text)
print(resu1)
#resu2 = res.json()
