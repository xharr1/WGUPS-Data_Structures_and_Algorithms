from Truck import Truck
from datetime import time
from DirectHashTable import DirectHashTable

# Package class to hold package details
class Package:
    # Initialization for items from WGUPS Package file, and additional variables required for tracking
    def __init__(self, id, address, city, state, zip, deadline, weight, note='',
                 truck=-1, delivery_time=None):
        self.id = id  # Package ID
        self.address = address  # Address
        self.city = city  # City
        self.state = state  # State
        self.zip = zip  # Zip
        self.deadline = deadline  # Delivery Deadline
        self.weight = weight  # Weight KILO
        self.note = note  # Special Note
        self.truck = truck  # assigned number once on truck - new (not in WGUPS package file)
        self.delivery_time = delivery_time  # Delivered timestamp - new (not in WGUPS package file)

    # Details and formatting for use as a string.
    def __str__(self):
        full_address = f'{self.address}, {self.city}, {self.state}, {self.zip}'
        return (f'{self.id:>10} | {full_address:<67} | '
                f'{self.weight:>3}kgs | {self.truck:>5} | {self.deadline:<8}')

    # Lookup function to print string details above and calculate the correct status
    def lookup(self, check_time: time, trucks: DirectHashTable):
        truck: Truck = trucks.search(self.truck)
        if self.delivery_time < check_time:
            print(f'{self} | Delivered at {self.delivery_time}')
        elif truck.departure_time > check_time:
            print(f'{self} | At the hub')
        else:
            print(f'{self} | En Route')
