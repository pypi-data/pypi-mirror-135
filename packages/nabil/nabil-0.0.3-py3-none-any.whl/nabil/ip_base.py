import requests 
import json 
# get ip addreass
def ip():
    i = requests.get("https://api64.ipify.org/").text 
    return str(i)

## get location of ip addreass 
def country():
    i = requests.get("https://api64.ipify.org/").text 
    api = f"http://ip-api.com/json/{i}"
    req = requests.get(api).text 
    data = json.loads(req)
    return data['country']

## get city of ip addreass 
def city():
    i = requests.get("https://api64.ipify.org/").text 
    api = f"http://ip-api.com/json/{i}"
    req = requests.get(api).text 
    data = json.loads(req)
    return data['city']



