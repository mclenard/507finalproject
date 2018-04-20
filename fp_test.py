# mclenard Final Project
# This file contains the unit tests for the project

from app import *
from model import *
from fp_pop_db import retrieve_spotcrime_data
import unittest

class TestAccess(unittest.TestCase):
    def test_cache(self):
        CACHE_FNAME = 'crime_cache.json'

        try:
            cache_file = open(CACHE_FNAME, 'r')
            cache_contents = cache_file.read()
            CACHE_DICTION = json.loads(cache_contents)
            cache_file.close()
        except:
            CACHE_DICTION = {}

        tdata = retrieve_spotcrime_data()

        self.assertEqual(len(tdata), 17835)
        self.assertEqual(type(tdata[3]), type((1,2)))
        self.assertEqual(len(tdata[3]), 6)

class TestDatabase(unittest.TestCase):
    def test_db(self):
        try:
            conn = sqlite3.connect("CrimespotData.db")
        except Error as e:
            print(e)

        tcur = conn.cursor()

        tq = """
        SELECT d.Id, c.Id, c.Category, d.Date
        FROM Description AS d
        JOIN Category AS c
        ON c.Id = d.CategoryId
        """

        tcur.execute(tq)
        test_results = tcur.fetchall()

        self.assertEqual(len(test_results), 17835)
        self.assertEqual(test_results[56][0], 57)

        tq = """
        SELECT d.Id, c.Id, c.Category
        FROM Description AS d
        JOIN Category AS c
        ON c.Id = d.CategoryId
         WHERE c.Id = 3
        """

        tcur.execute(tq)
        test_results = tcur.fetchall()

        for res in test_results:
            self.assertEqual(res[2], "SHOOTING")
        self.assertEqual(len(test_results), 2)

        conn.close()


class TestProcessing(unittest.TestCase):
    def test_class(self):
        test_crime = Crime(5, 2, "Burglary", "04/20/2018", "01:02 AM", None, None, None)

        self.assertEqual(test_crime.id, 5)
        self.assertEqual(test_crime.category, "Burglary")
        self.assertEqual(test_crime.year, 18)
        self.assertEqual(test_crime.month, 4)

    def test_model(self):
        create_crime_list()
        tdl, tsl = get_selected()

        self.assertEqual(len(tsl), 17835)
        self.assertEqual(tdl[0][0], "2010")
        self.assertEqual(len(tdl[0]), 14)

        tdl2, tsl2 = get_selected(types=[3])

        self.assertEqual(tdl2[1][1], 1)
        self.assertEqual(tdl2[0][1], 0)
        self.assertEqual(tdl2[2][1], 0)
        self.assertEqual(tdl2[3][1], 1)
        self.assertEqual(tsl2[0], "SHOOTING on 07/24/13")
        self.assertEqual(tsl2[1], "SHOOTING on 05/29/11")

if __name__ == '__main__':
    unittest.main()
