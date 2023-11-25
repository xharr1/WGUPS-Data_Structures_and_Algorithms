from DirectHashTable import DirectHashTable


# Takes an address and searches the address list for it's corresponding id.
def get_address_id(address, address_list):
    i = 0
    while i < len(address_list):
        current_address = address_list[i]
        if address == current_address[1]:
            return int(current_address[0])
        i += 1
    return None


# Gets the distance between two locations.
def get_distance(address_id_1, address_id_2, distance_list):
    distance = distance_list[address_id_1][address_id_2]
    if distance == '':
        distance = distance_list[address_id_2][address_id_1]
    return float(distance)


# Compares an address against a list of addresses to find the shortest distance.
# Returns the package id of the nearest neighbor, index of the neighbor, and the distance to the neighbor.
def get_nearest_neighbor(address, package_list, package_table: DirectHashTable, address_list, distance_list):
    address_id = get_address_id(address, address_list)
    shortest_distance = -1.0
    nearest_neighbor = -1
    index = -1
    i = 0
    while i < len(package_list):
        package = package_table.search(package_list[i])
        compare_id = get_address_id(package.address, address_list)
        temp_distance = float(get_distance(int(address_id), int(compare_id), distance_list))
        # Checks at -1.0 instead of 0.0 so that the algorithm find packages at the same address
        if (shortest_distance == -1.0) or (temp_distance < shortest_distance):
            shortest_distance = temp_distance
            nearest_neighbor = package.id
            index = i
        i += 1
    return [nearest_neighbor, index, float(shortest_distance)]
