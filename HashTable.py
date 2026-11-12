class CreateHash:

#create hash table with range 40 since only 40 packages
    def __init__(self):
        self.table = [[] for _ in range(40)]

#gives bucket for a given key
    def GetBucket(self, key):
        return key % len(self.table)

#inserts into hash table
    def insert(self, key, item):

        bucket = self.GetBucket(key)
        BucketList = self.table[bucket]

        #check if key exists
        for pair in BucketList:
            if pair[0] == key:
                pair[1] = item
                return

        #add new key value pair
        BucketList.append([key, item])

    #Search for a key and return the value
    def search(self, key):

        bucket = self.GetBucket(key)

        for stored_key, stored_item in self.table[bucket]:
            if stored_key == key:
                return stored_item

        return None

    #Remove key-value pair
    def remove(self, key):

        bucket = self.GetBucket(key)
        BucketList = self.table[bucket]

        for pair in BucketList:
            if pair[0] == key:
                BucketList.remove(pair)
                return True

        return False

