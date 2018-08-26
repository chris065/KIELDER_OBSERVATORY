# Title: Astro Data Scraper
# Version: 1.0 (11/08/2018)
# Description: This script calculates the Sunrise, Moonrise, Sunset and Moonset
#              using the PyEphem module. Then writes it to the HTML file
#
# Author: Chris Bennett

import ephem as e
import datetime
import pytz

#making the BST timezone object
bst = pytz.timezone('Europe/London')

obsLat = '55.232302'
obsLon = '-2.616033'

#Setting the OBSERVATORY as the Observer
obs = e.Observer()

obs.lat, obs.lon = obsLat, obsLon
obs.date = datetime.datetime.now()

#Sun values
sunrise = obs.next_rising(e.Sun())
sunset = obs.next_setting(e.Sun())

#Moon values
moonrise = obs.next_rising(e.Moon())
moonset = obs.next_setting(e.Moon())



#dt = datetime.datetime.strptime(str(sunrise), "%Y/%m/%d %H:%M:%S")
#print(dt.time().isoformat())

#Increment all the times by +1 hour to deal with BST
#
#This will eventally change, but this bodge will just have
#to do for now
sunrise = e.Date(sunrise + e.hour)
sunset = e.Date(sunset + e.hour)
moonrise = e.Date(moonrise + e.hour)
moonset = e.Date(moonset + e.hour)

#print("Sunrise: " + str(sunrise))
#print("Sunset: " + str(sunset))
#print("Moonrise: " + str(moonrise))
#print("Moonset: " + str(moonset))

#Take out the date (Y/m/d) element of each value calculated. Leaving just the time
sunrise = datetime.datetime.strptime(str(sunrise), "%Y/%m/%d %H:%M:%S")
sunrise = sunrise.time().isoformat()

sunset = datetime.datetime.strptime(str(sunset), "%Y/%m/%d %H:%M:%S")
sunset = sunset.time().isoformat()

moonrise = datetime.datetime.strptime(str(moonrise), "%Y/%m/%d %H:%M:%S")
moonrise = moonrise.time().isoformat()

moonset = datetime.datetime.strptime(str(moonset), "%Y/%m/%d %H:%M:%S")
moonset = moonset.time().isoformat()


htmlFile = open("../DISPLAY.html", "w+")

#writing the sunrise, moonrise, sunset and the moonset data to the html file
#overwrite the file rather than append to it

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
        <script>
            var suffix = "";
            var nextSuffix = "";

            var months = ["January","February","March","April","May","June","July","August","September","October","November","December"];

            var today = new Date();
            var dd = today.getDate();
            var mm = months[today.getMonth()];
            var year = today.getFullYear();

            var nextDay = (dd+1);

            if(dd<10)
            {
                dd = '0'+dd
            }
            if(nextDay<10)
            {
                nextDay = '0'+dd
            }

            if(dd == 1 || dd == 21 || dd == 31)
            {
                suffix = "st";
            }
            if(dd == 2 || dd == 22)
            {
                suffix = "nd"
            }
            if(dd == 3 || dd == 23)
            {
                suffix = "rd"
            }
            else
            {
                suffix = "th"
            }

            if(nextDay == 1 || nextDay == 21 || nextDay == 31)
            {
                nextSuffix = "st";
            }
            if(nextDay == 2 || nextDay == 22)
            {
                nextSuffix = "nd"
            }
            if(nextDay == 3 || nextDay == 23)
            {
                nextSuffix = "rd"
            }
            else
            {
                nextSuffix = "th"
            }
            tonight = 'Tonight: ' + dd +suffix+' - '+ nextDay +nextSuffix+' '+ mm + ' ' + year;
            document.write(tonight);
        </script>
      </div>

        <div class="astroTableDiv">
          <table class="astroTable">
            <tr>
              <th>Sunset</th>
              <th>Moonrise</th>
              <th>Sunrise</th>
              <th>Moonset</th>
            </tr>
            <tr>
              <!--Input time for sunset-->
              <td>'''+str(sunset)+''' BST'''+'''</td>
              <!--input time for moonrise-->
              <td>'''+str(moonrise)+''' BST'''+'''</td>
              <!--Input time for sunrise-->
              <td>'''+str(sunrise)+''' BST'''+'''</td>
              <!--Input time for moonset-->
              <td>'''+str(moonset)+''' BST'''+'''</td>
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
          </tabel>
        </div>
  </body>
</html>
'''
)
htmlFile.close()
