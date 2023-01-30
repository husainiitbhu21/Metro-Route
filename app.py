import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, dis

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///metrostation.db")

# Add support for JSON requests
app.config['JSON_AS_ASCII'] = False

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Ask user data"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        lati1 = request.form.get("lati")
        lati = float(lati1)
        longi1 = request.form.get("longi")
        longi = float(longi1)
        latf1 = request.form.get("latf")
        latf = float(latf1)
        longf1 = request.form.get("longf")
        longf = float(longf1)

        if not lati1 or not longi1 or not latf1 or not longf1:
            return apology("missing input")
        elif not lati or not longi or not latf or not longf:
            return apology("input is not float")
        elif lati < 27.0 or lati > 29.0 or latf < 27.0 or latf > 29.0 or longi < 76.0 or longi > 78.0 or longf < 76.0 or longf > 78.0:
            return apology("outside of delhi")
        else:
            stations = db.execute("SELECT * FROM station")
            station_id = 0
            di = 0.0
            df = 0.0
            min1 = 70000.0
            min2 = 70000.0
            a = 1
            b = 1
            for station in stations:
                station_id += 1
                di = dis(lati, station["latitude"], longi, station["longitude"])
                if di < min1:
                    min1 = di
                    a = station_id
                df = dis(latf, station["latitude"], longf, station["longitude"])
                if df < min2:
                    min2 = df
                    b = station_id

            initial = stations[a-1]["station_name"]
            la1 = stations[a-1]["latitude"]
            lg1 = stations[a-1]["longitude"]
            final = stations[b-1]["station_name"]
            la2 = stations[b-1]["latitude"]
            lg2 = stations[b-1]["longitude"]

            if lookup(initial, final) == None:
                return apology("Error")

            else:
                api = lookup(initial, final)
                if api["status"] == 200:
                    return render_template("data.html", api=api, initial=initial, final=final, lati=lati, longi=longi, latf=latf, longf=longf, la1=la1, lg1=lg1, la2=la2, lg2=lg2)
                else:
                    flash("Metro not needed!")
                    return redirect("/")

    else:
        return render_template("index.html")

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password!")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    name = request.form.get("username")
    p1 = request.form.get("password")
    p2 = request.form.get("confirmation")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not name:
            return apology("must provide username")

        # Ensure password was submitted
        elif not p1:
            return apology("must provide password")

        # Ensure confirmation matches with password
        elif p1 != p2:
            return apology("Password and confirmation don't match!")

        # Ensure username does not exists before
        elif db.execute("SELECT username FROM users WHERE username = ?", name):
            flash("Username already exist!")
            return redirect("/register")

        # Take user in
        else:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", name, generate_password_hash(p1))
            # Remember which user has logged in (intentionally change variable rows to row)
            row = db.execute("SELECT * FROM users WHERE username = ?", name)
            session["user_id"] = row[0]["id"]
            # Redirect user to home page
            flash("Welcome to Metro Route")
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow user to change her password"""

    if request.method == "POST":

        # Ensure current password is not empty
        if not request.form.get("current_password"):
            return apology("must provide current password")

        # Query database for user_id
        rows = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])

        # Ensure current password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("current_password")):
            flash("Invalid password!")
            return redirect("/change_password")

        # Ensure new password is not empty
        if not request.form.get("new_password"):
            return apology("must provide new password")

        # Ensure new password confirmation is not empty
        elif not request.form.get("new_password_confirmation"):
            return apology("must provide new password confirmation")

        # Ensure new password and confirmation match
        elif request.form.get("new_password") != request.form.get("new_password_confirmation"):
            flash("New password and confirmation must match!")
            return redirect("/change_password")

        # Update database
        hash = generate_password_hash(request.form.get("new_password"))
        rows = db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, session["user_id"])

        # Show flash
        flash("Changed!")
        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("change_password.html")

@app.route("/nearbystation/<int:id>", methods=["POST"])
@login_required
def nearbystation(id):
    location = request.get_json()
    lat = float(location["latitude"])
    long = float(location["latitude"])

    if lat < 27.0 or lat > 29.0 or long < 76.0 or long > 78.0:
        op = "True"
        name = "y"
        lat = 0.0
        long = 0.0
        la = 0.0
        lg = 0.0

    else:
        op = "False"
        stations = db.execute("SELECT * FROM station")
        station_id = 0
        di = 0.0
        min = 70000.0
        a = 1
        for station in stations:
            station_id += 1
            di = dis(lat, station["latitude"], long, station["longitude"])
            if di < min:
                min = di
                a = station_id

        name = stations[a-1]["station_name"]
        la = stations[a-1]["latitude"]
        lg = stations[a-1]["longitude"]
    
    return {
        "bool": op,
        "lat": lat,
        "long": long,
        "la": la,
        "lg": lg, 
        "name": name
    }

@app.route("/grabstation/<string:isd>/<string:lat>/<string:long>/<string:la>/<string:lg>/<string:name>/", methods=["GET"])
@login_required
def grabstation(isd, lat, long, la, lg, name):
    if isd == "True":
        flash("Not in Delhi!")
        return redirect("/")
    
    else:
        flash(f"Nearest Station: {name.capitalize()}")
        return render_template("nearbystation.html", lat=float(lat), long=float(long), la=float(la), lg=float(lg), name=name)

@app.route("/map")
@login_required
def map():
    return render_template("map.html")

@app.route("/show/<string:lat1>/<string:long1>/<string:lat2>/<string:long2>/", methods=["GET"])
@login_required
def show(lat1,long1,lat2,long2):
    lati = float(lat1)
    longi = float(long1)
    latf = float(lat2)
    longf = float(long2)
    stations = db.execute("SELECT * FROM station")
    station_id = 0
    di = 0.0
    df = 0.0
    min1 = 70000.0
    min2 = 70000.0
    a = 1
    b = 1
    for station in stations:
        station_id += 1
        di = dis(lati, station["latitude"], longi, station["longitude"])
        if di < min1:
            min1 = di
            a = station_id
        df = dis(latf, station["latitude"], longf, station["longitude"])
        if df < min2:
            min2 = df
            b = station_id

    initial = stations[a-1]["station_name"]
    la1 = stations[a-1]["latitude"]
    lg1 = stations[a-1]["longitude"]
    final = stations[b-1]["station_name"]
    la2 = stations[b-1]["latitude"]
    lg2 = stations[b-1]["longitude"]

    if lookup(initial, final) == None:
        return apology("Error")

    else:
        api = lookup(initial, final)
        if api["status"] == 200:
            return render_template("data.html", api=api, initial=initial, final=final, lati=lati, longi=longi, latf=latf, longf=longf, la1=la1, lg1=lg1, la2=la2, lg2=lg2)
        else:
            flash("Metro not needed!")
            return redirect("/")