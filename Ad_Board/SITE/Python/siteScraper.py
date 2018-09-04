import ephem as e
import datetime
import pytz
import json, requests, urllib
#from nasa import maas
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
import csv

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

#Sun values
sunset = obs.next_setting(e.Sun())
# Change Time to Sunset to get Moon times and next sunrise
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

feelLikeTemp = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['F'])
#print("Feels Like: "+ feelLikeTemp +"°C")
temp = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['T'])
#print("Actual Temp: "+ temp +"°C")
precip = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['Pp'])
#print("Precipitation Probablity: "+ precip + "%")
weatherCode = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['W'])

if weatherCode ==  "NA":
    weatherCode = "N/A"
    observation = weatherCode
else:
    observation = weatherCodeDescs[int(weatherCode)]

#print("Observation: " + observation)
windspd = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['G'])
winddir = (weather['SiteRep']['DV']['Location']['Period'][0]['Rep'][0]['D'])
#testValues()

#marsweather = maas.latest()
#print(marsweather.max_temp + ": Max Mars Temperature")

issPassUrl = "https://heavens-above.com/PassSummary.aspx?satid=25544&lat=55.2323&lng=-2.616&loc=Kielder&alt=378&tz=GMT"
issSoup = BeautifulSoup(urllib.request.urlopen(issPassUrl).read(), "html.parser")

passes=issSoup.find("table","standardTable")
passes = str(passes).replace("><", ">\n<") # Separate table elements into new lines for Extractor
extractor = Extractor(passes)
extractor.parse()
extractor.write_to_csv(path='.')

# Python CSV tutorial at https://realpython.com/python-csv/
with open('output.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    line = 0
    passlist = []
    for isspass in reader:
        if (line <= 1):
            line += 1
        else:
            entry = []
            passday = datetime.datetime.strptime(isspass[0],"\n%d %b\n").replace(year=today.year)
            if (passday.month < today.month):
                passday = passday + timedelta(years=1)

            entry.append(passday)
            for i in range(1,12):
                if i in [2, 5, 8]:
                    dummytime = datetime.datetime.strptime(isspass[i], "%H:%M:%S")
                    passtime = datetime.time(dummytime.hour, dummytime.minute, dummytime.second)
                    print(passtime)
                    entry.append(passtime)
                else:
                    entry.append(isspass[i].strip('°'))
            passlist.append(entry)
            line += 1
print(passlist)

htmlFile = open("../DISPLAY.html", "w+")

htmlFile.write(
'''<!DOCTYPE html>
<html>
  <head>
      <title>AD DISPLAY - KIELDER OBSERVATORY</title>
      <link type="text/css" rel="stylesheet" href="CSS/displayStyle.css"/>
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
            setTimeout(showSlides, 3000);
          }
          </script>

      <!--End of Code for automatic slide show-->

      <div class="date">
      Tonight: '''+datestr+'''
      </div>

      <div class="weatherDataTableDiv">
        <table class="weatherDataTable">
          <tr>
            <th>Temperature (Feels Like)</th>
            <th>Wind Speed (Dir)</th>
            <th>Precipitation Probability</th>
            <th>Current Observation</th>
          </tr>
          <tr>
            <!--Insert Feels Like Temp here-->
            <td>'''+str(temp)+''' &deg;C ('''+str(feelLikeTemp)+''' &deg;C)</td>
            <!--Insert Wind Info here-->
            <td>'''+str(windspd)+''' mph ('''+str(winddir)+''')</td>
            <!--Insert Precipertaion Probability here-->
            <td>'''+str(precip)+'''&percnt;</td>
            <!--Insert Current Observation here-->
            <td>'''+str(observation)+'''</td>
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
