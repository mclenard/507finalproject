# mclenard Final Project
# This file contains the "controller" code
# for the crimespot data app

from flask import Flask, render_template, request, redirect
import model

app = Flask(__name__)

@app.route("/")
def index():
    return '''
        <h1>Ann Arbor Crime Data</h1>
        <ul>
            <li><a href="/crimedata"> Go to Crime Data page </a></li>
        </ul>
        '''

@app.route("/crimedata")
def crime_data():
    return None

if __name__ == '__main__':
    model.create_crime_list()
    app.run(debug=True)
