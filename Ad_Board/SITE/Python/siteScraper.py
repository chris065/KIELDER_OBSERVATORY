import ephem as e
import datetime
import pytz
import json, requests, urllib
from io import BytesIO
#from nasa import maas
from bs4 import BeautifulSoup
#from html_table_extractor.extractor import Extractor
import csv

import json, requests
import urllib
from PIL import Image
import time

currentWeatherPeriod = 0
phaseName = ""
observation = ""
auToKm = 149600000

weatherCodeDesc = ["Clear Night", "Sunny Day", "Partly Cloudy (Night)", "Partly Cloudy (Day)", "Not Used",
                   "Mist","Fog", "Cloudy", "Overcast", "Light Rain Shower (Night)", "Light Rain Shower (day)",
                   "Drizzle", "Light Rain", "Heavy Rain Shower (Night)", "Heavy Rain Shower (Day)", "Heavy Rain",
                   "Sleet Shower (Night)", "Sleet Shower (Day)", "Sleet", "Hail Shower (Night)", "Hail Shower (Day)",
                   "Hail", "Heavy Snow Shower (Night)", "Heavy Snow Shower (Day)", "Heavy Snow", "Thunder Shower (Night)",
                   "Thunder Shower (Day)", "Thunder"]

diff = 0

def getMoonPhaseName(phasePercentage):
    if phasePercentage < 2:
        phaseName = "New Moon"
    elif phasePercentage < 45:
        phaseName =  moonStatus + " Crescent"
    elif phasePercentage < 55:
        phaseName = "Half Moon"
    elif phasePercentage < 98:
        phaseName = moonStatus + " Gibbous"
    else:
        phaseName = "Full Moon"

    return phaseName

def getTimeDiff():

    #Convert the times to time stamps
    moon_ts = time.mktime(moonset.timetuple())
    sun_ts = time.mktime(sunset.timetuple())

    diff = int(sun_ts - moon_ts) / 60

    if diff > 60 or diff < -60:
        if diff < -60:
            diff = abs(diff)
        diff = float(diff) / 60
        diff = round(diff, 1)
        diff = str(diff) + " hours"
    else:
        if diff < 0:
            diff = abs(diff)
        diff = round(diff, 1)
        diff = str(diff) + " minutes"

    #print(diff)

    return diff

tableData = ""

#get the events json file
with open("events.json", "r") as read_file:
    events = json.load(read_file)
    for x, line in enumerate(events["allEv"]):
        if(str(events["allEv"][x]["places"]) == "0"):
            tableData = tableData + "<tr style='color: #707070'><td>"+str(events["allEv"][x]["date"])+", "+str(events["allEv"][x]["time"])+"</td><td>"+str(events["allEv"][x]["title"])+"</td><td>"+str(events["allEv"][x]["places"])+"</td></tr>"
        else:
            tableData = tableData + "<tr><td>"+str(events["allEv"][x]["date"])+", "+str(events["allEv"][x]["time"])+"</td><td>"+str(events["allEv"][x]["title"])+"</td><td>"+str(events["allEv"][x]["places"])+"</td></tr>"
    #print(tableData)

# Key definition for moonrise/set table
def takeSecond(elem):
    return elem[1]

datestr = ""
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

if (today.year == tomorrow.year):
    if (today.month == tomorrow.month):
        datestr = today.strftime("%d") + " - " + tomorrow.strftime("%d") + " " + today.strftime("%B %Y")
    else:
        datestr = today.strftime("%d %b") + " - " + tomorrow.strftime("%d %b") + " " + today.strftime("%Y")
else: # Date is 31/12
    datestr = today.strftime("%d %b %y") + " - " + tomorrow.strftime("%d %b %y")
#print (datestr)


#What the temperature feels like (Units: °C)
feelLikeTemp = ""
#What the temperature actually is (Units: °C)
temp = ""
#percipitation probablity  (Units: %)
precip = ""
#The condition code that will corespond to the correct description
weatherCode = ""

#making the BST timezone object
gb = pytz.timezone('Europe/London')

obsLat = '55.232302'
obsLon = '-2.616033'

#Setting the OBSERVATORY as the Observer
obs = e.Observer()

obs.lat, obs.lon = obsLat, obsLon
obs.date = datetime.datetime.utcnow()

# Get Moon phase info here as time will be changed for Moonrise/set times
moon = e.Moon()
moon.compute(obs)
# Illumination (%):
moonPhase = moon.moon_phase
moonPhase = round((moonPhase * 100), 1)
moonPhase = str(moonPhase)
# Determine Lunation and pick out Phase Image from List
nnm = e.next_new_moon(obs.date)
pnm = e.previous_new_moon(obs.date)
nfm = e.next_full_moon(obs.date)
pfm = e.previous_full_moon(obs.date)

lunation=(obs.date-pnm)/(nnm-pnm)

if (lunation < 0.5):
	moonStatus = 'Waxing'
