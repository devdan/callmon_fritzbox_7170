import urllib3
import xml.etree.ElementTree as ET
import hashlib
from urllib.parse import urlparse
from urllib.parse import parse_qs
from requests import Session
import csv
from time import sleep
import mailer
import settings

def get_md5_hash(challenge, password):
    hash_me = (challenge + "-" + password).encode("UTF-16LE")
    hashed = hashlib.md5(hash_me).hexdigest()
    return challenge + "-" + hashed

def get_session_id():
    session = Session() 

    http = urllib3.PoolManager()
    data = http.request("get", settings.fritz_url + "/login_sid.lua").data

    tree = ET.fromstring(data)
    sid = tree.findtext("SID")

    if(sid == "0000000000000000"):
        challenge = tree.findtext("Challenge")   
        data = { "response": get_md5_hash(challenge, settings.fritz_pw)}     
        ret = session.post( settings.fritz_url + "/login.lua", data, allow_redirects=False)
        location = ret.headers['Location']

        parsed_url = urlparse(location)
        sid = parse_qs(parsed_url.query)['sid'][0]

    return sid

def remove_header(call_list):
    del call_list[:3]
    return call_list

def only_keep_first_x_rows(call_list):
    return call_list[0:settings.number_of_rows_to_keep]


def get_call_list_as_csv():
    sid = get_session_id()
    call_list_csv_url = settings.fritz_url + "/cgi-bin/webcm?sid=" + sid + "&getpage=../html/de/FRITZ!Box_Anrufliste.csv"
    home_url = settings.fritz_url + "/home/home.lua?sid=" + sid

    http = urllib3.PoolManager()
    # This page needs to be retrieved to update the csv file inside the box
    http.request("get", home_url)
    sleep(10)
    response = http.request("get", call_list_csv_url).data
    call_list_as_csv = response.decode("utf-8-sig")

    reader = csv.reader(call_list_as_csv.split("\n"), delimiter=';')
    call_list = list(reader)
    call_list = remove_header(call_list)

    call_list = list(filter(filter_missed_calls, call_list))
    
    call_list = only_keep_first_x_rows(call_list)
    
    return call_list


def send_missed_calls(old_call_list, new_call_list):
    for new_call in new_call_list:
        is_contained = False
        for old_call in old_call_list:
            if old_call[1] == new_call[1]:
                is_contained = True
        if not is_contained:
            call_time = new_call[1]
            caller = new_call[3]
            mailer.send_email(caller, call_time)

def filter_missed_calls(call):
    return len(call) > 0 and call[0] == "2"

# main

old_call_list = list()
call_list = list()

while (True):    
    call_list = get_call_list_as_csv()
    if len(call_list) < 2:
        sleep(settings.sleep_time_between_pulls_in_minutes * 60)
        continue

    if old_call_list:
        send_missed_calls(old_call_list, call_list)

    old_call_list = call_list

    sleep(settings.sleep_time_between_pulls_in_minutes * 60)
