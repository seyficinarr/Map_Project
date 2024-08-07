import requests
import psycopg2


def upload_data_to_db():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host="localhost", database="map_app", user="postgres", password="Aseyfo58"
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Define the SQL query for inserting data
        create_query = """
        INSERT INTO ispark_second (id, name, lat, lng, capacity, work_hours, park_type, district)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Fetch data from the API
        url = "https://api.ibb.gov.tr/ispark/Park"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Iterate over the JSON data and insert into the database
        for item in data:  # Assuming `data` is a list of dictionaries
            values = (
                item.get("parkID"),
                item.get("parkName"),
                item.get("lat"),
                item.get("lng"),
                item.get("capacity"),
                item.get("workHours"),
                item.get("parkType"),
                item.get("district"),
            )
            cursor.execute(create_query, values)

        # Commit the transaction
        connection.commit()

    except (psycopg2.Error, requests.RequestException) as e:
        print(f"An error occurred: {e}")
        # Rollback in case of error
        if connection:
            connection.rollback()

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


upload_data_to_db()
