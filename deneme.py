import geocoder
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Get current location using geocoder
g = geocoder.ip("me")
geolocator = Nominatim(user_agent="geoapiExercises")


def reverse_geocode(latitude, longitude):
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


# Check if location data is available
if g.ok:
    print(f"Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}")
    address = reverse_geocode(g.latlng[0], g.latlng[1])
    print(f"Address: {address}")
else:
    print("Location not found")
