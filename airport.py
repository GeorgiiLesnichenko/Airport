# Import modules
import re
import csv
from time import sleep

# Open Airports.txt
airportsCSV = open('Airports.txt', 'r')  # Open file
csvreader = csv.reader(airportsCSV)  # Load file into CSV module
airports = []  # empty array for data
for row in csvreader:  # Loop over rows
    airports.append(row)  # Add rows to array


# Open Aircraft.txt
airportsCSV = open('Aircraft.txt', 'r')  # Open file
csvreader = csv.reader(airportsCSV)  # Load file into CSV module
aircraft = []  # empty array for data
for row in csvreader:  # Loop over rows
    aircraft.append(row)  # Add rows to array
nums = r"[+-]?[\d.]+"
aircrafts = []
for sublist in aircraft: # convert str to int
    newsub = []
    for value in sublist:
        if re.match( nums, value ):
            if '.' not in value:
                newsub.append( int(value) )
            else:
                value = value.rstrip('0').rstrip('.')
                if '.' not in value:
                    newsub.append( int(value) )
                else:
                    newsub.append( float(value) )
        else:
            newsub.append( value )
    aircrafts.append( newsub ) # Add int to array


airportDetails = None  # Initialise with empty values
flightDetails = None


class GetAirportDetails():
    def getAirportDetails(self, airportData):
        self.airportData = airportData
        try:  # Get first 3 letters of input and make uppercase.
            ukAirport = input("Enter the three-letter a UK airport code [LPL|BOH]")[0:3].upper()
            if ukAirport != "LPL" and ukAirport != "BOH":
                raise ValueError
            overseasAirport = input(
                "Enter the three-letter an overseas airport code [JFK|ORY|MAD|AMS|CAI]")[0:3].upper()
            isValid = False
            for airport in airportData:  # Search airportData for code
                if overseasAirport == airport[0]:
                    isValid = True
                    print(airport[1] + " has been selected.")
                    return [ukAirport, airport]  # Return for use later
            if isValid == False:  # Code wasn't found in airportData
                print("No valid airport was entered. Returning to menu.")
        except:  # Handle errors from invalid input
            print("Input was invalid. Return to menu.")


class GetFlightDetails():
    def getFlightDetails(self,aircraftData):
        self.airportData = aircraftData
        print("Available aircraft types:")
        for count, aircraft in enumerate(aircraftData):  # Loop over aircraft
            print(str(count + 1) + ". " +
                  aircraft[0])  # Print numbered list of aircraft
        try:  # Handle inputs as in mainMenu
            option = input("Please choose an option: [1-" +
                           str(len(aircraftData)) +
                           "] ")  # Dynamically change max input
            option = int(option)
            if option < 1 or option > len(
                    aircraftData):  # Handle input out of range
                raise ValueError
        except:
            print("Input was invalid. Returning to menu.")
            return None  # Leave the function

        labels = [
            "Type", "Running cost/seat/100km", "Max flight range (km)",
            "Capacity (all standard seats)", "Min 1st class seats"
        ]
        aircraft = aircraftData[option - 1]  # Store selected aircraft
        print("\nAircraft selected:")
        for count, detail in enumerate(aircraft):  # Loop over selected aircraft
            print(labels[count] + ": " + str(detail))  # Print details of aircraft
       
        lowHigh = ''  # Must be declared to handle exceptions like Ctrl+C2
        try:

            option = input("\nEnter number of 1st class seats: (" +
                           str(aircraft[4]) + " - " + str(int(aircraft[3])) +
                           ") ")  # Calculate seat ranges
            option = int(option)
            if option < aircraft[4]:  # Raise error if too low
                lowHigh = "low"
                raise ValueError
            elif option > aircraft[3] / 2:  # Raise error if too high
                lowHigh = "high"
                raise ValueError
            firstSeats = option
            standardSeats = aircraft[3] - firstSeats * 2
            print("No. of 1st class seats: " + str(firstSeats))
            print("No. of standard seats: " + str(standardSeats))
            return [aircraft, firstSeats, standardSeats]  # Return for use later
        except:  # Handle exceptions
            if lowHigh == '':  # Handle other errors than too high/low
                print("Input was invalid.")
            else:
                print("Value entered was too " + lowHigh + ". Returning to menu.")


class GetPricePlan():
    def getPricePlan(self, airportDetails, flightDetails):
        self.airportDetails = airportDetails
        self.flightDetails = flightDetails
        try:  # Check data is ready for this stage
            if airportDetails == None:
                print("Airport details weren't entered.")
                raise ValueError
            if flightDetails == None:
                print("Flight details weren't entered.")
                raise ValueError
            # Tells the next line where to look for the flight distance
            ukAirportCheck = 2 if airportDetails[0] == 'LPL' else 3
            flightDistance = int(airportDetails[1][ukAirportCheck])
            if flightDetails[0][2] < flightDistance:
                print("Selected plane's range is too short.")
                raise ValueError
        except ValueError:
            print("Returning to main menu")
            return None  # Leave the function
        try:
            stdSeatPrice = float(
                input("Enter the price of a standard-class seat: (range 300-500£)"))
            firstSeatPrice = float(
                input("Enter the price of a first-class seat: (range 1200 -1500£)"))
            # Calculate costs with given formulae
            costPerSeat = flightDetails[0][1] * flightDistance / 100
            flightCost = costPerSeat * (flightDetails[1] + flightDetails[2])
            flightIncome = (flightDetails[1] *
                            firstSeatPrice) + (flightDetails[2] * stdSeatPrice)
            flightProfit = flightIncome - flightCost
            # Print the calculated values formated to 2dp.
            print("Flight cost/seat: £{:.2f}".format(costPerSeat))
            print("Flight cost:      £{:.2f}".format(flightCost))
            print("Flight income:    £{:.2f}".format(flightIncome))
            print("Flight profit:    £{:.2f}".format(flightProfit))
        except:
            print("Input was invalid, returning to menu.")

    # Create menu
class Menu():
    def mainMenu(self):
        global airportDetails  # Open as global for persistance
        global flightDetails  # once menu has run
        print("\n*******************************")
        print("Menu")
        print("*********************************")
        print("1. Enter airport details")
        print("2. Enter flight details")
        print("3. Enter price plan & calculate profit")
        print("4. Clear data")
        print("5. Quit")
        try:
            option = input("Please choose an option: [1-5] ")
            option = int(option[0])  # Check that input was an integer
            if option < 1 or option > 5:  # Check that integer is valid
                raise ValueError
        except SystemExit:  # Handle Ctrl+C and similar.
            return "quit"
        except:  # invalid input
            print("The option does not exist")

        if option == 1:
            g = GetAirportDetails()
            airportDetails = g.getAirportDetails(airports)
        elif option == 2:
            j = GetFlightDetails()
            flightDetails = j.getFlightDetails(aircrafts)
        elif option == 3:
            p = GetPricePlan()
            p.getPricePlan(airportDetails, flightDetails)
        elif option == 4:
            print("Clearing data...")
            airportDetails = None  # Reset to initial values
            flightDetails = None
        elif option == 5:
            return "quit"  # Returning 'quit' exits the main program loop
while True:
    r = Menu()
    loopState = r.mainMenu()  # Run the menu (which runs the other options)
    if loopState == "quit":
        break  # Break out of the loop (to quit, see below)
    sleep(1.5)  # Add pause so text can be read more easily

try:
    quit()  # Quit by raising SystemExit
except SystemExit:  # Handle SystemExit gracefully
    print("See you next time")




