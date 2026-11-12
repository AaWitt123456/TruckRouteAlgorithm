'''

Aaron Wittmus

Student ID: 001384854

C950 Task 2

'''

import csv
import datetime
from datetime import timedelta

import Truck
from builtins import ValueError

from HashTable import CreateHash
from Packages import Package



#These load in the CSV files for later use

with open("WGUPSDistanceTable.csv") as csvfile:
    CSVDistanceTable = csv.reader(csvfile)
    CSVDistanceTable = list(CSVDistanceTable)

with open("WGUPSAddressTable.csv") as csvfile1:
    CSVAddressTable = csv.reader(csvfile1)
    CSVAddressTable = list(CSVAddressTable)

with open("WGUPSPackageFile.csv") as csvfile2:
    CSVPackageFile = csv.reader(csvfile2)
    CSVPackageFile = list(CSVPackageFile)


#Creates package objects loads into the hash table.

def LoadPackageData(filename, PackagesHashTable):
    with open(filename) as PackagesInfo:
        PackageData = csv.reader(PackagesInfo)
        for package in PackageData:
            PackageID = int(package[0])
            PackageAddress = package[1]
            PackageCity = package[2]
            PackageState = package[3]
            PackageZipcode = package[4]
            PackageDeadline = package[5]
            PackageWeight = package[6]
            PackageStatus = "At Hub"


            p = Package(PackageID, PackageAddress, PackageCity, PackageState, PackageZipcode, PackageDeadline, PackageWeight, PackageStatus)

            PackagesHashTable.insert(PackageID, p)



#Finds distance between addresses by looking at row and column in distance table.
def DistanceTableValues(x_value, y_value):
    distance = CSVDistanceTable[x_value][y_value]
    #If the value is blank it will flip the x and y so that it finds the correct value
    if distance == '':
        distance = CSVDistanceTable[y_value][x_value]

    return float(distance)


#grabs address from row 2 of address table
def ExtractAddress(address):
    for row in CSVAddressTable:
        if address in row[2]:
            return int(row[0])



# Creates trucks, they are manually loaded. The packages that need to be delivered earlier are loading into truck 1 which leaves at 8
#some packages need to be on truck 2 and be delivered after 10:20
#some packages must leave after 9:05 so those are on truck 3

truck1 = Truck.Truck(16, 18, None, [1,13,14,15,19,16,20,29,30,31,34,40], 0.0, "4001 South 700 East",datetime.timedelta(hours=8))


truck2 = Truck.Truck(16, 18, None, [3,18,36,38,9,2,4,5,7,8,10,11,12,17,19,21], 0.0,"4001 South 700 East",datetime.timedelta(hours=10, minutes=20))

truck3 = Truck.Truck(16, 18, None, [6,25,28,32,22,23,24,26,27,33,35,37,39], 0.0, "4001 South 700 East",datetime.timedelta(hours=9, minutes=5))

delayed_packages = [6,25,28,32]

#creates hash table
PackageHashTable = CreateHash()


#loads the packages into hash table
LoadPackageData("WGUPSPackageFile.csv", PackageHashTable)


#assigns packages with truck number based on list of truck above.
for packageID in truck1.packages:
    PackageHashTable.search(packageID).truck_number = 1
for packageID in truck2.packages:
    PackageHashTable.search(packageID).truck_number = 2
for packageID in truck3.packages:
    PackageHashTable.search(packageID).truck_number = 3

#Truck delivers packages using nearest neighbor algorithm

def Delivering(truck):
#list of packages that need to be delivered
    NotDelivered = []
#get packages from hash table
    for packageID in truck.packages:
        NotDelivered.append(PackageHashTable.search(packageID))
#clear packages after delivery
    truck.packages.clear()
#continue until all packages are delivered
    while NotDelivered:

        NextAddress = 50
        NextPackage = None
#searches remaining packages and finds distances
        for package in NotDelivered:
            distance = DistanceTableValues(
                ExtractAddress(truck.address),
                ExtractAddress(package.address)
            )
#picks closer destination
            if distance <= NextAddress:
                NextAddress = distance
                NextPackage = package
#adds mileage
        truck.mileage += NextAddress
        #truck moves to new address
        truck.address = NextPackage.address
        #update time based on movement speed of 18 mph
        truck.time += datetime.timedelta(hours=NextAddress / 18)

#list of delivered packages
        delivered = []
#deliver every package that goes to this address
        for package in NotDelivered:
            #checks packages addresses
            if package.address == NextPackage.address:
                #records depart time and delivery time
                package.delivery_time = truck.time
                package.departure_time = truck.depart_time

                truck.packages.append(package.ID)
                delivered.append(package)

#after delivery removes them from not delivered list
        for package in delivered:
            NotDelivered.remove(package)





#starts delivering the trucks

Delivering(truck1)

Delivering(truck3)

#truck 2 waits until another truck returns since there are only 2 drivers.

truck2.depart_time = min(truck1.time, truck3.time)

Delivering(truck2)




#this is the user interface portion
#asks for input and if input is incorrect it asks you to try again

class Main:
    while True:
        print("\n\nWestern Governors University Parcel Service")
        print("Total Mileage:",truck1.mileage + truck2.mileage + truck3.mileage)
        while True:
            try:
                firstinput = input("\nPlease enter a time to check package status in HH:MM:SS format.")
                (h, m, s) = firstinput.split(":")
                convert_timedelta = datetime.timedelta(
                    hours=int(h),
                    minutes=int(m),
                    seconds=int(s)
                )
                break
            except ValueError:
                print("\nInvalid.")

        while True:
            secondinput = input("To view the status of one package type 'single', to see all packages type 'all': ")
#if type all user gets status list of all packages at time they entered
            if secondinput == "all":
                for packageID in range(1, 41):
                    package = PackageHashTable.search(packageID)
                    package.update_status(convert_timedelta)
#This checks if package is in list of delayed packages, and if it is after 9:05 when they arrive it will start to display normally otherwise says not recieved
                    if package.ID in delayed_packages and convert_timedelta < datetime.timedelta(hours=9, minutes=5):
                        print(package.short_package(), "Package not yet received")
                    else:
                        print(package, "Truck:", package.truck_number)
                break
#if using single will be prompted to type number for package and will get response for package at given time or error if input is incorrect
            elif secondinput == "single":
                try:
                    solo_input = input("Enter the package ID: ")
                    package = PackageHashTable.search(int(solo_input))

                    if package is None:
                        print("There is no package with that ID.")
                    else:
                        package.update_status(convert_timedelta)
                        if package.ID in delayed_packages and convert_timedelta < datetime.timedelta(hours=9, minutes=5):
                            print(package.short_package(), "Package not yet received")
                        else:
                            print(package, "Truck:", package.truck_number)
                        break

                except ValueError:
                    print("Please enter a number for package ID.")
            else:
                print("Invalid entry. Please type 'single' or 'all'.")
                #restarts program if desire to check other program.
        while True:
            restart = input(
                "\nWould you like to check another package? Type 'yes' to restart or 'no' to end: "
            ).lower()

            if restart == "yes":
                break

            elif restart == "no":
                print("\nFinished!")
                exit()

            else:
                print("Invalid entry. Please type 'yes' or 'no'.")




