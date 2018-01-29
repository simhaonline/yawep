#!/usr/bin/env python3
import requests
import json
import time
import config

url = "{}{}".format(config.key("url"),"/ftpaccounts")
username = config.key("username")
password = config.key("password")


while True:
 r = requests.get(url, auth=(username, password))
 print(r.status_code)
 if (r.status_code < 400):
  for x in r.json():
    print(x)
    print ("removing", x['id'],"domain = " ,x['domain_name'])
    x = requests.delete("%s/%s" % (url,x['id']), auth=(username, password))
    #for key in x.keys(): print(key)

 print ("Adding a new ftp account")
 y = requests.post(url, json = {"domain_id":"1" ,"username":"test1.ispbrasil.com.br","password":"x"}, auth=(username, password))
 print("pausing for 10secs")
 time.sleep(10)