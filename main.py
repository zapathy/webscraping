from urllib.request import urlopen, Request, HTTPError
import bs4
import pandas as pd
import numpy as np
import psycopg2
import re

url = 'https://www.towerbudapest.com/en/sales'
hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

property_links = []
while True:
    content = urlopen(Request(url, headers=hdr)).read()
    soup = bs4.BeautifulSoup(content, features="lxml")
    for tag in soup.findAll('a',
                            attrs={'href': re.compile("^https://www.towerbudapest.com/en/sales/budapest_property/")}):
        property_links.append(tag.get('href'))
    rightButton = soup.select('div[class*="text-right"]')[0].select('button')
    if len(rightButton) != 0:
        url = rightButton[0]['onclick'].split("'")[1]
    else:
        break

print(property_links)
print(len(property_links))

sections = soup.find_all("section", {"class": "reLiSection subjectWrapper"})
for link in property_links:
    content = urlopen(Request(link, headers=hdr)).read()
    soup = bs4.BeautifulSoup(content, features="lxml")
    print(soup.prettify())