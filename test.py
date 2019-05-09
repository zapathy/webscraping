from urllib.request import urlopen, Request, HTTPError
import bs4

unrecognized_suffixes = []
hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
link = "https://www.towerbudapest.com/en/sales/budapest_property/23922"
property_data = {}
content = urlopen(Request(link, headers=hdr)).read()
soup = bs4.BeautifulSoup(content, features="lxml")
header = soup.select('div[class*="property-content"]')[0].select('h1')[0].contents[0]
property_data['name'] = header
description = soup.select('div[class*="property-details-content-description"]')[0].select('p')[1].contents[0]
property_data['description'] = description
details = soup.select('div[class*="property-details-sidebar"]')[0]

for listitem in details.select('ul')[0].select('li'):
    new_key = listitem.select('strong')[0].contents[0].replace(':', '')
    if (len(listitem.contents) > 1):
        new_value = listitem.contents[1]
    else:
        new_value = True
    property_data[new_key] = new_value

property_data['Price_HUF'] = details.select('ul')[1].select('li')[1].contents[0].split()[0].replace('.', '')
if len(details.select('ul')[1].select('li')) > 2:
    property_data['Price_EUR'] = details.select('ul')[1].select('li')[2].contents[0].split()[0].replace('.', '')

property_data['Contact'] = details.select('ul')[2].select('li')[1].contents[0]

recognized_suffixes = ['utca', 'út', 'tér']
split_name = (str(property_data['name'])).split()
for s in split_name:
    if (s in recognized_suffixes):
        property_data['street_suffix'] = s
        split_name.remove(s)
        property_data['street_name'] = ' '.join(split_name)
        break

print(property_data)