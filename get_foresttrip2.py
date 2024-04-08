import requests 
import re
import time
import datetime
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

area = {
        '인천/경기'		: {'_csrf': 'd7e59d7a-f836-45b7-a985-f56585ed3af1' , 'srchInsttArcd': 1},
        '강원'			: {'_csrf': 'd7e59d7a-f836-45b7-a985-f56585ed3af1' , 'srchInsttArcd': 2},
        '충북'			: {'_csrf': 'd7e59d7a-f836-45b7-a985-f56585ed3af1' , 'srchInsttArcd': 3},
        '전북'			: {'_csrf': 'd7e59d7a-f836-45b7-a985-f56585ed3af1' , 'srchInsttArcd': 5},
        '전남'			: {'_csrf': 'd7e59d7a-f836-45b7-a985-f56585ed3af1' , 'srchInsttArcd': 6},
        '대구/경북'		: {'_csrf': 'b40b2846-a44e-4b96-81b7-5bf8c9140501' , 'srchInsttArcd': 7},
        '부산/경남'		: {'_csrf': 'e122ef39-c336-4eca-b476-9f854f436683' , 'srchInsttArcd': 8},
        '제주'			: {'_csrf': 'a9f5b305-4658-4bf6-a516-e53d9409bc5c' , 'srchInsttArcd': 9},
        '대전/충남'		: {'_csrf': 'd7e59d7a-f836-45b7-a985-f56585ed3af1' , 'srchInsttArcd': 4},
        }


for i,val in area.items():
    #print("key = {key}, value={value}".format(key=i, value=val))
    #print('[Debug1]: ',i, area[i]['_csrf'], area[i]['srchInsttArcd'])
    #time.sleep(2)
    
    location = i
   
    #23.4.13 넷퍼넬 도입으로 인한 네퍼넬 키 요청 로직 추가
    nef_url = "https://nf.foresttrip.go.kr/ts.wseq?opcode=5101&nfid=0&prefix=NetFunnel.gRtype=5101;&sid=service_1&aid=action1&js=yes&1681360392254" 
    response = requests.get(nef_url, timeout=10)
    string = response.text
    #print(response.text)

    ## 넷퍼넬 콜백에서 난수 키값을 받아 온다.
    try:
        found = re.search('key=(.+?)&nwait', string).group(1)
        #print(found)
    except AttributeError:
        print("[01FC] Cann't find netfernel key value.")
        pass

    paramDict = {
        '_csrf': area[i]['_csrf'],
        'srchInsttArcd': area[i]['srchInsttArcd'] ,
        'srchInsttId': '',
        'srchRsrvtBgDt': day1,
        'srchRsrvtEdDt': day2,
        'srchStngNofpr': 2,
        'srchSthngCnt': 1,
        'srchWord': '',
        'netfunnel_key': found,
        'houseCampSctin': CampType, ## 01: 휴양관 02: 야영장
        'rsrvtPssblYn': '',
        'rsrvtWtngSctin': '01', 
        'srchHouseCharg': '',
        'srchCampCharg': '',
        'goodsClsscHouseCdArr': '',
        'goodsClsscCampCdArr': '',
        'srchInsttTpcd': '',
        'cmdogYn': 'N',
        'bbqYn': 'N',
        'dsprsYn': 'N',
        'otsdWeterYn': 'N',
        'wifiYn': 'N',
        'snowPlaceYn': 'N',
        'srchMyLtd': '',
        'srchMyLng': '',
        'srchDstnc': '',
        'gNowPage': 1,
        'srchGoodsId': '',
        'hmpgId': 'FRIP',
    }

    url = "https://www.foresttrip.go.kr/rep/or/fcfsRsrvtRcrfrDtlDetls.do" 
    
    response = requests.get(url, params=paramDict, timeout=10) 
    
    #print(response.status_code)​
    #print(response.url)
    #print(response.text.find('예약'))
    #print(response.text)
    
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        '''
        title = soup.select('b')
        for i in title:
            print(i.text)
            
        booking = soup.select('.ut_roomcount')    
        for i in booking:
            print(i.text)
        '''
        title = soup.select('b')
        booking = soup.select('.ut_roomcount') 
        for i,x in zip(title,booking):
            #sfe = str(i.text,'utf-8')
            #print(type(sfe))
            #print('[Debug2] : ' ,i.text,x.text)
            #print('cam_foresttrip,location='+ location.replace('/','') +',sitename='+ i.text.replace(']','').replace('[','').replace('(','').replace(')','')[:5] \
            print('cam_foresttrip,location='+ location.replace('/',':') +',sitename='+ i.text.replace(' ','') \
            + ' year='+day1[0:4]+',month='+day1[4:6]+\
            ',day='+day1[6:8]+',vacancy='+x.text.replace('예약가능 객실 수 : ',''))
    else : 
        print(response.status_code)
    
    #time.sleep(2)


