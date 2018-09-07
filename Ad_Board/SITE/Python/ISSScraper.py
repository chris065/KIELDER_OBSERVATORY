#!/usr/bin/python3.7
# coding=utf8
import urllib
import datetime
import csv
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor


#issPassUrl = "https://heavens-above.com/PassSummary.aspx?satid=25544&lat=55.2323&lng=-2.616&loc=Kielder&alt=378&tz=GMT"
issPassUrl = open("ISSVisiblePasses.html", "r")
#issSoup = BeautifulSoup(urllib.request.urlopen(issPassUrl).read(), "html.parser")
issSoup = BeautifulSoup(issPassUrl.read(), "html.parser")

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
                        print(entry[2], passtime)
                        if ((passtime-entry[2]) > datetime.timedelta(hours=1)):
                            passtime = passtime - datetime.timedelta(hours=1)
                        elif ((passtime-entry[2]) < datetime.timedelta(hours=-22)):
                            passtime = passtime + datetime.timedelta(days=1)
                        elif ((passtime-entry[2]) > datetime.timedelta(minutes=-40)):
                            passtime = passtime + datetime.timedelta(hours=1)
                    entry.append(passtime)
                else:
                    entry.append(isspass[i].strip('°'))
            # Heavens Above Table parsed, perform calculations for display
            dur = entry[8] - entry[2]
            entry.append(str(dur))

            if int(entry[3]) < 20:
                entry.append("Rises")
            else:
                entry.append("Appears overhead")

            if int(entry[9]) < 20:
                entry.append("Sets")
            else:
                entry.append("Disappears overhead")

            passlist.append(entry)
            print(entry)
            line += 1
