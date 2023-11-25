# Author: Harrison Plummer
# Student ID: 010186537
# Title: WGUPS Project Task 2

import csv
from datetime import time
import DirectHashTable
import Package
from Truck import Truck
from load_trucks import load_trucks
from deliver_packages import deliver_packages
from interface import interface

# The following section loads data from csv files into lists or a has table depending on the data.
# Get addresses from csv file and put in a list.
with open('csv/address.csv') as csv_address:
    address_list = csv.reader(csv_address)
    address_list = list(address_list)

# Get distances from csv file and put in a list.
with open('csv/distance.csv') as csv_distance:
    distance_list = csv.reader(csv_distance)
    distance_list = list(distance_list)

# Create hash table instance for package data.
package_table = DirectHashTable.DirectHashTable()

# Get package info from csv file.
with open('csv/package.csv') as csv_package:
    package_csv = csv.reader(csv_package)
    # Put package data in a package object and load into hash table.
    for row in package_csv:
        temp_package = Package.Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        package_table.insert(int(row[0]), temp_package)

# Define the three trucks, number them, and create a hash table to store them. Truck 3 also has a start time of 9:05
# since it will be loaded with the delayed packages.
truck1 = Truck(1, [])
truck2 = Truck(2, [])
truck3 = Truck(3, [], time(hour=9, minute=5), time(hour=9, minute=5))
trucks = DirectHashTable.DirectHashTable(3)
trucks.insert(truck1.number, truck1)
trucks.insert(truck2.number, truck2)
trucks.insert(truck3.number, truck3)

# Load trucks and deliver packages
load_trucks(package_table, trucks, address_list, distance_list, truck1, truck2, truck3)
deliver_packages(package_table, trucks, address_list, distance_list, truck1, truck2, truck3)
interface(package_table, trucks)
