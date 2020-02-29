#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This is a simple python script intended to update the DNS record on Cloudflare
# Currently,this script does 1 check on all dns records of 1 zone whose info listed as bellow, which should be enough for personal use
# This script does not run continuously, please run this script using crontab or other sceheduler utility and create proper log files
# Before use, please modify the information below to ensure you get correct autherication

import requests
import json

base_url = "https://api.cloudflare.com/client/v4/"

email = "your-email@email.com"
x_auth_key = "your_cloudflare_global_API_Key"
zone = "Zone_ID_of_your_domain_name"

base_headers = {
    "X-Auth-Email": email,
    "X-Auth-Key": x_auth_key,
    "content-type": "application/json",
}

# obtain public IP address from https://api.ipify.org
def check_ip():
    lookup_ip = requests.get(url="https://api.ipify.org?format=json").json()["ip"]
    return lookup_ip

def update_dns_record(ip):
    r = requests.get(
        base_url + "zones/" + zone + "/dns_records", headers=base_headers
    ).json()
    # with open("./dns_records.json","w") as f:  # for testing purpose
    #     f.write(r.text)
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

                # try to update dns record for current item
                updateRes = requests.put(
                    base_url + "zones/" + zone + "/dns_records/" + record_id,
                    headers=base_headers,
                    data=json.dumps(payLoad),  # dumps payLoad before upload a json in body
                ).json()

                if updateRes["success"]:
                    print(
                        "Record update success! Update at: "
                        + updateRes["result"]["modified_on"]
                    )
                else:
                    print("Record update failed! Errors:" + str(updateRes["errors"]))
            # else:   # only for testing
            #     print("ip didn't change, record_ip maintains " + record_ip)
    else:
        print("Listing records failed! Errors:" + r["errors"])

update_dns_record(check_ip())