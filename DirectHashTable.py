# Prime functions used for resizing hash table
# From https://stackoverflow.com/questions/60003330/find-the-next-prime-number-in-python
def is_prime(x):
    return all(x % i for i in range(2, x))


def next_prime(x):
    return min([a for a in range(x+1, 2*x) if is_prime(a)])


# Altered from W-1_ChainingHashTable_zyBooks_Key-Value.py
# HashTable class using direct hashing
class DirectHashTable:
    # Constructor with optional initial capacity parameter
    def __init__(self, initial_capacity=40):
        # Initialize the hash table with empty bucket list entries
        self.table = [None] * initial_capacity

    # Inserts a new item into the hash table.
    def insert(self, key, item):
        # Get the bucket where the item will go
        bucket = hash(key) % len(self.table)
        key_value = [key, item]
        # If bucket is empty insert key-value pair
        if self.table[bucket] is None:
            self.table[bucket] = key_value
        # If the new key already exists, update the value
        elif self.table[bucket][0] == key:
            self.table[bucket][1] = item
        # If the bucket has another key, resize the table and recursively insert
        else:
            self.hash_resize(len(self.table))
            self.insert(key, item)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # Get the bucket where the key would be
        bucket = hash(key) % len(self.table)
        key_value = self.table[bucket]
        # Verify if the bucket is empty
        if key_value is None:
            return None
        # If the bucket is not empty
        else:
            value = key_value[1]
            return value

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # Get the bucket where this item will be removed from and remove the key-value pair.
        bucket = hash(key) % len(self.table)
        self.table[bucket] = None

    # Developed using the pseudocode from C949: Data Structures and Algorithms I 15.6: Hash table resizing.
    # Resize the hash table
    def hash_resize(self, cur_size):
        # Multiply the current size by 2 and get the next prime and create a temporary hash table the size of the prime.
        new_size = next_prime(cur_size * 2)
        new_array = DirectHashTable(new_size)

        bucket = 0
        # Iterate over every bucket and insert items into temporary hash table.
        while bucket < cur_size:
            key_value = self.table[bucket]
            if key_value is not None:
                new_array.insert(key_value[0], key_value[1])
            bucket += 1
        # Copy the new larger hash table to the original table
        self.table = new_array.table
