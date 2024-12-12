from bs4 import BeautifulSoup
import urllib.request
import urllib3
import time
import random
import csv
from urllib.request import Request, urlopen
from geopy.geocoders import Photon

#used for finding the zipcode
geolocator = Photon(user_agent="measurements")

def double_quote(word):
    double_q = '"' # double quote
    return double_q + word + double_q

#possible headers that can be used
User = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15']

#open your file, and add your column titles(make sure you have the correct file path)
path = 'c:/Users/kykyk/OneDrive/Desktop/stations.csv'
file = open(path, 'w', encoding='utf-8')
file.write("street" + "," + "city" + "," + "state" +"," + "zip" +"," +"regular" +"," +"midgrade" +","+"premium"+","+"diesel"+"\n")

for i in range(1, 10):
    try:
        r1 = random.randint(3, 10)
        time.sleep(r1) # rate limiting prevention
        #replace the first portion of the request with the site you want to scrape, you may want to rotate the headers while scraping
        req = Request('http://www.gasbuddy.com/station/' + str(i), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        #check what info you want from the site first and copy to the class below
        name = soup.find_all("h2", class_="header__header2___1p5Ig header__header___1zII0 header__midnight___1tdCQ header__snug___lRSNK StationInfoBox-module__header___2cjCS")
        address = soup.find("div", class_="StationInfoBox-module__ellipsisNoWrap___1-lh5")
        loca = address.find_all ("span")
        price = soup.find_all("span", class_="text__xl___2MXGo text__bold___1C6Z_ text__left___1iOw3 FuelTypePriceDisplay-module__price___3iizb")
        if len(name) == 0:
            print("Site did not have a Station %d", i)
        else:
            #strip html leaving only text
            name = name[0].text.strip()
            street, area, regular, midgrade, premium = loca[1].text, loca[3].text, price[0].text, price[1].text, price[2].text
            #used to get the zipcode
            addy = str(street) + ' ' + str(area)
            name = area.split()
            city = name[0][:-1]
            state = name[1]
            location = geolocator.geocode(addy)
            loc_data = str(location).split()
            x = [i[-2].isalpha() for i in loc_data]
            zip = 0
            for n in range(0, len(x)):
                if x[n] == False:
                    if loc_data[n] not in addy:
                        zip = loc_data[n][:-1]
            #write to the file
            file.write(street + "," + city + "," + state +"," + zip +"," +regular +"," +midgrade +","+premium+"\n")
    except:
        print("Error processing Station %d", i)

#close file
file.close()

'''headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}'''