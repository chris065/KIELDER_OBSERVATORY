#!/usr/bin/python3

import urllib3, certifi
from bs4 import BeautifulSoup
import json
import datetime

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

kObsCalURL = "https://kielderobservatory.org/our-events"

calPage = http.request('GET', kObsCalURL)
kObsCal = BeautifulSoup(calPage.data.decode('utf-8'), "html.parser")

with open("calendar.json", "w") as o:
    cal = kObsCal.find_all("div", id="component")[0]
    events = str(cal).split('[')[1].split(']')[0].strip()
    for id in ['id:', 'title:', 'start:', 'url:', 'showTime:', 'draggable:', 'className:', 'backgroundColor:', 'description:']:
        newID = '"' + id[:-1] + '":'
        events = events.replace(id, newID)
        events = events.replace("},{", "},\n{")
    #cal2 = kObsCal.find_all("script")
    o.write('[' + events + ']')

with open("calendar.json", "r") as i:
    iText = i.read()
    #print(iText)
    eventList = json.loads(iText)
    #print(eventList)
    #allEv = open('allEvents.json', 'w')
    #spacesEv = open('spacesEvents.json', 'w')
    for event in eventList:
        start = datetime.datetime.strptime(event['start'],"%Y-%m-%d %H:%M:%S")
        date = start.strftime("%d %b")
        time = start.strftime("%H:%M")
        if 'SOLD OUT:' in event['title']:
            places = 0
            title = event['title'].split('OUT:')[1].strip()
        elif 'Only ' in event['title']:
            title = event['title'].split("\n\r\n\rOnly ")[0].strip()
            places = str(event['title'].split("\n\r\n\rOnly ")[1])[0]
            places = int(places)
        else:
            title = event['title']
            places = 10
        print(date, time, title, places)
    #allEv.close()
    #spacesEv.close()

print('done')
