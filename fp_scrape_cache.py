# mclenard Final Project
# This file contains the code to scrape the website
# and cache the results

import requests
import json
from bs4 import BeautifulSoup

CACHE_FNAME = 'crime_cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}


def get_unique_key(url, params=None):
    if params == None:
        return url
    else:
        idstring = url
        for key in params:
            idstring += key
            idstring += str(params[key])
        return idstring


def make_request_using_cache(url):
    unique_ident = get_unique_key(url)

    if unique_ident in CACHE_DICTION:
        #print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]


def get_spotcrime_data():
    url_main = 'https://spotcrime.com/mi/ann+arbor/daily/more'
    html_main = make_request_using_cache(url_main)
    soup_main = BeautifulSoup(html_main, 'html.parser')
    content_main = soup_main.find(class_="main-content-column")
    columns_main = content_main.find_all(class_="list-unstyled")
    column_one = columns_main[0]
    column_two = columns_main[1]
    c1_links = column_one.find_all("a")
    c2_links = column_two.find_all("a")
    path_list = []
    for elem in c1_links:
        path_list.append(elem["href"])
    for elem in c2_links:
        path_list.append(elem["href"])

    for path in path_list:
        base_url = 'https://spotcrime.com'
        page_url = base_url + path
        html_page = make_request_using_cache(page_url)

    return path_list

if __name__ == "__main__":
    paths = get_spotcrime_data()
