import json
import re
import sys
from urllib.request import urlopen, Request

import bs4
import requests

exceptions = {}
status_codes = {}


def main():
    global total_pages
    url = 'https://www.towerbudapest.com/en/sales'
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                      'Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    property_links = []
    property_data_list = []
    soup = bs4.BeautifulSoup(urlopen(Request(url, headers=hdr)).read(), features="lxml")
    for paragraph in soup.select('p[class*="kill-margin"]'):
        if 'Page' in str(paragraph.contents[0]):
            total_pages = int(paragraph.contents[0].split(' ')[10])
            break
    print("found " + str(total_pages) + " pages")
    for i in range(total_pages):
        print('=', end='')
    print()
    while True:
        soup = bs4.BeautifulSoup(urlopen(Request(url, headers=hdr)).read(), features="lxml")
        for tag in soup.findAll('a',
                                attrs={
                                    'href': re.compile("^https://www.towerbudapest.com/en/sales/budapest_property/")}):
            property_links.append(tag.get('href'))
        rightButton = soup.select('div[class*="text-right"]')[0].select('button')
        print('.', end='')
        sys.stdout.flush()
        if len(rightButton) != 0:
            url = rightButton[0]['onclick'].split("'")[1]
        else:
            print()
            break
    print()
    print("found " + str(len(property_links)) + " links")
    property_links = list(set(property_links))
    print(str(len(property_links)) + " after removing duplicates")
    for i in range(len(property_links)):
        if i % 10 == 0:
            print('=', end='')
    print()
    counter = 0
    global status_codes
    global exceptions
    for link in property_links:
        try:
            counter += 1
            if counter % 10 == 0:
                print('.', end='')
                sys.stdout.flush()
            property_data = {}
            content = urlopen(Request(link, headers=hdr)).read()
            soup = bs4.BeautifulSoup(content, features="lxml")
            header = soup.select('div[class*="property-content"]')[0].select('h1')[0].contents[0]
            property_data['name'] = header
            details = soup.select('div[class*="property-details-sidebar"]')[0]

            for listitem in details.select('ul')[0].select('li'):
                new_key = listitem.select('strong')[0].contents[0].replace(':', '').lower().replace(' ', '')
                if len(listitem.contents) > 1:
                    new_value = str(listitem.contents[1]).strip()
                    if new_value == 'Yes':
                        new_value = True
                    if new_value == 'No':
                        new_value = False
                else:
                    new_value = True
                property_data[new_key] = new_value

            property_data['pricehuf'] = details.select('ul')[1].select('li')[1].contents[0].split()[0].replace('.', '')
            if len(details.select('ul')[1].select('li')) > 2:
                property_data['priceeur'] = details.select('ul')[1].select('li')[2].contents[0].split()[0].replace('.',
                                                                                                                   '')

            # property_data['contact'] = details.select('ul')[2].select('li')[1].contents[0]

            property_data['name'] = property_data['name'].lower()
            recognized_suffixes = ['utca', 'út', 'tér', 'park']
            recognized_suffixes_english = ['street', 'road', 'square', 'park']
            split_name = (str(property_data['name'])).split()
            for s in split_name:
                if s in recognized_suffixes or s in recognized_suffixes_english:
                    if s in recognized_suffixes:
                        property_data['streetsuffix'] = s
                    if s in recognized_suffixes_english:
                        property_data['streetsuffix'] = recognized_suffixes[recognized_suffixes_english.index(s)]
                    split_name.remove(s)
                    property_data['streetname'] = ' '.join(split_name)
                    break

            property_data['size'] = int(property_data['size'].split(' ')[0])

            property_data_list.append(property_data)
            r = requests.post("https://propertybuddy-database.herokuapp.com/properties", json=property_data)
            # r = requests.post("http://localhost:8080/properties", json=property_data)

            latest_status_code = (r.status_code, json.loads(r.content)['message'])
            if latest_status_code in status_codes:
                status_codes[latest_status_code] += 1
            else:
                status_codes[latest_status_code] = 1
        except Exception as e:
            latest_exception = str(e)
            if "HTTPSConnectionPool" in latest_exception and "Max retries exceeded with url" in latest_exception:
                latest_exception = latest_exception.split("(Caused")[0]
            if latest_exception in exceptions:
                exceptions[latest_exception] += 1
            else:
                exceptions[latest_exception] = 1
    print()
    print()
    print('all done')
    end_print()


def end_print():
    print('status codes:')
    for c in status_codes:
        print("\t" + str(c[0]) + " x" + "\t" + str(status_codes[c]) + "\n\t\t" + str(c[1]))
    print('exceptions:')
    for e in exceptions:
        print("\t" + e + " x" + "\t" + str(exceptions[e]))


try:
    main()
except KeyboardInterrupt:
    print()
    print()
    print('exiting on user interrupt')
    end_print()
