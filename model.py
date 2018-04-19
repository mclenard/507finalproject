# mclenard Final Project
# This file contains the "model" code
# for the crimespot data app

import json
import sqlite3

crime_list = []

class Crime():
    def __init__(self, id, catid, category, date, time, address, desc, code):
        self.id = id
        self.catid = catid
        self.category = category
        self.date = date
        self.year = int(date[-2:])
        self.time = time
        self.address = address
        self.description = desc
        self.code = code

    def __str__(self):
        return "{} on {}".format(self.category, self.date)

def create_crime_list():
    global crime_list
    try:
        conn = sqlite3.connect("CrimespotData.db")
    except Error as e:
        print(e)

    cur = conn.cursor()

    q = """
    SELECT d.Id, c.Id, c.Category, d.Date, d.Time, d.Address, d.ShortDesc, d.Code
     FROM Description AS d
     JOIN Category AS c
     ON c.Id = d.CategoryId
    """

    cur.execute(q)
    result_list = cur.fetchall()

    conn.close()

    for r in result_list:
        crime_list.append(Crime(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))

    return None

create_crime_list()
