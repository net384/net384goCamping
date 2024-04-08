from random import seed
import requests

url = "https://api-ticketfront.interpark.com/v1/goods/22016459/playSeq?endDate=20240430&goodsCode=22016459&page=1&pageSize=1550&preSale=false&startDate=20240322"

proxy = {
'http': 'http://115.89.203.59:80',
'https': 'http://115.89.203.59:80'
#'https': 'https://username:password@proxy_server:proxy_port'
}
    
session_obj = requests.Session()
response = session_obj.get(url, headers={"User-Agent": "Mozilla/5.0"}, proxies=proxy, verify=False)

print(response.status_code)


