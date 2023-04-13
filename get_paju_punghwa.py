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
    day1 = "20230509"
    YYYY = "2023"
    MM = "05"
    DD = "09"
    pass

today = datetime.datetime.now().strftime('%Y%m%d')

#print(day1)

if day1 <= today:
    print("예약 날짜("+today+")가 지났습니다. 프로그램을 종료 합니다.")
    sys.exit()


#url = 'https://imjingakcamping.co.kr/resv/res_01_calendar.php?year='+YYYY+'&month='+MM+'&day='+DD+' '
#headers = {'Referer': 'https://imjingakcamping.co.kr/resv/res_01.html?checkdate='+YYYY+'-'+MM+'-'+DD+''}

url = 'https://imjingakcamping.co.kr/module/reserv21/res_01_calendar.php?year='+YYYY+'&month='+MM+'&day='+DD+' '
headers = {'Referer': 'https://imjingakcamping.co.kr/module/reserv21/res_01.html?checkdate='+YYYY+'-'+MM+'-'+DD+''}


#print(url)
#print(headers)
#http://imjingakcamping.co.kr/resv/res_01.html?checkdate=2021-05-13

res = requests.get(url,headers=headers)
#print(res.status_code)

#print(res.text)

val1 = res.text

#print('string type: {}'.format(type(val1)))
#print(val1.replace(':true,',':\'true\','))
val2 = val1.replace(':true,',':\'true\',')
dict1 = literal_eval(val2)
dict2 = dict1['result']
##딕셔너리 타입 안의 딕셔너리 형 데이터만 추출한다.
#print(dict1['result'])

'''
ph_a_ : 평화캠핑존
hl_ : 힐링캠핑존
nr_ : 누리캠핑존
ec_b : 에코캠핑존    

output : 

cam_paju_punghwa,host=paju-zone,sitelocation=zone평화 year=2020,month=05,day=01,vacancy=0
cam_paju_punghwa,host=paju-zone,sitelocation=Zone힐링 year=2020,month=05,day=01,vacancy=0
cam_paju_punghwa,host=paju-zone,sitelocation=Zone누리 year=2020,month=05,day=01,vacancy=0
cam_paju_punghwa,host=paju-zone,sitelocation=Zone애코 year=2020,month=05,day=01,vacancy=0

'''
cnt1 = 0
cnt2 = 0
cnt3 = 0
cnt4 = 0

for a1,a2 in dict2.items():
    if a1[:4] =='ph_a' and a2 == '0':        
        #print(a1,' : ',a2)
        cnt1 += 1
        #print(cnt1)
    elif a1[:3] =='hl_' and a2 == '0' :
        #print(a1,' : ',a2)
        cnt2 += 1
        #print(a2)
    elif a1[:3] =='nr_' and a2 == '0':
        #print(a1,' : ',a2)
        cnt3 += 1
    elif a1[:4] =='ec_b' and a2 == '0':
        #print(a1,' : ',a2)
        cnt4 += 1
    
print('cam_paju_punghwa,host=paju-zone,sitelocation=zone평화 year='+YYYY+',month='+MM+',day='+DD+',vacancy='+str(cnt1)+'')
print('cam_paju_punghwa,host=paju-zone,sitelocation=Zone힐링 year='+YYYY+',month='+MM+',day='+DD+',vacancy='+str(cnt2)+'')
print('cam_paju_punghwa,host=paju-zone,sitelocation=Zone누리 year='+YYYY+',month='+MM+',day='+DD+',vacancy='+str(cnt3)+'')    
print('cam_paju_punghwa,host=paju-zone,sitelocation=Zone애코 year='+YYYY+',month='+MM+',day='+DD+',vacancy='+str(cnt4)+'')

'''
a1 =res.text
replace_t1 = a1.replace("fnPlayDateChangeCallBack({\"JSON\":[", "[",1)
replace_t2 = replace_t1.replace("]});", "]",1)
print(replace_t2)
#res.status_code

#print(replace_t2)
print(json.loads(replace_t2))
'''


'''
sv1 = json.loads(replace_t2)

##복수의 날짜가 나오는경우는 조회 날짜만 나와야 함.1 박 2일 기준임
#print(sv1.get('PlaySeq'))
for i in sv1:
    if i.get('PlayDate') == day1:
        #print(i.get('PlayDate'),i.get('PlaySeq'))
        day_f = i.get('PlaySeq')

## 위에 가져온 playseq를 이용하여 날자를 매개변수로 받는다.
url2 = "http://ticket.interpark.com/Ticket/Goods/GoodsInfoJSON.asp?Flag=RemainSeat&GoodsCode=20003580&PlaceCode=20000297&PlaySeqList="+day_f+"&CampingYN=Y&Callback=fnPlaySeqChangeCallBack"
headers2 = {'Referer': 'http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode=20003580'}

res2 = requests.get(url2,headers=headers2)
#print(res2.text)

a2 =res2.text
replace2_t1 = a2.replace("fnPlaySeqChangeCallBack({\"JSON\":[", "[",1)
replace2_t2 = replace2_t1.replace("]});", "]",1)


#print(replace2_t2)

sv2 = json.loads(replace2_t2)

for i in sv2:
    #if int(i.get('RemainCnt')) > 0 :
    print('cam_noeulcamp,host=noeul-zone,sitelocation='+i.get('SeatGradeName')+' year='+day1[0:4]+',month='+day1[4:6]+\
              ',day='+day1[6:8]+',vacancy='+i.get('RemainCnt'))
'''
'''
cam_noeulcamp,host=noeul-zone,sitelocation=zone평화 year=2020,month=10,day=17,vacancy=0
'''