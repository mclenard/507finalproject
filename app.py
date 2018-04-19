# mclenard Final Project
# This file contains the "controller" code
# for the crimespot data app

from flask import Flask, render_template, request, redirect
import model

app = Flask(__name__)

@app.route.("/")
def
