
import requests
import json
#import datetime
import sys
import socket
import os
import time
from datetime import datetime
from dateutil.relativedelta import *
import urllib3

#ssl 인증서 오류 https://sun2day.tistory.com/226
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#day1 = "20201024"
##날짜 입력으로 seq 값 확인\\\
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

d = {}
with open(DAYFILE) as f:
    for line in f:
        (key, val) = line.split('=')
        d[str(key)] = val



#print (d)
#print(d.get('YYYY').rstrip('\r\n')+d.get('MM').rstrip('\r\n')+d.get('DD').rstrip('\r\n'))

day1 = d.get('YYYY').rstrip('\r\n')+d.get('MM').rstrip('\r\n')+d.get('DD').rstrip('\r\n')

#print(day1)

##다음달 마지막 일 구하기
today = datetime.today()

next_month_f = datetime(today.year, today.month,1) + relativedelta(months=2)
next_month_l = next_month_f + relativedelta(seconds=-1)
day2 = str(next_month_l.strftime('%Y%m%d'))
#print('조회일:' ,day1, '조회일기준 다음달 말일 :', next_month_l.strftime('%Y%m%d'))


##날짜 조건절 체크 (오늘 보다 작으면 에러)    
today = datetime.now().strftime('%Y%m%d')

if day1 <= today:
    print("예약 날짜("+today+")가 지났습니다. 프로그램을 종료 합니다.")
    sys.exit()

##요청 날짜의 시작일과 다음달 말일의 범위로 콜한다. 


dicv = {"22016459" : ["연천재인폭포오토캠핑장","cam_jaein_camp"],
        "21005592" : ["한탄강오토캠핑장","cam_hantan_camp"],  
        "22002652" : ["노을캠핑장","cam_noeul_camp"] , 
        "21012652" : ["천왕산가족캠핑장","cam_chunwang_camp"] , 
        "20003623" : ["구리토평가족캠핑장","cam_topeung_camp"] , 
        "20004468" : ["안성맞춤캠핑장","cam_ansung_camp"] , 
        "23001955" : ["시흥갯골캠핑장","cam_cyhungget_camp"] , 
        "22005895" : ["고양시킨텍스캠핑장","cam_kintax_camp"] , 
        "24000549" : ["노을진캠핑장 ","cam_noeuljin_camp"] , 
        "22005895" : ["인천대공원캠핑장","cam_inchenpark_camp"] , 
}

for sitecode in dicv:
    
    #url = "http://ticket.interpark.com/Ticket/Goods/GoodsInfoJSON.asp?Flag=UseCheckIn&GoodsCode=20003580&PlaceCode=20000297&PlayDate="+day1+"&Callback=fnPlayDateChangeCallBack"
    url = "https://api-ticketfront.interpark.com/v1/goods/"+sitecode+"/playSeq?endDate="+day2+"&goodsCode="+sitecode+"&page=1&pageSize=1550&preSale=false&startDate="+day1+""
    #a = {"Num":"1","PlaySeq":"126","PlayDate":"20201101","SeatYN":"N","BalanceSeatYN":"N","CancelableDate":"202010312359","OnlineDate":"20201028","BookingEndDate":"202010312359","NoOfTime":"1","PlayDateDisc":"1박 2일","PlaySeqList":"126","StartPlaySeq":"126"}
    
    proxy_srv = '110.12.211.14'
    proxy = {
    'http': 'http://'+proxy_srv+':80','https': 'http://'+proxy_srv+':80'
    #'https': 'https://username:password@proxy_server:proxy_port'
    }
    
    headers = {'Referer': 'https://tickets.interpark.com/',
               'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    
    print(url)

    res = requests.get(url,headers=headers, proxies=proxy, verify=False)
    #res = requests.get(url,headers=headers, verify=False)
    #print(response.status_code)

    print(res.text)
    
    
    a1 = res.text
    #replace_t1 = a1.replace("fnPlayDateChangeCallBack({\"JSON\":[", "[",1)
    #replace_t2 = replace_t1.replace("]});", "]",1)
    #print(replace_t2)
    #res.status_code

    #print(replace_t2)
    #print(json.loads(replace_t2))

    #결과의json 을 dict로 저장 처리
    sv1 = json.loads(a1)
    #print(sv1.get('data'))
    #sv2 = sv1.get('data')

    #print(sv1.get("data"))


    for i2 in sv1.get("data"):
        #{'playSeq': '016', 'playDate': '20220419', 'playTime': '1400', 'bookableDate': '202203100000', 'bookingEndDate': '202204191800', 'cancelableDate': '202204191800', 'remainSeat': None, 'casting': None, 'limitMaxStayDate': None, 'playSeqList': [{'stayPlaySeq': '016', 'stayDay': '1박2일'}, {'stayPlaySeq': '016,017', 'stayDay': '2박3일'}]}
        #print(i2.get('playDate') + ":" + i2.get('playSeq'))
        if i2.get('playDate') == day1:
            v_playseq = i2.get('playSeq')
            
    ## 2박 이라면 https://api-ticketfront.interpark.com/v1/goods/22002652/playSeq/PlaySeq/016,017/REMAINSEAT  사용 필요 
    #https://api-ticketfront.interpark.com/v1/goods/22002652/playSeq/PlaySeq/016/REMAINSEAT
    url2 = "https://api-ticketfront.interpark.com/v1/goods/"+sitecode+"/playSeq/PlaySeq/"+v_playseq+"/REMAINSEAT"
    headers2 = {'Referer': 'https://tickets.interpark.com/' , 'pragma': 'no-cache'}

    res2 = requests.get(url2,headers=headers2)
    #print(res2.text)
    a2 = res2.text

    sv2 = json.loads(a2)

    #print (sv2.get("data").get("remainSeat"))
    ix = sv2.get("data").get("remainSeat")

    for i3 in ix:
        #{'playSeq': '016', 'playDate': '20220419', 'playTime': '1400', 'bookableDate': '202203100000', 'bookingEndDate': '202204191800', 'cancelableDate': '202204191800', 'remainSeat': None, 'casting': None, 'limitMaxStayDate': None, 'playSeqList': [{'stayPlaySeq': '016', 'stayDay': '1박2일'}, {'stayPlaySeq': '016,017', 'stayDay': '2박3일'}]}
        #print(i3.get('seatGrade'),i3.get("seatGradeName")+"g"+str(i3.get("remainCnt")))
        #cam_noeulcamp,host=noeul-zone,sitelocation=zone평화 year=2020,month=10,day=17,vacancy=0
        print(''+sitecode,dicv[sitecode][1]+',host=noeul-zone,sitelocation='+str(i3.get("seatGradeName"))+' year='+day1[0:4]+',month='+day1[4:6]+ ',day='+day1[6:8]+',vacancy='+str(i3.get('remainCnt')))

    time.sleep(2)
    