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
from collections import Counter

#login_html = 'https://reservation.knps.or.kr/member/memberLogin.action'
#crawl_html = 'https://reservation.knps.or.kr/reservation/searchSimpleCampReservation.action'

gs = c_GetCampDay.GetCampDay()
filename = os.path.split(sys.argv[0])[1].replace('.py','.in')

#print (filename)
##날짜 입력으로 seq 값 확인\\\
#hostname = gs.hostname
DAYFILE = gs.CheckExecServer(gs.hostname,filename)
COOK_FILE = gs.GetCookieDir(gs.hostname,filename)
#print(DAYFILE)

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

#print(day1)  
##날짜 조건절 체크 (오늘 보다 작으면 에러)    
today = datetime.datetime.now().strftime('%Y%m%d')
#today = '20210815'
   
gs.CheckBookDay(gs.day1,today,DAYFILE)

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

resu1 = str(res.text)
resu2 = res.json()

#print(resu2['campList'])

for camptop1 in resu2['campGroupList'] :
    #print(f" campTop1 :  {camptop1}") # 대그룹 사이트 명
    campv = f"{camptop1}"
    #print ('top1' ,  campv)
    
    ##디버그 코드
    if campv != '디버깅 코드 라인 ':
    #if campv == '내장산':
        ##두번째 단계
        for camptop2, org_id in [(item['orgnzt_nm'],item['orgnzt_id']) for item in resu2['campList'] if item['orgnzt_parent_nm'] == campv]:
            #print('deptnm : ' ,camptop2 , 'orgnzt_id : ' , org_id  ) 
            
            site3 = []
            for item in resu2['campGubunList']:
                
                if item['DEPT_NM'] == camptop2:
                    #print("HRK_PRD_CTG_NM:", item['HRK_PRD_CTG_NM'])                    
                    site3.append(str(item['HRK_PRD_CTG_ID'])) 
                    
            site3 = ",".join(site3)
            #print (site3)            
            deptnm = camptop2
            
            url="https://reservation.knps.or.kr/reservation/campsite/campsites.do"
            data = {'prdSalStcd': 'N',
                        'period': daycount, #박수 최고 2박
                        'bgnDate': day1,    #체크인 날짜
                        'endDate': day2,    #체크아웃날짜
                        'deptId': org_id,   # 중그룹 사이트 코드 
                        'prdCtgIds': site3 ,   # 소그룹 사이트 코드
                    }
            #print(data) 
            #print(daycount)
            headers2 = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6',
                        'Connection': 'keep-alive',
                        'Content-Length': '94',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Host': 'reservation.knps.or.kr',
                        'Origin': 'https://reservation.knps.or.kr',
                        'Referer': 'https://reservation.knps.or.kr/',
                        }

            #쿠키 미사용
            res=requests.post(url, data=data, headers=headers2)
            #res.raise_for_status()

            lastval1 = str(res.text)
            lastval2 = res.json()
            code_nm2_values = [item["CODE_NM2"] for item in lastval2["avails"]]
            
            counter = list(Counter(code_nm2_values).items())
            
            for fval in counter:
                #print('사이트대그룹: ',camptop1,'사이트중그룹: ',deptnm,'사이트소그룹: ',fval[0], '자리: ' ,fval[1],'개 있음')
                print('cam_knps,location='+ camptop1 +',sitename1='+ deptnm +',sitename2='+ fval[0] +' year='+gs.day1[0:4]+',month='+gs.day1[4:6]+ \
                        ',day='+gs.day1[6:8]+',vacancy='+ str(fval[1]) + '')
                #cam_knps,location=가야산,sitename=자동차야영장 year=2023,month=09,day=21,vacancy=17
                      
            time.sleep(1)

            
