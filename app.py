import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import requests
from functools import wraps
from datetime import date



def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

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
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        password = request.form.get("password")
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("Must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("Must provide password", 400)

        elif password != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)

        #elif len(password) < 8:
        #    return apology("Password must be at least 8 characters", 400)

        #digit = re.findall("\d", password)
        #if not digit:
        #    return apology("Password must have at least one digit", 400)

        #spec_char = re.findall("[!@#$%]", password)
        #if not spec_char:
            #return apology(
                #"Password must contain at least one special character (!, @, #, $, %)",
                #400,
            #)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # check if the username already exists
        if len(rows) > 0:
            return apology("Username is not available", 400)

        # get the hash of the password
        hash = generate_password_hash(request.form.get("password"))
        db.execute(
            "INSERT INTO users (username, hash) VALUES (:username, :hash)",
            username=request.form.get("username"),
            hash=hash,
        )

        # store their user id
        session["user_id"] = db.execute(
            "SELECT user_id FROM users WHERE username = :username",
            username=request.form.get("username"),
        )[0]["user_id"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
def average():
    formatted_date = datetime.now().strftime('%m/%d/%Y')
    count = db.execute("SELECT COUNT(*) FROM ratings WHERE date = ?", formatted_date)
    if count[0]["COUNT(*)"] > 0:
        average_rating = db.execute("SELECT AVG(rating) FROM ratings WHERE date = ?", formatted_date)
        return average_rating

@app.route("/")
@login_required
def home():
    if request.method == "GET":
        user_id = session["user_id"]
        # get access to the food items, date they are serverd, mealtime, where they are served and nutrition facts in a database

        # first we need to be able to loop through the API and generate a list of say, the menu items
        # to do this we need to index through everything, specify what we want, and return all those values in a single list
        # then export the data to food.db

        #for item in data:
        #    db.execute("INSERT INTO Meal (date, meal_time, location_name, recipe_name, meal_category) VALUES (?, ?, ?, ?, ?)", item['Serve_Date'], item['Meal_Name'], item['Location_Name'], item['Recipe_Print_As_Name'], item['Menu_Category_Name'])
        return render_template("home.html")
    else:
        return redirect("/")

def rating():
    # when you rate the item, the form you use in the html gives you a number from 0 to 5 and you send that to the rating database
    user_id = session["user_id"]
    formatted_date = datetime.now().strftime('%m/%d/%Y')
    # get user input
    rating = request.form.get("rating")
    review = request.form.get("review")

    # check if there is any input for rating and review
    if not rating:
        return apology("Missing Rating", 400)
    if not 0 <= int(rating) <= 5:
        return apology("Invalid Rating", 400)
    if not review:
        return apology("Missing Review", 400)

    db.execute("INSERT INTO Ratings (user_id, date, rating, review) VALUES (?, ?, ?, ?)", user_id, formatted_date, rating, review)

@app.route("/lunch", methods=["GET", "POST"])
@login_required
def lunch():
    user_id = session["user_id"]
    formatted_date = datetime.now().strftime('%m/%d/%Y')
    if request.method == "POST":
        rating = request.form.get("rating")
        review = request.form.get("review")
        if not rating:
            return apology("Missing Rating", 400)
        if not review:
            return apology("Missing Review", 400)
        db.execute("INSERT INTO Ratings (user_id, date, rating, review, meal_time) VALUES (?, ?, ?, ?, ?)", user_id, formatted_date, rating, review, "lunch")
    if request.method == "GET":
        # define formatted_date
        lunch_entree = db.execute("""
                            SELECT DISTINCT recipe_name FROM Meal
                            WHERE (location_name LIKE '%Adams%'
                            OR location_name LIKE '%Lowell%'
                            OR location_name LIKE '%Quincy%'
                            OR location_name LIKE '%Leverett%'
                            OR location_name LIKE '%Mather%'
                            OR location_name LIKE '%Dunster%'
                            OR location_name LIKE '%Eliot%'
                            OR location_name LIKE '%Kirkland%'
                            OR location_name LIKE '%Winthrop%'
                            OR location_name LIKE '%Cabot%'
                            OR location_name LIKE '%Pforzheimer%'
                            OR location_name LIKE '%Currier%'
                            OR location_name LIKE '%Annenberg%')
                            AND meal_time LIKE '%Lunch Entrees%'
                            AND meal_category LIKE '%Entrees%'
                            AND date = ?
                        """, (formatted_date))

        lunch_vegetables = db.execute("""
                            SELECT DISTINCT recipe_name FROM Meal
                            WHERE (location_name LIKE '%Adams%'
                            OR location_name LIKE '%Lowell%'
                            OR location_name LIKE '%Quincy%'
                            OR location_name LIKE '%Leverett%'
                            OR location_name LIKE '%Mather%'
                            OR location_name LIKE '%Dunster%'
                            OR location_name LIKE '%Eliot%'
                            OR location_name LIKE '%Kirkland%'
                            OR location_name LIKE '%Winthrop%'
                            OR location_name LIKE '%Cabot%'
                            OR location_name LIKE '%Pforzheimer%'
                            OR location_name LIKE '%Currier%'
                            OR location_name LIKE '%Annenberg%')
                            AND meal_time LIKE '%Lunch Entrees%'
                            AND meal_category LIKE '%Vegetables%'
                            AND date = ?
                        """, (formatted_date))
        lunch_starch = db.execute("""
                            SELECT DISTINCT recipe_name FROM Meal
                            WHERE (location_name LIKE '%Adams%'
                            OR location_name LIKE '%Lowell%'
                            OR location_name LIKE '%Quincy%'
                            OR location_name LIKE '%Leverett%'
                            OR location_name LIKE '%Mather%'
                            OR location_name LIKE '%Dunster%'
                            OR location_name LIKE '%Eliot%'
                            OR location_name LIKE '%Kirkland%'
                            OR location_name LIKE '%Winthrop%'
                            OR location_name LIKE '%Cabot%'
                            OR location_name LIKE '%Pforzheimer%'
                            OR location_name LIKE '%Currier%'
                            OR location_name LIKE '%Annenberg%')
                            AND meal_time LIKE '%Lunch Entrees%'
                            AND meal_category LIKE '%Starch And Potatoes%'
                            AND date = ?                        """, (formatted_date))
        lunch_vegan = db.execute("""
                            SELECT DISTINCT recipe_name FROM Meal
                            WHERE (location_name LIKE '%Adams%'
                            OR location_name LIKE '%Lowell%'
                            OR location_name LIKE '%Quincy%'
                            OR location_name LIKE '%Leverett%'
                            OR location_name LIKE '%Mather%'
                            OR location_name LIKE '%Dunster%'
                            OR location_name LIKE '%Eliot%'
                            OR location_name LIKE '%Kirkland%'
                            OR location_name LIKE '%Winthrop%'
                            OR location_name LIKE '%Cabot%'
                            OR location_name LIKE '%Pforzheimer%'
                            OR location_name LIKE '%Currier%'
                            OR location_name LIKE '%Annenberg%')
                            AND meal_time LIKE '%Lunch Entrees%'
                            AND meal_category LIKE '%Veg,Vegan%'
                            AND date = ?
                        """, (formatted_date))
        lunch_halal = db.execute("""
                            SELECT DISTINCT recipe_name FROM Meal
                            WHERE (location_name LIKE '%Adams%'
                            OR location_name LIKE '%Lowell%'
                            OR location_name LIKE '%Quincy%'
                            OR location_name LIKE '%Leverett%'
                            OR location_name LIKE '%Mather%'
                            OR location_name LIKE '%Dunster%'
                            OR location_name LIKE '%Eliot%'
                            OR location_name LIKE '%Kirkland%'
                            OR location_name LIKE '%Winthrop%'
                            OR location_name LIKE '%Cabot%'
                            OR location_name LIKE '%Pforzheimer%'
                            OR location_name LIKE '%Currier%'
                            OR location_name LIKE '%Annenberg%')
                            AND meal_time LIKE '%Lunch Entrees%'
                            AND meal_category LIKE '%Halal%'
                            AND date = ?
                        """, (formatted_date))
        return render_template("lunch.html", lunch_entree=lunch_entree, lunch_vegetables=lunch_vegetables, lunch_starch=lunch_starch, lunch_vegan=lunch_vegan, lunch_halal=lunch_halal)
    else:
        return redirect("/")

@app.route("/dinner", methods=["GET", "POST"])
@login_required
def dinner():
    user_id = session["user_id"]
    formatted_date = datetime.now().strftime('%m/%d/%Y')
    if request.method == "POST":
        rating = request.form.get("rating")
        review = request.form.get("review")
        if not rating:
            return apology("Missing Rating", 400)
        if not review:
            return apology("Missing Review", 400)
        db.execute("INSERT INTO Ratings (user_id, date, rating, review, meal_time) VALUES (?, ?, ?, ?, ?)", user_id, formatted_date, rating, review, "dinner")
    if request.method == "GET":

        dinner_entree = db.execute("""
                            SELECT DISTINCT recipe_name FROM Meal
                            WHERE (location_name LIKE '%Adams%'
                            OR location_name LIKE '%Lowell%'
                            OR location_name LIKE '%Quincy%'
                            OR location_name LIKE '%Leverett%'
                            OR location_name LIKE '%Mather%'
                            OR location_name LIKE '%Dunster%'
                            OR location_name LIKE '%Eliot%'
                            OR location_name LIKE '%Kirkland%'
                            OR location_name LIKE '%Winthrop%'
                            OR location_name LIKE '%Cabot%'
                            OR location_name LIKE '%Pforzheimer%'
                            OR location_name LIKE '%Currier%'
                            OR location_name LIKE '%Annenberg%')
                            AND meal_time LIKE '%Dinner Entrees%'
                            AND meal_category LIKE '%Entrees%'
                            AND date = ?
                        """, (formatted_date))

        dinner_vegetables = db.execute("""
                            SELECT DISTINCT recipe_name FROM Meal
                            WHERE (location_name LIKE '%Adams%'
                            OR location_name LIKE '%Lowell%'
                            OR location_name LIKE '%Quincy%'
                            OR location_name LIKE '%Leverett%'
                            OR location_name LIKE '%Mather%'
                            OR location_name LIKE '%Dunster%'
                            OR location_name LIKE '%Eliot%'
                            OR location_name LIKE '%Kirkland%'
                            OR location_name LIKE '%Winthrop%'
                            OR location_name LIKE '%Cabot%'
                            OR location_name LIKE '%Pforzheimer%'
                            OR location_name LIKE '%Currier%'
                            OR location_name LIKE '%Annenberg%')
                            AND meal_time LIKE '%Dinner Entrees%'
                            AND meal_category LIKE '%Vegetables%'
                            AND date = ?
                        """, (formatted_date))
        dinner_starch = db.execute("""
                            SELECT DISTINCT recipe_name FROM Meal
                            WHERE (location_name LIKE '%Adams%'
                            OR location_name LIKE '%Lowell%'
                            OR location_name LIKE '%Quincy%'
                            OR location_name LIKE '%Leverett%'
                            OR location_name LIKE '%Mather%'
                            OR location_name LIKE '%Dunster%'
                            OR location_name LIKE '%Eliot%'
                            OR location_name LIKE '%Kirkland%'
                            OR location_name LIKE '%Winthrop%'
                            OR location_name LIKE '%Cabot%'
                            OR location_name LIKE '%Pforzheimer%'
                            OR location_name LIKE '%Currier%'
                            OR location_name LIKE '%Annenberg%')
                            AND meal_time LIKE '%Dinner Entrees%'
                            AND meal_category LIKE '%Starch And Potatoes%'
                            AND date = ?
                        """, (formatted_date))
        dinner_vegan = db.execute("""
                            SELECT DISTINCT recipe_name FROM Meal
                            WHERE (location_name LIKE '%Adams%'
                            OR location_name LIKE '%Lowell%'
                            OR location_name LIKE '%Quincy%'
                            OR location_name LIKE '%Leverett%'
                            OR location_name LIKE '%Mather%'
                            OR location_name LIKE '%Dunster%'
                            OR location_name LIKE '%Eliot%'
                            OR location_name LIKE '%Kirkland%'
                            OR location_name LIKE '%Winthrop%'
                            OR location_name LIKE '%Cabot%'
                            OR location_name LIKE '%Pforzheimer%'
                            OR location_name LIKE '%Currier%'
                            OR location_name LIKE '%Annenberg%')
                            AND meal_time LIKE '%Dinner Entrees%'
                            AND meal_category LIKE '%Veg,Vegan%'
                            AND date = ?
                        """, (formatted_date))
        dinner_halal = db.execute("""
                            SELECT DISTINCT recipe_name FROM Meal
                            WHERE (location_name LIKE '%Adams%'
                            OR location_name LIKE '%Lowell%'
                            OR location_name LIKE '%Quincy%'
                            OR location_name LIKE '%Leverett%'
                            OR location_name LIKE '%Mather%'
                            OR location_name LIKE '%Dunster%'
                            OR location_name LIKE '%Eliot%'
                            OR location_name LIKE '%Kirkland%'
                            OR location_name LIKE '%Winthrop%'
                            OR location_name LIKE '%Cabot%'
                            OR location_name LIKE '%Pforzheimer%'
                            OR location_name LIKE '%Currier%'
                            OR location_name LIKE '%Annenberg%')
                            AND meal_time LIKE '%Dinner Entrees%'
                            AND meal_category LIKE '%Halal%'
                            AND date = ?
                        """, (formatted_date))

        return render_template("dinner.html", dinner_entree=dinner_entree, dinner_vegetables=dinner_vegetables, dinner_starch=dinner_starch, dinner_vegan=dinner_vegan, dinner_halal=dinner_halal)
    else:
        return redirect("/")


@app.route("/submit_review", methods=["POST"])
def submit_review():
    # Handle the form submission logic here

    # Redirect to home page after processing the form
    return redirect(url_for("home"))









