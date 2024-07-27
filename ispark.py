class ispark:
    def __init__(
        self,
        park_name,
        location_name,
        park_type_id,
        park_type_desc,
        capacity_of_park,
        working_time,
        county_name,
        longitude,
        latitude,
        location,
    ):
        self.park_name = park_name
        self.location_name = location_name
        self.park_type_id = park_type_id
        self.park_type_desc = park_type_desc
        self.capacity_of_park = capacity_of_park
        self.working_time = working_time
        self.county_name = county_name
        self.longitude = longitude
        self.latitude = latitude
        self.location = location

    def get_park_name(self):
        return self.park_name

    def set_park_name(self, value):
        self.park_name = value

    def get_location_name(self):
        return self.location_name

    def set_location_name(self, value):
        self.location_name = value

    def get_park_type_id(self):
        return self.park_type_id

    def set_park_type_id(self, value):
        self.park_type_id = value

    def get_park_type_desc(self):
        return self.park_type_desc

    def set_park_type_desc(self, value):
        self.park_type_desc = value

    def get_capacity_of_park(self):
        return self.capacity_of_park

    def set_capacity_of_park(self, value):
        self.capacity_of_park = value

    def get_working_time(self):
        return self.working_time

    def set_working_time(self, value):
        self.working_time = value

    def get_county_name(self):
        return self.county_name

    def set_county_name(self, value):
        self.county_name = value

    def get_longitude(self):
        return self.longitude

    def set_longitude(self, value):
        self.longitude = value

    def get_latitude(self):
        return self.latitude

    def set_latitude(self, value):
        self.latitude = value

    def get_location(self):
        return self.location

    def set_location(self, value):
        self.location = value
