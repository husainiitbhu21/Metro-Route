import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from math import radians, cos, sin, asin, sqrt

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(initial, final):
    """Look up api for initial and final metro stations."""

    # Contact API
    try:
        url = f"https://us-central1-delhimetroapi.cloudfunctions.net/route-get?from={urllib.parse.quote_plus(initial)}&to={urllib.parse.quote_plus(final)}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "status": int(quote["status"]),
            "line1": quote["line1"],
            "line2": quote["line2"],
            "interchange": quote["interchange"],
            "lineEnds": quote["lineEnds"],
            "path": quote["path"],
            "time": round(float(quote["time"]))
        }
    except (KeyError, TypeError, ValueError):
        return None

# Function to calculate Distance Between Two Points on Earth
def dis(lat1, lat2, lon1, lon2):

    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. 
    r = 6372.8

    # calculate the result
    return(c * r)
