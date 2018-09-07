#!/usr/bin/python3.7
# coding=utf8
import urllib
import datetime
import csv
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor

today = datetime.date.today()

issPassUrl = "https://heavens-above.com/PassSummary.aspx?satid=25544&lat=55.2323&lng=-2.616&loc=Kielder&alt=378&tz=GMT"
#issPassUrl = open("ISSVisiblePasses.html", "r")
issSoup = BeautifulSoup(urllib.request.urlopen(issPassUrl).read(), "html.parser")
#issSoup = BeautifulSoup(issPassUrl.read(), "html.parser")

passes=issSoup.find("table","standardTable")
passes = str(passes).replace("><", ">\n<") # Separate table elements into new lines for Extractor
extractor = Extractor(passes)
extractor.parse()
extractor.write_to_csv(path='.')
#issPassUrl.close()
# Python CSV tutorial at https://realpython.com/python-csv/
with open('output.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    line = 0
    passlist = []
    for isspass in reader:
        if (line <= 1): # Skip first two lines of header data
            line += 1
        else:
            entry = []
            passday = datetime.datetime.strptime(isspass[0],"\n%d %b\n").replace(year=today.year)
            if (passday.month < today.month):
                passday = passday + timedelta(years=1)
            entry.append(passday)
            for i in range(1,12):
                if i in [2, 5, 8]:
                    dummy = datetime.datetime.strptime(isspass[i], "%H:%M:%S")
                    passtime = datetime.datetime(passday.year, passday.month, passday.day, dummy.hour, dummy.minute, dummy.second)
                    if i in [5,8]:
                        tdelt = passtime - entry[2]
                        if (tdelt > datetime.timedelta(seconds=-1) and tdelt < datetime.timedelta(minutes=15)):
                            pass
                        elif (tdelt > datetime.timedelta(hours=1)):
                            passtime = passtime - datetime.timedelta(hours=1)
                        elif (tdelt < datetime.timedelta(hours=-22)):
                            passtime = passtime + datetime.timedelta(days=1)
                        elif (tdelt > datetime.timedelta(minutes=-40)):
                            passtime = passtime + datetime.timedelta(hours=1)
                    entry.append(passtime)
                elif i in [1,3,6,9]:
                    entry.append(float(isspass[i].strip('°')))
                else:
                    entry.append(isspass[i])
            # Heavens Above Table parsed, perform calculations for display
            dur = entry[8] - entry[2]
            entry.append(dur)
            desc = ""
            if entry[1] < -2.8:
                desc = desc + "bright, "
            elif (entry[1]) > -1.4:
                desc = desc + "faint, "

            if entry[6] > 35:
                desc = desc + "overhead pass. "
            elif entry[6] < 15:
                desc = desc + "low-altitude pass. "
            if desc[-6:] != "pass. ":
                desc = desc.replace(", ", " pass. ")
            desc = desc.capitalize()

            if int(entry[3]) < 20 and entry[2] != entry[5]:
                desc = desc + "Rises "
            elif int(entry[3]) > 35:
                desc = desc + "Appears overhead "
            else:
                desc = desc + "Appears mid-pass "

            desc = desc + "towards " + entry[4] + " and "

            if int(entry[9]) < 20:
                desc = desc + "sets "
            else:
                desc = desc + "disappears mid-pass "

            desc = desc + "after " + str(dur)[3:] + "."

            passlist.append(desc)
            print(entry[2].strftime("%d %b - %H:%M:%S  --  "), desc)
#            print(entry)
            line += 1