else:
	moonStatus = 'Waning'

fileno = int(lunation*713)

moonlist=open("../IMG/moonframes/aa_filelist.txt", "r")
for c, line in enumerate(moonlist):
	#print(c, value)
	if (c ==fileno):
		phase = line
		break
moonlist.close()

pfm = pfm.datetime().replace(tzinfo=pytz.utc)
pfm = pfm.astimezone(tz=gb)
lastFullMoonDate = pfm.strftime("%d %b")
lastFullMoonTime = pfm.strftime("%H:%M:%S %Z")

nnm = nnm.datetime().replace(tzinfo=pytz.utc)
nnm = nnm.astimezone(tz=gb)
nextNewMoonDate = nnm.strftime("%d %b")
nextNewMoonTime = nnm.strftime("%H:%M:%S %Z")


#Sun values
sunset = obs.next_setting(e.Sun())
# Change Time to Sunset to get Moon times and next sunrise
# Note this forces the Sunset time to be the earliest time returned
obs.date = sunset

sunset = sunset.datetime().replace(tzinfo=pytz.utc)
sunrise = obs.next_rising(e.Sun()).datetime().replace(tzinfo=pytz.utc)
moonrise = obs.next_rising(e.Moon()).datetime().replace(tzinfo=pytz.utc)
moonset = obs.next_setting(e.Moon()).datetime().replace(tzinfo=pytz.utc)

sunset = sunset.astimezone(tz=gb)
sunrise = sunrise.astimezone(tz=gb)
moonset = moonset.astimezone(tz=gb)
moonrise = moonrise.astimezone(tz=gb)

riseset = [("Sunrise", sunrise),("Sunset", sunset),("Moonrise",moonrise),("Moonset",moonset)]
riseset.sort(key=takeSecond)
#print(riseset)

#print(riseset[0][0]) #sunset
#print(riseset[1][0]) #moonrise
#print(riseset[2][0]) #moonset
#print(riseset[3][0]) #sunrise

moon = e.Moon()
moon.compute(datetime.datetime.now())
earthToMoon = int(moon.earth_distance * auToKm)
earthToMoon = format(earthToMoon, ' ,d')
#print(earthToMoon)



#Code to pull back the weather
def testValues():
    #print the whole JSON array
    #print(weather)
    print("Feels Like: "+ feelLikeTemp +"°C")
    print("Actual Temp: "+ temp +"°C")
    print("Precipitation Probablity: "+ precip + "%")
    print("Wind Speed: " + windspd + " mph")
    print("Wind Direction: " + winddir)
    print("Observation: " + observation)


weatherDataUrl = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/352090?res=3hourly&key=c5e68363-c162-4e94-8661-bc92d217577a"
jWeather = requests.get(weatherDataUrl)
weather = json.loads(jWeather.text)
#print(weather)

location = (weather['SiteRep']['DV']['Location']['name'])
feelLikeTemp = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][currentWeatherPeriod]['F'])
#print("Feels Like: "+ feelLikeTemp +"°C")
temp = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][currentWeatherPeriod]['T'])
#print("Actual Temp: "+ temp +"°C")
precip = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][currentWeatherPeriod]['Pp'])
#print("Precipitation Probablity: "+ precip + "%")
weatherCode = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][currentWeatherPeriod]['W'])

if observation == "NA":
    observation = "N/A"
else:
    observation = str(weatherCodeDesc[int(weatherCode)])

#print(observation + " ("+weatherCode+")")



windspd = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][currentWeatherPeriod]['S'])
winddir = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][currentWeatherPeriod]['D'])
gust = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][currentWeatherPeriod]['G'])
#testValues()

#marsweather = maas.latest()
#print(marsweather.max_temp + ": Max Mars Temperature")
issAboveView = "http://www.heavens-above.com/orbitdisplay.aspx?icon=iss&width=300&height=300&mode=A&satid=25544"
issGroundTrack = "http://www.heavens-above.com/orbitdisplay.aspx?icon=iss&width=1500&height=750&mode=M&satid=25544"

#issAboveImg = urllib.request.urlretrieve(issAboveView, "../IMG/issAbove.png")
i = requests.get(issAboveView)
issAboveImg = Image.open(BytesIO(i.content))

#Mask out the water mark for the above view
issCreditMaskAbove = 107, 8
issCreditMaskAbove = Image.new("RGBA", issCreditMaskAbove)
issCreditMaskAbove.save("../IMG/issCreditMaskAbove.png")
issCreditMarkAbove = 190, 290
issAboveImg.paste(issCreditMaskAbove, issCreditMarkAbove)
issAboveImg.save("../IMG/issAbove.png")
#end of mask code for above view

i = requests.get(issGroundTrack)
issGroundImg = Image.open(BytesIO(i.content))

