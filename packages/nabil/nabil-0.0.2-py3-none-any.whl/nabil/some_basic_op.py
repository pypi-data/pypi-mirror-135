## Made for easy programming :)

## used modules ##
import os,sys 
import datetime 
from datetime import date
import re 
import time 
import requests
import webbrowser
import random 
from bs4 import BeautifulSoup 


## str upper function 
def u(str):
    return str.upper()

## str lower function 
def l(str): 
    return str.lower() 

## clear function 
def c():
    os.system("clear")

## date function
def today_date():
    return date.today()

## time start function 
def start():
    global s 
    s = time.time() 

## time stop function 
def stop():
    global st
    st = time.time() 

## total time count function 
def total_time():
    return int(st-s) 

## send get reuqests 
def send_req(url):
    try:
      return requests.get(url)
    except Exception as e:
        print(f"Requests error : {e}")
def get(url):
    return send_req(url)

## to print random number
def print_ran_num(x):
    return random.randint(1,x)

## retruning user value to the function 
def rannum(x):
    return print_ran_num(x)

## for reverse a string 
def reverse(str):
    return str[::-1]

## to open a url 
def url_open(url):
    return webbrowser.open(url)

## to open url in termux 
def url_open_termux(url):
    return os.system(f"xdg-open {url}")

## to figlet a text 
def figlet(text):
    return os.system(f"figlet {text}")

## sleep function 
def sleep(x):
    return time.sleep(x)

## text coloring function 
def color_manage(x,text):
    os.system("color")
    color_dict = {
       "red" : "\033[1;31m",
       "green" : "\033[1;32m",
       "yellow" : "\033[1;33m",
       "blue" : "\033[1;34m",
       "purple" : "\033[1;35m",
       "cyan" : "\033[1;36m",
       "white" : "\033[1;37m",
   }
    return color_dict[x]+str(text).strip(' ')


def color(x,text):
    return color_manage(x,text)
  

### for printing author info 
def author_info(name,git,fb):
    x = f"""\033[1;32m------------------------------------------   
\33[93m AUTHOR  : {name}
\33[93m GITHUB  : {git}
\33[93m FB      : {fb}
\033[1;32m------------------------------------------"""
    return print(x)

### for printing logo 

def logo(name,font):
    if font == "":
        font = "slant"
    req = requests.get(f"https://artii.herokuapp.com/make?text={name}&font={font}").text 
    return req   

## for chking internet connection 
def chk_con():
    url = "https://www.google.com"
    try:
       req = requests.get(url)
    except:
       print("No Internet Connection")
       sys.exit()

## get current tempertaure 
def temperature():
    search = "temperature now"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text,"html.parser")
    temp = data.find("div",class_="BNeawe").text 
    return temp 



