from flask import Flask, render_template, request
import psycopg2
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from datetime import datetime
import requests
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
import folium


app = Flask(__name__)

# Define the PostgreSQL connection URL
# Password should be changed
DATABASE_URL = "postgresql://postgres:password@localhost:5432/map_app"

# Create an engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a base class for declarative models
Base = declarative_base()


# Define the Ispark model
class Ispark(Base):
    __tablename__ = "ispark"

    id = Column(Integer, primary_key=True)  # Add a primary key
    park_name = Column(String(255))
    location_name = Column(String(255))
    park_type_id = Column(String(255))
    park_type_desc = Column(String(255))
    capacity_of_park = Column(Integer)
    working_time = Column(String(255))
    county_name = Column(String(255))
    longitude = Column(Float)
    latitude = Column(Float)
    location = Column(Text)


# Create a session
Session = sessionmaker(bind=engine)
session = Session()


def checkHour(interval):
    # Get the current hour
    current_hour = datetime.now().hour

    # Split the interval into start and end hours
    start_hour, end_hour = map(int, interval.split("-"))

    # Check if the current hour falls within the interval
    if start_hour <= current_hour < end_hour:
        return True
    return False


# Functions to handle geocoding and distance calculation
# def getCurrentLocation():
#     g = geocoder.ip("me")
#     return g.latlng if g.latlng else (None, None)

def getCurrentLocation():
    return (40.955857, 29.117504)


def reverse_geocode(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        location = geolocator.reverse((latitude, longitude), timeout=100)
        if location:
            address = location.raw["address"]
            country = address.get("country", "Country not found")
            state = address.get("state", "State not found")
            city = address.get("city", "City not found")
            suburb = address.get("suburb", "Suburb not found")
            road = address.get("road", "Road not found")
            house_number = address.get("house_number", "House number not found")

            return {
                "country": country,
                "state": state,
                "city": city,
                "suburb": suburb,
                "road": road,
                "house_number": house_number,
            }
        else:
            return "Address not found"
    except GeocoderTimedOut:
        return "Geocoding service timed out"
    except Exception as e:
        return f"An error occurred: {e}"


def get_distance(lat1, lon1, lat2, lon2):
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return None

    try:
        # Convert coordinates to floats to ensure they are numerical
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)

        coord1 = (lat1, lon1)
        coord2 = (lat2, lon2)

        # Calculate the geodesic distance
        distance = geodesic(coord1, coord2).kilometers

        # Return the distance formatted to two decimal places
        return float("{:.2f}".format(distance))
    except ValueError as e:
        print(f"Error calculating distance: {e}")
        return None
    except TypeError as e:
        print(f"Type error: {e}")
        return None


def getClosestIspark():
    curLoc = getCurrentLocation()
    if curLoc[0] is None or curLoc[1] is None:
        return None
    curLatitude, curLongitude = curLoc
    connection = psycopg2.connect(
        host="localhost", database="map_app", user="postgres", password="Aseyfo58"
    )
    cursor = connection.cursor()
    select_query = "SELECT park_name, latitude, longitude FROM ispark"
    min_distance = float("inf")
    min_distance_ispark = None
    cursor.execute(select_query)
    records = cursor.fetchall()
    for r in records:
        park_name, ispark_latitude, ispark_longitude = r
        if (
            ispark_latitude > 90
            or ispark_latitude < -90
            or ispark_longitude > 180
            or ispark_longitude < -180
        ):
            continue
        distance = get_distance(
            curLatitude, curLongitude, ispark_latitude, ispark_longitude
        )
        if distance is not None and distance < min_distance:
            min_distance = distance
            min_distance_ispark = r
    cursor.close()
    connection.close()
    return [min_distance_ispark, min_distance] if min_distance_ispark else [None, None]


# Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/isparks")
def isparks():
    isparks_list = session.query(Ispark).all()
    now = datetime.now()
    return render_template(
        "isparks.html",
        now=now,
        isparks_list=isparks_list,
        get_distance=get_distance,
        getCurrentLocation=getCurrentLocation,
    )


@app.route("/current_location")
def current_location_page():
    location = getCurrentLocation()
    address = reverse_geocode(location[0], location[1])
    return render_template(
        "current_location.html",
        latitude=location[0],
        longitude=location[1],
        address=address,
    )


@app.route("/closest_ispark")
def closest_ispark_page():
    closest = getClosestIspark()
    return render_template(
        "closest_ispark.html",
        closest_ispark={
            "name": closest[0][0] if closest[0] else None,
            "latitude": closest[0][1] if closest[0] else None,
            "longitude": closest[0][2] if closest[0] else None,
        },
        distance=closest[1],
    )


@app.route("/reverse_geocode", methods=["GET", "POST"])
def reverse_geocode_route():
    address = None
    if request.method == "GET":
        latitude = request.args.get("latitude", type=float)
        longitude = request.args.get("longitude", type=float)
        if latitude is not None and longitude is not None:
            address = reverse_geocode(latitude, longitude)
    return render_template("reverse_geocode.html", address=address)

@app.route("/ispark/<int:id>")
def ispark(id):
    ispark = session.query(Ispark).get(id)
    lat = ispark.latitude
    lon = ispark.longitude
    return render_template("ispark.html", ispark=ispark, lat=lat, lon=lon)


def colorOfMarker(argument):

    # Define a dictionary mapping park types to colors
    switcher = {
        "AÇIK OTOPARK": "blue",
        "MİNİBÜS PARK": "purple",
        "TAKSİ PARK": "red",
        "KAPALI OTOPARK": "black",
        "YOL ÜSTÜ": "green",
    }

    # Return the color based on the park type or default to 'gray'
    return switcher.get(argument, "gray")

@app.route("/ispark_map/<int:id>")
def ispark_map(id):
    # Fetch the Ispark location from the database
    ispark = session.query(Ispark).get(id)
    if ispark:
        lat = ispark.latitude
        lon = ispark.longitude
        color = colorOfMarker(ispark.park_type_desc)
        ispark_name = ispark.park_name

        # Create a Folium map centered at the Ispark location
        map = folium.Map(location=[lat, lon], zoom_start=12)
        distance = get_distance(
            lat, lon, getCurrentLocation()[0], getCurrentLocation()[1]
        )

        fgp = folium.FeatureGroup(name="targetpoint")

        fgp.add_child(folium.Marker([lat, lon],
            popup=f"<h1>{ispark_name}</h1><img src='/static/images/ispark.png' width='100px'><p>{distance} kilometers away.</p>",
            tooltip=f"<h4>{ispark.park_type_desc}</h4><p>Latitude: {lat}</p> <p>Longitude: {lon}</p>",
            icon=folium.Icon(color=color),))
        
        map.add_child(fgp)
        map.save("templates/ispark_map.html")


        # Render the template with the Ispark data and map path
        return render_template("ispark_map.html", ispark=ispark, lat=lat, lon=lon)
    return "Ispark location not found", 404


if __name__ == "__main__":
    app.run(debug=True)
