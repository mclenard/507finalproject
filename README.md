# 507finalproject

Data Sources used: My project scrapes data from https://spotcrime.com/mi/ann+arbor/daily/more.
This page links to daily "crime blotters" that provide information on crimes that
occurred in the Ann Arbor area on that day, and I crawled/scraped each of the pages
available, from 10/1/2010 to 4/19/2017. This amounted to something around 1100 pages.

Program Structure: My program is separated into 5 python files and some other files
such as html templates and the cache and database. The five python files are:

1. fp_scrape_cache.py -- this file has the code to scrape the spotcrime pages
and cache the resulting page html

2. fp_pop_db.py -- this file has the code to retrieve page html from the cache and
populate the database with the relevant information after parsing the html for
each page

3. model.py -- this file has the "model" code for the app, which gathers the data
from the database, uses it to create a Crime class object for each row of the database,
and use the attributes of each Crime object to process information to pass back to
the app for viewing

4. app.py -- this file is the "controller" code for the app, which accounts for
user input

5. fp_test.py -- this file contains the unit tests for files 2 and 3

The Class I create, Crime, takes in information from the database and makes each
information type an attribute, plus a few additional attributes (month, year) that
allow for easier processing later on.

The main processing functions in my program are:

retrieve_spotcrime_data(): This function retrieves each page's html, parses it, and
puts the relevant information into a list of tuples for populating the database.

create_crime_list(): This function retrieves all ~18k rows from the database and
feeds the necessary information into the Crime class constructor, putting each
created Crime object into a list.

get_selected(): This function takes lists representing user selection of crime type
and year and narrows down the entire list of ~18k crimes to the ones the user specified.
It returns a list of all crimes the user elected to see, plus a list of lists formatted
specifically for output via html tables.

User guide:

If you're building this app up from scratch, you'll need to run the scraping file
first to build the cache. Spotcrime only allows scraping of 20 pages per run of the file,
so it takes many runs of the code to build the cache fully. After that, you'll need to run
the pop_db file once to create the database. Once the cache and database are created,
these files are no longer run.

To run the app, just enter "python app.py" in the right directory. There's no further
command line entry needed. The available presentation options are all checkboxes on the
app browser page. Users can select which years they'd like to see crime data for, which
types of crime, and whether they'd like to see each relevant crime (very briefly) listed.
The selected data is then shown in a table, where the frequency of crime for each month
& the total for that year are shown for each selected year.
