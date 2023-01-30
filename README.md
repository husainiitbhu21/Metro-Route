# METRO ROUTE
#### Video Demo (Old Version):  <https://youtu.be/Mhk723n1aHc>
#### Description:
Hello, world!

The Delhi Metro is a mass rapid transit system serving Delhi and its satellite cities. The network consists of 10 colour-coded lines serving 255 stations with a total length of 348.12 kilometres. It is by far the largest and busiest metro rail system in India, and the second oldest after the Kolkata Metro. It is very difficult to find nearest metro stations for one's journey in DELHI.

Welcome to **Metro Route** - a simple online Metro route provider. Your Route was designed, written, and implemented by Husain Saify. For a quick tour of Your Route, please watch a short video.

![Input](https://imgur.com/DpGCemw.png)
![Output](https://imgur.com/kJq0H7A.png)
![oo](https://imgur.com/iIkbFVL.png)

## Quickstart

 1. Register or log into Your Route
 2. Input (latitude, longitude) values of the source and destination, which you can get from Google Maps. The source and destination need not be a metro station. Make these values are in Delhi.
 3. Site will provide journey details.
 4. Use **Nearby Station** feature to know the nearest station.
 5. Use **Search** to find intial location and destination on map.
 4. You can also change your password by change password icon.

## Features

 1. Get shortest complete path from Source Station to Destination
    Station
 2. Get list of Interchange Stations in order
 3. Get Metro Lines Changed
 4. Get Total Travel Time
 5. Get Final Station of Metro Line in direction of destination/next interchange

## Interactive Maps

 Details of journey are accompanied by interactive javascript maps

## Tech Used
 1. HTML, CSS, Javascript and Bootstrap.
 2. Python based web framework called Flask.
 3. SQL and sqlite3 database.
 4. DELHI METRO API.

## Haversine formula

![Earth](https://imgur.com/IpW1q2h.png)

Given latitude and longitude in degrees to find the distance between two points on the earth, we use Haversine Formula.
The great circle distance or the orthodromic distance is the shortest distance between two points on a sphere (or the surface of Earth). In order to use this method, we need to have the co-ordinates of point A and point B.The great circle method is chosen over other methods.

Distance, **d = 3963.0 * arccos[(sin(lat1) * sin(lat2)) + cos(lat1) * cos(lat2) * cos(long2 – long1)]** in km

This formula is used to find the nearest metro station from the given geolocations of origin and destination.


## Delhi Metro API
  A Javascript based API for calculating the shortest path between two metro stations.</br>
  The API is hosted on Google Firebase, and can be called at:</br>
  https://us-central1-delhimetroapi.cloudfunctions.net/route-get
  with a GET query and parameters as from (source station) and to (destination station).</br>
  For example, the API call for a route between Dwarka and Palam would be: https://us-central1-delhimetroapi.cloudfunctions.net/route-get?from=Dwarka&to=Palam.</br>
  The stations to be passed in the parameters must start with a capital letter.

## Acknowledgements:

  1. [Delhi Metro API](https://github.com/Mansehej/DelhiMetroAPI)
  2. [Metrostation Database](https://www.kaggle.com/datasets/kunalgupta2616/delhi-metro-stations-data)
  3. [Small portions of Python Flask code](https://cs50.harvard.edu/x/2022/psets/9/finance/)

  4. [Leaflet JS Library](https://leafletjs.com/)

