import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
import json
from urllib.request import urlopen
# import pycountry


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


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

#########


# could not use ip adress and ggeolocation function of my code CS50 IDE does not include pycountry module :(
# def local():
#     # url = 'http://api.ipstack.com/189.217.204.74?access_key=edb5437d303d58d6768784ba68a6debe'
#     url = 'http://ipinfo.io/json'
#     response = urlopen(url)
#     data = json.load(response)
#     # print(data)
#     # print("Your Country is " + data['country'])
#     c = data['country']
#     print(f"Tú País es {c}")

#     país =  pycountry.countries.get(alpha_2 = c)
#     curren = pycountry.currencies.get(numeric = país.numeric)
#     print(curren.alpha_3)
#     c = curren.alpha_3

#     url2 = f'https://free.currconv.com/api/v7/convert?q=USD_{curren.alpha_3}&compact=ultra&apiKey=7e33716d0f94742166e0'
#     response2 = urlopen(url2)
#     dict = json.load(response2) # ya es un diccionario #

#     x = list(dict.values())[0]
#     return x, c