#Mask out the water mark for the ground view
issCreditMaskGround = 107, 8
issCreditMaskGround = Image.new("RGBA", issCreditMaskGround)
issCreditMaskGround.save("../IMG/issCreditMaskGround.png")
issCreditMarkGround = 1390, 740
issGroundImg.paste(issCreditMaskGround, issCreditMarkGround)
issGroundImg.save("../IMG/issGround.png")
#end of mask code for ground view


htmlFile = open("../Display_V2.html", "w+")

htmlFile.write(
'''<!DOCTYPE html>
<html>
  <head>
      <title>AD BOARD - KIELDER OBSERVATORY</title>
      <link rel="stylesheet" type="text/css" href="CSS/displayStyleV2.css">
  </head>

  <body>

      <div class="blockOne">

        <!--Imgs and divs for the slide show-->

        <div class="slideShowContainer">

          <div class="slide fade">
            <img src="IMG/blockOneImgs/Dan M MILKY WAY 2.jpg">
          </div>

          <div class="slide fade">
            <img src="IMG/blockOneImgs/Dan M MILKY WAY 2.jpg">
          </div>

          <div class="slide fade">
            <img src="IMG/blockOneImgs/Dan M MILKY WAY 2.jpg">
          </div>

        </div>
        <img id="kLogo" src="IMG/blockOneImgs/ObsLogo_NoBG.png">
        <script>
        var slideIndex = 0;
        showSlides();

        function showSlides()
        {
          var i;
          var slides = document.getElementsByClassName("slide");
          for (i = 0; i < slides.length; i++)
          {
            slides[i].style.display = "none";
          }
          slideIndex++;
          if (slideIndex > slides.length)
          {
            slideIndex = 1
          }
          slides[slideIndex-1].style.display = "block";
          setTimeout(showSlides, 3000); //Show image for 5 seconds
        }
        </script>

        <!--End of imgs and divs for the slide show-->
        <p id="text">Stargazing heaven <br/> all year round!</p>
      </div>

      <div class="blockTwo">
        <div class="weather tables fade">
          <p class="title">Current weather <br/> in Kielder</p>
          <img id="weatherIcon" src="IMG/metofficeicons/metimg'''+str(weatherCode)+'''.svg"/>
          <p class="weatherIconDesc">'''+str(observation)+'''</p>

          <p class="Temp">'''+str(temp)+''' &deg;C</p>

          <table id="weatherTable">
            <tr>
              <th>Wind Speed (Gust)</th>
              <th>Wind Direction</th>
              <th>Percipitation Probablity</th>
            </tr>
            <tr>
              <td>'''+str(windspd)+''' mph ('''+str(gust)+''')</td>
              <td>'''+str(winddir)+'''</td>
              <td>'''+str(precip)+'''%</td>
            </tr>
          </table>

          <table id="astroDataTable">
            <tr>
              <th>Sunset</th>
              <th>Moonrise</th>
              <th>Sunrise</th>
              <th>Moonset</th>
            </tr>
            <tr>
              <td>'''+riseset[0][1].strftime("%H:%M:%S %Z")+'''</td>
              <td>'''+riseset[1][1].strftime("%H:%M:%S %Z")+'''</td>
              <td>'''+riseset[3][1].strftime("%H:%M:%S %Z")+'''</td>
              <td>'''+riseset[2][1].strftime("%H:%M:%S %Z")+'''</td>
            </tr>
          </table>
        </div>

        <div class="moon tables fade">
          <p class="title">Tonights Moon</p>
          <img id="moonImage" src="IMG/moonframes/'''+str(phase)+'''"/>

          <p class="moonData"><b>'''+str(moonPhase)+'''%<b/> / <b>'''+getMoonPhaseName(float(moonPhase))+'''<b/>
            <br/><br/><br/>
            The Moon sets <b>'''+str(getTimeDiff())+'''<b/> after the sun
            <br/><br/><br/>
            Distance from the moon: <b>'''+str(earthToMoon)+''' Km</b>
          </p>
        </div>

      <div class="ISS tables fade">
        <img id="issGround" src="IMG/issGround.png">
        <img id="issAbove" src="IMG/issAbove.png">

        <div class="issInfo">
          <p>ISS Passes / Crew Info</p>
        </div>
      </div>
    </div>

      <script>
      var tableIndex = 0;
      showTables();

      function showTables()
      {
        var i;
        var tables = document.getElementsByClassName("tables");
        for (i = 0; i < tables.length; i++)
        {
          tables[i].style.display = "none";
        }
        tableIndex++;
        if (tableIndex > tables.length)
        {
          tableIndex = 1
        }
        tables[tableIndex-1].style.display = "block";
        setTimeout(showTables, 5000); //Show data for 5 seconds
      }
      </script>

      <div class="blockThree">

        <table id="eventTable">
          <tr>
            <th style="border-right: white solid 5px">Date</th>
            <th style="border-right: white solid 5px">Event Name</th>
            <th>Spaces</th>
          </tr>
          '''+str(tableData)+'''
        </table>

      </div>
  </body>
</html>
'''
)
htmlFile.close()
