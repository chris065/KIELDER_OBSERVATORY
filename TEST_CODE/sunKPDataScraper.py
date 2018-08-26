import urllib.request
import urllib
import datetime
import json, requests

kpValue = ""
maxJsonvVal = 0

#get the current time but just the hour part
timeNow = datetime.datetime.now().time().hour

timeNowTest = datetime.datetime.now()
print(timeNowTest)

#url to the json file
kpData = "http://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
#get the json file
url = requests.get(kpData)
#load the json file in a text format
kp = json.loads(url.text)

kpValue = (kp[maxJsonvVal][1])

print("Kp Index: " + kpValue)
