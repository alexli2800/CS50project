import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import requests
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

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

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/")
@login_required
def index():
    # get access to the food items, date they are serverd, mealtime, where they are served and nutrition facts in a database

    # first we need to be able to loop through the API and generate a list of say, the menu items
    # to do this we need to index through everything, specify what we want, and return all those values in a single list
    # then export the data to food.db
    recipe_names = []
    for item in data:
        recipe_names.append(item['Recipe_Name'])
    return recipe_names


