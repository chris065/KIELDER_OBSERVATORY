import ephem as e
import datetime
import pytz
import json, requests, urllib
#from nasa import maas
from bs4 import BeautifulSoup
#from html_table_extractor.extractor import Extractor
import csv

import json, requests
import urllib
from PIL import Image

# Key definition for moonrise/set table
def takeSecond(elem):
    return elem[1]

def getMonth(monthNo):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month = (months[int(monthNo-1)])
    return month

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
#The condition code will map to one of these values
weatherCodeDescs = ["Clear night", "Sunny day", "Partly cloudy (night)", "Partly cloudy (day)", "Not used", "Mist", "Fog", "Cloudy", "Overcast", "Light rain shower (night)",
                    "Light rain shower (day)", "Drizzle", "Light rain", "Heavy rain shower (night)", "Heavy rain shower (day)", "Heavy rain", "Sleet shower (night)", "Sleet shower (day)",
                    "Sleet", "Hail shower (night)", "Hail shower (day)", "Hail", "Light snow shower (night)", "Light snow shower (day)", "Light snow", "Heavy snow shower (night)", "Heavy snow shower (day)",
                    "Heavy snow", "Thunder shower (night)", "Thunder shower (day)", "Thunder"]
#once the condition code has been mapped to the description it
#will be stored in this variable
observation = ""

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
lastFullMoonDate = str(pfm.date().day) + " " + str(getMonth(pfm.date().month))
lastFullMoonTime = pfm.strftime("%H:%M:%S %Z")

nnm = nnm.datetime().replace(tzinfo=pytz.utc)
nnm = nnm.astimezone(tz=gb)
nextNewMoonDate = str(nnm.date().day) + " " + str(getMonth(nnm.date().month))
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
feelLikeTemp = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['F'])
#print("Feels Like: "+ feelLikeTemp +"°C")
temp = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['T'])
#print("Actual Temp: "+ temp +"°C")
precip = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['Pp'])
#print("Precipitation Probablity: "+ precip + "%")
weatherCode = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['W'])

# Handle No Data errors
if weatherCode ==  "NA":
    observation = "N/A"
else:
    observation = weatherCodeDescs[int(weatherCode)]

# Remove day/night qualifiers from Observation text
# Text not removed from list in case we want to add a picture later on
for text in [" (day)", " (night)"]:
    if observation.endswith(text):
        observation = observation.replace(text, "")

windspd = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['S'])
winddir = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['D'])
gust = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['G'])
#testValues()

#marsweather = maas.latest()
#print(marsweather.max_temp + ": Max Mars Temperature")
issAboveView = "http://www.heavens-above.com/orbitdisplay.aspx?icon=iss&width=300&height=300&mode=A&satid=25544"
issGroundTrack = "http://www.heavens-above.com/orbitdisplay.aspx?icon=iss&width=1500&height=750&mode=M&satid=25544"

issAboveImg = urllib.request.urlretrieve(issAboveView, "../IMG/issAbove.png")
issAboveImg = Image.open("../IMG/issAbove.png")

#Mask out the water mark for the above view
issCreditMaskAbove = 107, 8
issCreditMaskAbove = Image.new("RGBA", issCreditMaskAbove)
issCreditMaskAbove.save("../IMG/issCreditMaskAbove.png")
issCreditMarkAbove = 190, 290
issAboveImg.paste(issCreditMaskAbove, issCreditMarkAbove)
issAboveImg.save("../IMG/issAbove.png")
#end of mask code for above view

issGroundImg = urllib.request.urlretrieve(issGroundTrack, "../IMG/issGround.png")
issGroundImg = Image.open("../IMG/issGround.png")

#Mask out the water mark for the ground view
issCreditMaskGround = 107, 8
issCreditMaskGround = Image.new("RGBA", issCreditMaskGround)
issCreditMaskGround.save("../IMG/issCreditMaskGround.png")
issCreditMarkGround = 1390, 740
issGroundImg.paste(issCreditMaskGround, issCreditMarkGround)
issGroundImg.save("../IMG/issGround.png")
#end of mask code for ground view



htmlFile = open("../DISPLAY.html", "w+")

