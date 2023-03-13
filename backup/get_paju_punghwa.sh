#!/bin/bash

##examlple 
#./get_paju_jein.sh 2019 12 7
#./get_paju_jein.sh 21
# type is 20,21,22,23,24

##read configfile
. /root/script/get_paju_punghwa.in

ty=$1
ty="em class"

ipput=data-date\=\"$dd\"
#output=`curl -s "http://www.namastte.kr/popup.php?s=step01&t=resve&innb=5b7d0fe8da05f5b7d0fe8da0a1&Y=$yyyy&m=$mm&searchRoomTy=$ty" | grep $ipput | grep 'btn-select-room' | wc -l`
output=`curl -s imjingakcamping.co.kr/resv/res_01.html?checkdate=$yyyy-$mm-$dd | iconv -f euc-kr -t utf-8 | grep "$ty"`  

#output1=`./get_paju_punghwa.sh "em class" | sed 's/<\/em>/\n/g' | grep '평화캠핑존' | wc -l`

output1=`curl -s imjingakcamping.co.kr/resv/res_01.html?checkdate=$yyyy-$mm-$dd | iconv -f euc-kr -t utf-8 | grep "$ty" | sed 's/<\/em>/\n/g' | grep '평화캠핑존' | wc -l`
output2=`curl -s imjingakcamping.co.kr/resv/res_01.html?checkdate=$yyyy-$mm-$dd | iconv -f euc-kr -t utf-8 | grep "$ty" | sed 's/<\/em>/\n/g' | grep '힐링캠핑존' | wc -l`
output3=`curl -s imjingakcamping.co.kr/resv/res_01.html?checkdate=$yyyy-$mm-$dd | iconv -f euc-kr -t utf-8 | grep "$ty" | sed 's/<\/em>/\n/g' | grep '누리캠핑존' | wc -l`
output4=`curl -s imjingakcamping.co.kr/resv/res_01.html?checkdate=$yyyy-$mm-$dd | iconv -f euc-kr -t utf-8 | grep "$ty" | sed 's/<\/em>/\n/g' | grep '에코캠핑존' | wc -l`

#debug output
#echo $yyyy $mm $dd "Type:"$ty

#echo $output1

#result=`ssh -q $ipput /usr/bin/sar 1 1 | grep Aver  | awk '{print "%user="$3 ",%nice="$4 ",%system="$5 ",%iowait="$6 ",%steal="$7 ",%idle="$8}'`


echo "cam_paju_punghwa,host=paju-zone,sitelocation="zone평화 year="$yyyy",month="$mm",day="$dd",vacancy="$output1"
echo "cam_paju_punghwa,host=paju-zone,sitelocation="Zone힐링 year="$yyyy",month="$mm",day="$dd",vacancy="$output2"
echo "cam_paju_punghwa,host=paju-zone,sitelocation="Zone누리 year="$yyyy",month="$mm",day="$dd",vacancy="$output3"
echo "cam_paju_punghwa,host=paju-zone,sitelocation="Zone애코 year="$yyyy",month="$mm",day="$dd",vacancy="$output4"

