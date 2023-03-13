#!/bin/bash

curl -s -H "content=text/html" -H "charset=euc-kr" -d "location=002&wh_year=2019&man=503&wh_month=11" -X POST https://chukryong.gg.go.kr:455/reservation.asp | iconv -f euc-kr -t utf-8 
