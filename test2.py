from random import seed
import requests

url = "https://stackoverflow.com/search?q=html+error+403"
session_obj = requests.Session()
response = session_obj.get(url, headers={"User-Agent": "Mozilla/5.0"})

print(response.status_code)


