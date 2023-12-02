import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import requests
from functools import wraps

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///food.db")

headers = {
    'X-Api-Key': 'bf38CA83IGUGr9QH2eaGvOAYqGoo4lGD', "Accept": "application/json"
}

response = requests.get('https://go.apis.huit.harvard.edu/ats/dining/v3/recipes', headers=headers)

if response.ok:
    data = response.json()
else:
    print("Error: ", response.status_code)


@app.route("/")
def index():
    # get access to the food items, date they are serverd, mealtime, where they are served and nutrition facts in a database

    # first we need to be able to loop through the API and generate a list of say, the menu items
    # to do this we need to index through everything, specify what we want, and return all those values in a single list
    # then export the data to food.db
    sourcream = data[0]['Recipe_Name']
    for item in data:
        print(data[item]['Recipe_Name'])




