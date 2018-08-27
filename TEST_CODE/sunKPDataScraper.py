#
import urllib.request
import urllib
import datetime
import json, requests
#from PIL import Image
from subprocess import run

kpValue = ""
solarWindSpeedValue = ""
maxJsonvVal = 0
maxLinesInEnlil = 0


#get the current taime but just the hour part
#timeNow = datetime.datetime.now().time().hour


#url to the json files
kpData = "http://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
solarWindSpeedData = "http://services.swpc.noaa.gov/products/summary/solar-wind-speed.json"
enlilSimLinks = "http://services.swpc.noaa.gov/products/animations/enlil.json"
#get the json files
urlKP = requests.get(kpData)
urlSolarWind = requests.get(solarWindSpeedData)
urlEnlilSim = requests.get(enlilSimLinks)
#load the json files in a text format
kp = json.loads(urlKP.text)
swSpeed = json.loads(urlSolarWind.text)
enlil = json.loads(urlEnlilSim.text)
#count the lines in the JSON file and return the max amount
maxJsonvVal = sum(1 for line in kp)
maxLinesInEnlil = sum(1 for line in enlil)
#Because its an array it starts from 0 so have to minus one (not from the KP value)
kpValue = (kp[maxJsonvVal-1][1])
solarWindSpeedValue = (swSpeed['WindSpeed'])


for i in range(1, maxLinesInEnlil):
    #This will loop
    imgUrl = "http://services.swpc.noaa.gov/"+enlil[i]['url']
    enlilImg = urllib.request.urlretrieve(imgUrl, "IMG/enlil_"+str(i).zfill(3)+".jpg")
#    enlilImg = Image.open("IMG/enlil_"+str(i).zfill(3)+".jpg")
#    enlilImg.save("IMG/enlil_"+str(i).zfill(3)+".jpg")

run("ffmpeg -y -r 15 -f image2 -s 960x600 -i IMG/enlil_%03d.jpg -vcodec libx264 -crf 20 -pix_fmt yuv420p anim.mp4", shell=True)



#print("Kp Index: " + kpValue)
#print("Wind Speed: " + solarWindSpeedValue + " kms^-1")
