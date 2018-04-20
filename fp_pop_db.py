# mclenard Final Project
# This file contains code to retreive data from the cache,
# parse the html for relevant data,
# and populate a database with that data

import json
import sqlite3
import sys
from bs4 import BeautifulSoup
from fp_scrape_cache import make_request_using_cache, get_unique_key

CACHE_FNAME = 'crime_cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}


def init_db():
    try:
        conn = sqlite3.connect("CrimespotData.db")
    except Error as e:
        print(e)

    cur = conn.cursor()

    create_table_statement = '''
    CREATE TABLE 'Description' (
        "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "CategoryId" INTEGER,
        "Date" TEXT,
        "Time" TEXT,
        "Address" TEXT,
        "ShortDesc" TEXT,
        "Code" TEXT,
        FOREIGN KEY ("CategoryId") REFERENCES "Category(Id)"
    );
    '''
    cur.execute(create_table_statement)

    create_table_statement = '''
    CREATE TABLE 'Category' (
        "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "Category" TEXT
    );
    '''
    cur.execute(create_table_statement)


def retrieve_spotcrime_data():
    data_list = []
    for key in CACHE_DICTION:
        if key == "https://spotcrime.com/mi/ann+arbor/daily/more":
            pass
        else:
            page_html = CACHE_DICTION[key]
            page_soup = BeautifulSoup(page_html, 'html.parser')
            page_table = page_soup.find(class_="table")
            table_rows = page_table.find_all("tr")
            table_rows.pop(0)
            for row in table_rows:
                items = row.find_all("td")
                items.pop()
                items.pop(0)
                cat_tag = items[0]
                cat = cat_tag.text.upper()
                date_tag = items[1]
                date = date_tag.text[:8]
                if len(date_tag.text) > 10:
                    time_tag = items[1]
                    time = time_tag.text[-9:-1]
                else:
                    time = None
                if int(date[-2:]) > 16 or (int(date[-2:]) >= 16 and int(date[:2]) > 2):
                    desc_tag = items[2]
                    desc = desc_tag.text[:-5]
                    code_tag = items[2]
                    code = code_tag.text[-4:]
                    address = None
                else:
                    address_tag = items[2]
                    address = address_tag.text
                    desc = None
                    code = None
                data_list.append((cat, date, time, address, desc, code))
    return data_list

if __name__ == '__main__':
    init_db()

    data = retrieve_spotcrime_data()

    try:
        conn = sqlite3.connect("CrimespotData.db")
    except Error as e:
        print(e)

    cur = conn.cursor()

    for tup in data:
        insertion = (None, None, tup[1], tup[2], tup[3], tup[4], tup[5])
        statement = 'INSERT INTO "Description" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)

    conn.commit()

    crime_set = set()
    for tup in data:
        crime_set.add(tup[0])

    cnt = 1
    type_dict = {}
    for crime_type in crime_set:
        insertion = (None, crime_type)
        statement = 'INSERT INTO "Category" '
        statement += 'VALUES (?, ?)'
        type_dict[crime_type] = cnt
        cnt += 1
        cur.execute(statement, insertion)

    conn.commit()

    type_list = [None]
    for tup in data:
        categ = tup[0]
        if categ in type_dict:
            type_list.append(type_dict[categ])

    for id in range(1, 17836):
        statement = '''
        UPDATE Description
        SET CategoryId = ?
          WHERE Id = ?
        '''
        params = (type_list[id], id, )
        cur.execute(statement, params)

    conn.commit()

    conn.close()
