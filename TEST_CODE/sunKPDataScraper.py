import urllib.request
import urllib
import datetime
import json, requests

kpValue = ""
maxJsonvVal = 0

#get the current time but just the hour part
#timeNow = datetime.datetime.now().time().hour


#url to the json file
kpData = "http://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
#get the json file
url = requests.get(kpData)
#load the json file in a text format
kp = json.loads(url.text)
#count the lines in the JSON file and return the max amount
maxJsonvVal = sum(1 for line in kp)
#Because its an array it starts from 0 so have to minus one (not from the KP value)
kpValue = (kp[maxJsonvVal-1][1])

print("Kp Index: " + kpValue)
