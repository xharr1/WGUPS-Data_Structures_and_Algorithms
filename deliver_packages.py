from datetime import datetime, time, timedelta, date
from Truck import Truck
from get_nearest_neighbor import get_nearest_neighbor, get_distance, get_address_id
from DirectHashTable import DirectHashTable


# Goes through each truck and delivers each package using the nearest neighbor algorithm
def deliver_packages(package_table: DirectHashTable, trucks: DirectHashTable, addr_list, dist_list,
                     truck1: Truck, truck2: Truck, truck3: Truck):
    temp_date = date(1, 1, 1)
    i = 1
    while i <= 3:
        cur_truck = trucks.search(i)
        while len(cur_truck.packages) > 0:
            # get_nearest_neighbor returns a list of items. This splits the list into individual items.
            nearest_neighbor_info = get_nearest_neighbor(cur_truck.cur_location, cur_truck.packages, package_table,
                                                         addr_list, dist_list)
            nearest_neighbor = package_table.search(nearest_neighbor_info[0])
            index = nearest_neighbor_info[1]
            distance = nearest_neighbor_info[2]
            # This only adds miles and time to the truck if it moves to a new address, effectively delivering all
            # packages with the same address at the same time.
            if distance > 0.0:
                cur_truck.miles += distance
                # I had trouble with the time calculations. I referred to this stackoverflow post for help. Create a
                # datetime object, add the time delta, then get the time back out.
                # (https://stackoverflow.com/questions/12448592/how-to-add-delta-to-python-datetime-time)
                delta = timedelta(hours=distance/cur_truck.speed)
                cur_truck.cur_time = (datetime.combine(temp_date, cur_truck.cur_time) + delta).time()
            cur_truck.cur_location = nearest_neighbor.address
            nearest_neighbor.delivery_time = cur_truck.cur_time
            nearest_neighbor.status = 'delivered'
            cur_truck.packages.pop(index)
            # This handles package 9 that has the incorrect address until 10:20. It adds it to truck 3's delivery route
            # if it is past 10:20, or if it is the last package. If it is the last package, wait for the updated address
            # before delivering.
            if i == 3:
                package9 = package_table.search(9)
                if (package9.delivery_time is None and package9.truck == -1
                        and (len(cur_truck.packages) == 0 or cur_truck.cur_time > time(hour=10, minute=20))):
                    cur_truck.packages.append(9)
                    package9.truck = 3
                    if cur_truck.cur_time < time(hour=10, minute=20):
                        cur_truck.cur_time = time(hour=10, minute=20)
                    package9.address = '410 S State St'
            # If the truck is empty, return to the hub. The hub's id is 0.
            if len(cur_truck.packages) == 0:
                hub_distance = get_distance(0, get_address_id(cur_truck.cur_location, addr_list), dist_list)
                cur_truck.miles += hub_distance
                hub_delta = timedelta(hours=hub_distance / cur_truck.speed)
                cur_truck.cur_time = (datetime.combine(temp_date, cur_truck.cur_time) + hub_delta).time()
                cur_truck.cur_location = 'HUB'
                # Since there are 3 trucks but only 2 drivers, we need to make sure the 3rd truck doesn't leave until
                # one of the first 2 trucks returns. If both trucks get back after the third truck's start time, updates
                # the start time to the first of the 2 to return.
                if i == 2:
                    if truck3.cur_time < truck1.cur_time and truck3.cur_time < truck2.cur_time:
                        if truck1.cur_time < truck2.cur_time:
                            truck3.cur_time = truck1.cur_time
                            truck3.departure_time = truck1.cur_time
                        else:
                            truck3.cur_time = truck2.cur_time
                            truck3.departure_time = truck2.cur_time
        i += 1
