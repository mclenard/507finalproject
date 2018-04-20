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
        <p></p>
        <h2><a href="/crimedata"> Go to Crime Data page </a></h2>
        '''

@app.route("/crimedata", methods=['GET', 'POST'])
def crime_data():
    if request.method == 'POST':
        response = request.form
        types = []
        years = []
        for key in response:
            if "year" in key:
                years.append(int(response[key]))
            if "type" in key:
                types.append(int(response[key]))

        dl, sl = model.get_selected(types, years)

        try:
            if request.form['list'] == 'yes':
                return render_template("crimedata.html", data=dl, select=sl)
        except:
            return render_template("crimedata.html", data=dl, select=
            ["list option not selected"])

    else:
        dl, sl = model.get_selected([], [])
        return render_template("crimedata.html", data=dl)

if __name__ == '__main__':
    model.create_crime_list()
    app.run(debug=True)
