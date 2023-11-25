from datetime import time
from Truck import Truck
from DirectHashTable import DirectHashTable


# Loops through items and prints them. It is in 2 different parts of the interface, and was pulled out to save space.
def interface_loop(package_table, trucks, check_time):
    truck1_packages = []
    truck2_packages = []
    truck3_packages = []
    delivered = []
    column_names = f'\033[1mPackage ID | {'Address':<67} | Weight | Truck | Deadline | Status\033[0m'
    # Adds each package to a corresponding list of what truck it was on, or if it was delivered.
    for i in range(1, 41):
        cur_package = package_table.search(i)
        if cur_package.delivery_time < check_time:
            delivered.append(cur_package.id)
        elif cur_package.truck == 1:
            truck1_packages.append(cur_package.id)
        elif cur_package.truck == 2:
            truck2_packages.append(cur_package.id)
        else:
            truck3_packages.append(cur_package.id)
    print()
    # Loops through each delivered item and prints its id, status/delivery time, and deadline.
    print('Delivered items:')
    print(column_names)
    for package_id in delivered:
        cur_package = package_table.search(package_id)
        cur_package.lookup(check_time, trucks)
    # Loops through each truck's items and prints its id, status, and deadline.
    truck_packages = (truck1_packages, truck2_packages, truck3_packages)
    for i in range(len(truck_packages)):
        truck_number = i + 1
        cur_truck_packages = truck_packages[i]
        truck = trucks.search(truck_number)
        if cur_truck_packages:
            print()
            print(f'Packages on truck {truck_number}:')
            print(column_names)
            for package_id in cur_truck_packages:
                cur_package = package_table.search(package_id)
                cur_package.lookup(check_time, trucks)


# This is the user interface. It prints the total miles traveled, asks the user for a time to check, and returns package
# data for that time. It continues to ask for input until -1 is input.
def interface(package_table: DirectHashTable, trucks: DirectHashTable):
    # The trucks are used to calculate the total miles for menu option 1.
    truck1: Truck = trucks.search(1)
    truck2: Truck = trucks.search(2)
    truck3: Truck = trucks.search(3)
    # Reusable menu text to save space.
    menu_text = ('--------\n'
                 '1. Print all packages and total miles\n'
                 '2. Get a single package with a time\n'
                 '3. Get all packages with a time\n'
                 '4. Exit\n'
                 '--------\n')
    menu_input = '0'
    # The program exits on an input of 4.
    while menu_input != '4':
        menu_input = input(menu_text).strip()
        if menu_input == '4':
            break
        # Ensures that the input is a valid menu option.
        elif menu_input != '1' and menu_input != '2' and menu_input != '3':
            print('Please choose a valid option')
            continue
        # 1. Print all packages and total miles.
        elif menu_input == '1':
            print(f'Total miles: {format(truck1.miles + truck2.miles + truck3.miles, ".1f")}')
            # Time is needed for the lookup function. 23:00 is at the end of the day and will return all delivery times.
            check_time = time(hour=23)
            interface_loop(package_table, trucks, check_time)
            print()
            continue
        # 2. Get a single package with a time.
        elif menu_input == '2':
            package_input = input('Enter a package id between 1 and 40 to check. ')
            package_id = -1
            check_time = time(hour=0)
            # This makes sure the input is a valid package id between 1 and 40 and doesn't error out.
            while True:
                try:
                    package_id = int(package_input)
                except Exception:
                    package_input = input('Invalid package id (1-40) input. Please input a valid id. ')
                    continue
                if package_id < 1 or package_id > 40:
                    package_input = input('Invalid package id (1-40) input. Please input a valid id. ')
                    continue
                else:
                    break
            time_input = input('Enter a time to check (HH:MM). ')
            # This makes sure the input is a time and doesn't error out.
            while True:
                try:
                    temp_time = time_input.split(':')
                    check_time = time(hour=int(temp_time[0]), minute=int(temp_time[1]))
                except Exception:
                    time_input = input('Invalid time input (HH:MM). Please input a valid time. ')
                    continue
                break
            package = package_table.search(package_id)
            print()
            print(f'\033[1mPackage ID | {'Address':<67} | Weight | Truck | Deadline | Status\033[0m')
            package.lookup(check_time, trucks)
            print()
        # 3. Get all packages with a time.
        elif menu_input == '3':
            time_input = input('Enter a time to check (HH:MM). ')
            check_time = time(hour=0)
            # This makes sure the input is a time and doesn't error out.
            while True:
                try:
                    temp_time = time_input.split(':')
                    check_time = time(hour=int(temp_time[0]), minute=int(temp_time[1]))
                except Exception:
                    time_input = input('Invalid time input (HH:MM). Please input a valid time. ')
                    continue
                break
            interface_loop(package_table, trucks, check_time)
            print()