#!/bin/bash


#curl -s "http://ticket.interpark.com/Ticket/Goods/GoodsInfoJSON.asp?Flag=UseCheckIn&GoodsCode=20003580&PlaceCode=20000297&PlayDate=20201101&Callback=fnPlayDateChangeCallBack" -H "Referer: http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode=20003580" | iconv -f euc-kr -t utf-8


#curl -s "http://ticket.interpark.com/Ticket/Goods/GoodsInfoJSON.asp?Flag=RemainSeat&GoodsCode=20003580&PlaceCode=20000297&PlaySeqList=123&CampingYN=Y&Callback=fnPlaySeqChangeCallBack" -H "Referer: http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode=20003580" | iconv -f euc-kr -t utf-8


output1=`curl -s "http://ticket.interpark.com/Ticket/Goods/GoodsInfoJSON.asp?Flag=UseCheckIn&GoodsCode=20003580&PlaceCode=20000297&PlayDate=20201101&Callback=fnPlayDateChangeCallBack" -H "Referer: http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode=20003580" | iconv -f euc-kr -t utf-8`

output2=`curl -s "http://ticket.interpark.com/Ticket/Goods/GoodsInfoJSON.asp?Flag=RemainSeat&GoodsCode=20003580&PlaceCode=20000297&PlaySeqList=123&CampingYN=Y&Callback=fnPlaySeqChangeCallBack" -H "Referer: http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode=20003580" | iconv -f euc-kr -t utf-8`


echo $output1

echo $output2
