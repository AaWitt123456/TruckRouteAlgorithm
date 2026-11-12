import datetime
#creates packages class
class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline_time, weight, status, truck_number=None):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None
        self.truck_number = truck_number
        self.truck_number = None
#makes packages able to be printed as a string
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (
            self.ID,
            self.address,
            self.city,
            self.state,
            self.zipcode,
            self.deadline_time,
            self.weight,
            self.delivery_time,
            self.status
        )
    def short_package(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (
            self.ID,
            self.address,
            self.city,
            self.state,
            self.zipcode,
            self.deadline_time,
            self.weight,
            self.delivery_time,
        )



#this is for updating table
    def update_status(self, convert_timedelta):
#at 10:20 address gets updated so this changes the address
        if self.ID == 9 and convert_timedelta >= datetime.timedelta(hours=10, minutes=20):
            self.address = "410 S State St"
            self.zipcode = "84111"

#changes whether package is delivered or not

        if self.delivery_time < convert_timedelta:
            self.status = "Delivered"
        elif self.departure_time > convert_timedelta:
            self.status = "At Hub"
        else:
            self.status = "En Route"