import socket
import string
import json
import random
import requests
import json
def getipaddress():
    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)
    ipaddress=ipaddress.replace('.','-')
    return ipaddress
def gettheuserid():
    dta={}
    try:
        userid=getipaddress()
    except:
        userid="unknown"
    return userid
def check_login():
    try:
        headers = {'Content-type': 'application/json'}
        res=requests.post(url = "http://127.0.0.1:5000/check_login", data = json.dumps({}), headers=headers)
        res=json.loads(res.text)
        status=res["status"]
    except:
        status=False
    return status
    
def check_login_recursive():
    status=check_login()
    if(status==False):
        webbrowser.open('https://datakund.com/account/login', new=2)
        print("Please login in browser first to continue.....")
    while(True):
        status=check_login()
        if(status==True):
            break
    print("Logged in successfully..")
    