htmlFile.write(
'''<!DOCTYPE html>
<html>
  <head>
      <title>AD DISPLAY - KIELDER OBSERVATORY</title>
      <link href="https://fonts.googleapis.com/css?family=Roboto+Condensed:300,700" rel="stylesheet">
      <link type="text/css" rel="stylesheet" href="CSS/haydensStyle.css"/>
  </head>

  <body>
      <p style="text-align: center;"><img class="logoIMG" src="IMG/logoNew.png"></p>

      <!--Start of code for automatic slide show
          The slide show will change the image every 3 seconds
          The slide show will be used to show light polution-->

          <div class="slideShowContainer">
            <div class="slides fade">
              <img src="IMG/LP_IMAGE.png" style="width: 100%;">
              <div class="text">Image taken in a light polluted enviroment</div>
            </div>

            <div class="slides fade">
              <img src="IMG/LPF_IMAGE.png" style="width: 100%;">
              <div class="text">Image taken in a light pollution free enviroment</div>
            </div>

            <div class="slides fade">
              <p style="text-align: center;"><img src="IMG/issAbove.png" style="width: 50%;"></p>
              <div class="text">current position of the ISS</div>
            </div>

            <div class="slides fade">
               <p style="text-align: center;"><img src="IMG/issGround.png" style="width: 100%;"></p>
              <div class="text">current position of the ISS</div>
            </div>

          </div>

          <script>
          var slideIndex = 0;
          showSlides();

          function showSlides()
          {
            var i;
            var slides = document.getElementsByClassName("slides");
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
            setTimeout(showSlides, 5000); //Show image for 5 seconds
          }
          </script>

      <!--End of Code for automatic slide show-->

      <div class="weatherDataTableDiv">
        <table class="weatherDataTable">
          <tr>
            <th>Temperature (Feels Like)</th>
            <th>Wind Speed (Gust)</th>
            <th>Wind Direction</th>
            <th>Precipitation Probability</th>
          </tr>
          <tr>
            <!--Insert Feels Like Temp here-->
            <td>'''+str(temp)+''' &deg;C ('''+str(feelLikeTemp)+''' &deg;C)</td>
            <!--Insert Wind Info here-->
            <td>'''+str(windspd)+''' mph ('''+str(gust)+''')</td>
            <td>'''+str(winddir)+'''</td>
            <!--Insert Precipertaion Probability here-->
            <td>'''+str(precip)+'''&percnt;</td>
          </tr>
        </table>
      </div>
      <!-- Add in div tag/table to showcase moon illumination info and
      phase image-->

      <div class="weatherIconDiv">
        <img class="weatherIcon" src="IMG/metofficeicons/metimg'''+str(weatherCode)+'''.svg">
     </div>

     <div class="date">
     Tonight: <b>'''+datestr+'''</b> in <b>'''+str(location).title()+'''</b>
     </div>

        <div class="astroTableDiv">
            <table class="astroTable">
                <tr>
                    <td colspan="2">Last Full Moon</td>
                    <td rowspan="3" ><img src="IMG/moonframes/'''+phase+'''" style="width:250px;height:250px;"></img></td>
                    <td rowspan="2" style="font-size:90px"><b>'''+str(moonPhase)+'''%</b> lit</td>
                    <td colspan="2">Next New Moon</td>
                </tr>
                <tr>
                    <td>'''+str(lastFullMoonDate)+'''</td>
                    <td rowspan="2">Last Full</td>
                    <td>'''+str(nextNewMoonDate)+'''</td>
                    <td rowspan="2">Next New</td>
                    </tr>
                <tr>
                    <td>'''+str(lastFullMoonTime)+'''</td>
                    <td>Moon Phase</td>
                    <td>'''+str(nextNewMoonTime)+'''</td>
                </tr>
            </table>
        </div>

        <div class="astroTableDiv">
          <table class="astroTable">
            <tr>
              <th>'''+riseset[0][0]+'''</th>
              <th>'''+riseset[1][0]+'''</th>
              <th>'''+riseset[2][0]+'''</th>
              <th>'''+riseset[3][0]+'''</th>
            </tr>
            <tr>
              <!--Input time for sunset-->
              <td>'''+riseset[0][1].strftime("%H:%M:%S %Z")+'''</td>
              <!--input time for moonrise-->
              <td>'''+riseset[1][1].strftime("%H:%M:%S %Z")+'''</td>
              <!--Input time for sunrise-->
              <td>'''+riseset[2][1].strftime("%H:%M:%S %Z")+'''</td>
              <!--Input time for moonset-->
              <td>'''+riseset[3][1].strftime("%H:%M:%S %Z")+'''</td>
            </tr>
          </table>
        </div>

        <div class="eventTableDiv">
          <table class="eventTable">
            <tr>
              <th>Date</th>
              <th>Event Name</th>
              <th>Spaces Available</th>
            </tr>

            <tr>
              <td>DD/MM</td>
              <td>Event Title</td>
              <td>Spaces</td>
            </tr>
            <tr>
              <td>DD/MM</td>
              <td>Event Title</td>
              <td>Spaces</td>
            </tr>
            <tr>
              <td>DD/MM</td>
              <td>Event Title</td>
              <td>Spaces</td>
            </tr>

            <tr>
              <td>DD/MM</td>
              <td>Event Title</td>
              <td>Spaces</td>
            </tr>

            <tr>
              <td>DD/MM</td>
              <td>Event Title</td>
              <td>Spaces</td>
            </tr>

            <tr>
              <td>DD/MM</td>
              <td>Event Title</td>
              <td>Spaces</td>
            </tr>
          </table>
        </div>
  </body>
</html>
'''
)
htmlFile.close()
