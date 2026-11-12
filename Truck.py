class Truck:

#creates truck object
    def __init__(self, capacity, speed, driver, packages, mileage, address, departtime):
        self.capacity = capacity
        self.speed = speed
        self.driver = driver
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart_time = departtime
        self.time = departtime
#string of truck object for printing truck info
    def __str__(self):
        return  "%s, %s, %s, %s, %s, %s, %s" % (
            self.capacity,
            self.speed,
            self.driver,
            self.packages,
            self.mileage,
            self.address,
            self.depart_time
        )
