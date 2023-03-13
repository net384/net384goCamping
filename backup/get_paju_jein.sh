#!/bin/bash

##examlple 
#./get_paju_jein.sh 2019 12 7
#./get_paju_jein.sh 21
# type is 20,21,22,23,24

##read configfile
. /root/script/get_paju_jein.in

ty=$1

ipput=data-date\=\"$dd\"
output=`curl -s "http://www.namastte.kr/popup.php?s=step01&t=resve&innb=5b7d0fe8da05f5b7d0fe8da0a1&Y=$yyyy&m=$mm&searchRoomTy=$ty" | grep $ipput | grep 'btn-select-room' | wc -l`

#debug output
#echo $yyyy $mm $dd "Type:"$ty

#echo $output
#result=`ssh -q $ipput /usr/bin/sar 1 1 | grep Aver  | awk '{print "%user="$3 ",%nice="$4 ",%system="$5 ",%iowait="$6 ",%steal="$7 ",%idle="$8}'`


echo "cam_paju_jein,host=paju-jein,sitelocation="$ty year="$yyyy",month="$mm",day="$dd",vacancy="$output"

