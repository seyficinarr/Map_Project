import geocoder
import psycopg2
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


def getCurrentLocation():
    g = geocoder.ip("me")  # Use 'me' to get the location based on your IP
    print(reverse_geocode(g.latlng[0], g.latlng[1]))
    return (
        g.latlng if g.latlng else (None, None)
    )  # Return None if location is not available


def reverse_geocode(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        # Perform reverse geocoding
        location = geolocator.reverse((latitude, longitude), timeout=10)

        # Check if a location was found
        if location:
            return location.address
        else:
            return "Address not found"
    except GeocoderTimedOut:
        return "Geocoding service timed out"
    except Exception as e:
        return f"An error occurred: {e}"


def get_distance(lat1, lon1, lat2, lon2):
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return None  # Return None if any coo   rdinate is missing

    # Create tuples for the coordinates
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)

    try:
        # Calculate the distance
        distance = geodesic(coord1, coord2).kilometers
        return distance
    except ValueError as e:
        print(f"Error calculating distance: {e}")
        return None


def getClosestIspark():
    curLoc = getCurrentLocation()
    if curLoc[0] is None or curLoc[1] is None:
        print("Unable to get current location.")
        return None

    curLatitude, curLongitude = curLoc

    connection = psycopg2.connect(
        host="localhost", database="map_app", user="postgres", password="Aseyfo58"
    )
    cursor = connection.cursor()

    select_query = """
    SELECT park_name, latitude, longitude 
    FROM ispark
    """

    min_distance = float("inf")
    min_distance_ispark = None
    count_invalid_coords = 0

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
            count_invalid_coords += 1
            continue
        distance = get_distance(
            curLatitude, curLongitude, ispark_latitude, ispark_longitude
        )
        if distance is not None and distance < min_distance:
            min_distance = distance
            min_distance_ispark = r

    cursor.close()
    connection.close()

    print(f"Invalid coordinates count: {count_invalid_coords}")

    if min_distance_ispark:
        return [min_distance_ispark, min_distance]
    else:
        return [None, None]


closest_ispark = getClosestIspark()
if closest_ispark[0]:
    closest_ispark_name = closest_ispark[0][0]
    latitude, longitude = closest_ispark[0][1], closest_ispark[0][2]
    distance = closest_ispark[1]
    print("Closest ispark:", closest_ispark_name)
    print("Closest ispark's latitude and longitude:", latitude, longitude)
    print("The distance is:", distance)
else:
    print("No valid ispark found.")
