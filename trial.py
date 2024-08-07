import requests

def getCurrentLocation():
    url = "https://www.googleapis.com/geolocation/v1/geolocate?key={}".format(
        "AIzaSyBTDU0W-s7dcbVOcSjkKQ71kPmr33kKgMc"
    )

    response = requests.post(url)

    if response.status_code == 200:
        location_data = response.json()
        print(location_data["location"]["lat"])
        print(location_data["location"]["lng"])
        get_address(
            "AIzaSyBTDU0W-s7dcbVOcSjkKQ71kPmr33kKgMc",
            location_data["location"]["lat"],
            location_data["location"]["lng"],)
        return (location_data["location"]["lat"], location_data["location"]["lng"])
    else:
        print("Error:", response.status_code, response.text)
        return None


def get_address(api_key, latitude, longitude):
    # Construct the URL for the Geocoding API
    url = "https://maps.googleapis.com/maps/api/geocode/json"

    # Define the parameters for the request
    params = {"latlng": f"{latitude},{longitude}", "key": api_key}

    # Make the request to the Geocoding API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if results are found
        if data["status"] == "OK" and len(data["results"]) > 0:
            # Extract the formatted address from the results
            address = data["results"][0]["formatted_address"]
            print(address)
            return address
        else:
            return "No results found"
    else:
        return f"Request failed with status code {response.status_code}"


getCurrentLocation()