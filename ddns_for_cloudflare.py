#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This is a simple python script intended to update the DNS record on Cloudflare
# Currently,this script does 1 check on all dns records of 1 zone, which should be enough for personal use
# This script does not run continuously, please run this script using crontab or other sceheduler utility and create proper log files
# Before use, please modify the information in file config.json to ensure you get correct autherication

import requests
import json
from datetime import datetime

def obCurrentTime():
    return "["+str(datetime.now())+"] "

try:
    with open ("./config.json") as f:
        conf=json.loads(f.read())
except FileNotFoundError as e:
    print(obCurrentTime()+" Config file not found: "+str(e))

base_url=conf["base_url"]
zone_id=conf["zone_id"]
auth_mode=conf["auth_mode"]

def assHeader():
    if auth_mode=="token_auth":
        headers={
            "Authorization": "Bearer " + conf[auth_mode]["api_token"],
            "content-type": "application/json",
        }
    elif auth_mode=="key_auth":
        headers={
            "X-Auth-Email": conf[auth_mode]["email"],
            "X-Auth-Key": conf[auth_mode]["x_auth_key"]
        }
    else:
        raise ValueError("Invalid auth_mode")
    return headers

# obtain public IP address from https://api.ipify.org
def check_ip():
    try:
        res = requests.get("https://api.ipify.org")
        if res.status_code==200:
            return res.text
        else:
            raise ConnectionError("cannot obtain IP, response code:"+res.text)
    except Exception as e:
        print(obCurrentTime()+"Request error: "+str(e))    

def update_dns_record(ip):
    r = requests.get(
        base_url + "zones/" + zone_id + "/dns_records", headers=assHeader()
    ).json()

    if r["success"]:
        for record in r["result"]:
            record_id = record["id"]
            # record_type = record["type"]
            # name = record["name"]
            record_ip = record["content"]
            # ttl = record["ttl"]
            # proxied = record["proxied"]

            if record_ip != ip:
                # print("record_ip should be changed to " + ip)
                payLoad = {
                    "type": record["type"],
                    "name": record["name"],
                    "content": ip,
                    "ttl": record["ttl"],
                    "proxied": record["proxied"],
                }

                # try to update dns record for current record
                updateRes = requests.put(
                    base_url + "zones/" + zone_id + "/dns_records/" + record_id,
                    headers=assHeader(),
                    data=json.dumps(
                        payLoad
                    ),  # dumps payLoad before upload a json in body
                ).json()

                if updateRes["success"]:
                    print(
                        "["+ updateRes["result"]["modified_on"]+"] Record update success!"
                    )
                else:
                   raise ConnectionError("Record update failed! Errors:" + str(updateRes["errors"]))

            # only for testing
            else:
                print(obCurrentTime()+"ip didn't change, record_ip maintains: " + record_ip)
    # print for failures
    else:
        raise ConnectionError("Listing records failed! Errors:" + str(r["errors"]))

try:
    update_dns_record(check_ip())
except ConnectionError as cError:
    print(obCurrentTime()+str(cError))
except ValueError as vError:
    print(obCurrentTime()+str(vError))
except Exception as e:
    print(obCurrentTime()+"Error detected: "+str(e))