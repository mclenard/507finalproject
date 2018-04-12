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


def make_request_using_cache(url, params=None):
    unique_ident = get_unique_key(url, params)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url, params=params)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]


def get_spotcrime_data():
    for year in range(2010, 2018):
        for month in range(1, 13):
            for day in range(1, 32):
                datestring = "{}-{}-{}".format(year, month, day)
                url = 'https://spotcrime.com/mi/ann+arbor/daily-blotter/{}'.format(datestring)
                html = make_request_using_cache(url)


if __name__ == "__main__":
    get_spotcrime_data()
