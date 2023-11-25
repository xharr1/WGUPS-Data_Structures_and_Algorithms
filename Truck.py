import datetime


# Class to hold truck details
class Truck:
    # Initialization with variables needed for tracking and algorithm
    def __init__(self, number, packages, cur_time=datetime.time(hour=8), departure_time=datetime.time(hour=8),
                 speed=18.0, max_capacity=16, miles=0.0, cur_location='HUB'):
        self.number = number  # Used for identification
        self.packages = packages  # List of packages in truck
        self.cur_time = cur_time  # Used to track the trucks progress, and EOD time.
        self.departure_time = departure_time  # Used for checking status at hub vs en route.
        self.speed = speed
        self.max_capacity = max_capacity  # Max number of packages
        self.miles = miles  # Mileage tracker
        self.cur_location = cur_location
