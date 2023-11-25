from DirectHashTable import DirectHashTable
from get_nearest_neighbor import get_nearest_neighbor
from Truck import Truck


# Load trucks starting by manually loading packages with special notes. Then load any packages that have the same
# address as manually loaded packages. Finally, load all remaining packages based on nearest neighbors.
def load_trucks(package_table: DirectHashTable, trucks: DirectHashTable, address_list, distance_list,
                truck1: Truck, truck2: Truck, truck3: Truck):
    # This section will manually load items with special notes onto trucks and put items without special notes into
    # a remaining packages table.
    remaining_packages = []
    for package in package_table.table:
        cur_package = package[1]
        note = str(cur_package.note)
        if cur_package is None:
            continue
        # This groups packages 13, 15, and 19, as well as the packages that must be delivered with 13, 15, and 19.
        # (I assume the notes were meant to go on 13, 15, and 19, but they're on 14, 16, and 20.)
        elif ((cur_package.id == 13 or cur_package == 15 or cur_package == 19)
              or (note == 'Must be delivered with 15, 19'
                  or note == 'Must be delivered with 13, 19'
                  or note == 'Must be delivered with 13, 15')):
            truck2.packages.append(cur_package.id)
            cur_package.truck = 2
            continue
        # Items that can only be on truck 2 go on truck 2.
        elif note == 'Can only be on truck 2':
            truck2.packages.append(cur_package.id)
            cur_package.truck = 2
            continue
        # Load packages with various delays onto truck 3.
        elif (note == 'Delayed on flight---will not arrive to depot until 9:05 am'
              or note == 'Wrong address listed'):
            truck3.packages.append(cur_package.id)
            cur_package.truck = 3
            continue
        # Packages with deadlines go on truck 1, the "express" truck.
        elif cur_package.deadline == '10:30 AM' or cur_package.deadline == '9:00 AM':
            truck1.packages.append(cur_package.id)
            cur_package.truck = 1
            continue
        # Everything else still needs to be sorted and goes in the remaining_packages list.
        elif note == '':
            remaining_packages.append(cur_package.id)
            continue
    # This first loop will load any remaining packages that have the same address as any manually loaded packages. No
    # other packages will be loaded yet.
    for truck in trucks.table:
        cur_truck = truck[1]
        cur_package_list = cur_truck.packages
        i = 0
        # This check avoids errors and skips empty trucks.
        if len(cur_package_list) > 0:
            while i < len(cur_package_list):
                distance = 0.0
                cur_package = package_table.search(cur_package_list[i])
                # This loop has the logic for finding packages at 0.0 distance, meaning the same address.
                while distance == 0.0:
                    nearest_neighbor_info = get_nearest_neighbor(cur_package.address, remaining_packages, package_table,
                                                                 address_list, distance_list)
                    nearest_neighbor = package_table.search(nearest_neighbor_info[0])
                    index = nearest_neighbor_info[1]
                    distance = nearest_neighbor_info[2]
                    if distance == 0.0:
                        cur_truck.packages.append(nearest_neighbor.id)
                        remaining_packages.pop(index)
                        nearest_neighbor.truck = cur_truck.number
                i += 1

    # This will add any remaining packages to the trucks. It starts at 2 as no additional packages will be added to the
    # express truck (number 1).
    k = 2
    while k <= 3:
        cur_truck = trucks.search(k)
        # If the truck isn't empty, it grabs the last package in the list.
        if len(cur_truck.packages) > 0:
            cur_package = package_table.search(cur_truck.packages[((len(cur_truck.packages)) - 1)])
        else:
            cur_package = None
        while len(cur_truck.packages) < cur_truck.max_capacity and len(remaining_packages) > 0:
            # If the truck is empty, start at the hub. Otherwise, get the address from the current package.
            if len(cur_truck.packages) == 0:
                nearest_neighbor_info = get_nearest_neighbor('HUB', remaining_packages, package_table,
                                                             address_list, distance_list)
            else:
                nearest_neighbor_info = get_nearest_neighbor(cur_package.address, remaining_packages,
                                                             package_table, address_list, distance_list)
            # get_nearest_neighbor returns a list of items. This splits the list into individual items.
            nearest_neighbor = package_table.search(nearest_neighbor_info[0])
            index = nearest_neighbor_info[1]
            # Add the package to the truck and remove from remaining packages list.
            cur_truck.packages.append(nearest_neighbor.id)
            remaining_packages.pop(index)
            cur_package = nearest_neighbor
            cur_package.truck = k
        # Remove package 9 from the delivery list. It will be added back once the updated address is received.
        if k == 3:
            cur_truck.packages.remove(9)
            package_table.search(9).truck = -1
        k += 1
