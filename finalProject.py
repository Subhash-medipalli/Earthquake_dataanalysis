'''
Program Title: Final Project
Author : Subhash Medipalli
File Name : finalProject.py
Program : The program analysis user input related to an earthquake, explosion, 
nuclear explosion, or rock burst, conducts an analysis, and generates sets of 
data visualizations and graphs and city affected near the radius of the earthquake.
Revisions:
   00 : Import the csv, datetime, math, matplotlib modules
   01 : Define getCityData,coord2rad,havDist,findCities,
        getQuakeData functions
   02 : Prompt the user for selecting the various range of categories 
        for analyzing the earthquake data
   03 : plot the graphs for the selected data and cities affected near location.
   
'''
### Step 00 : Import the required module
import csv
from datetime import datetime as dt
from math import radians, cos, sin, asin, sqrt,floor,ceil
import matplotlib.pyplot as plt


### Step 01 : Defined getCityData,coord2rad,havDist,findCities,getQuakeData functions


def coord2rad(location):
    '''
    

    Parameters
    ----------
    location : coordinates in degrees (tuple: Lat,long)
      

    Returns
    -------
    coordinates : coordinates in radians (dict: Lat, long)
        

    '''
    
    coordinates = {'lat':radians(location[0]),'long':radians(location[1])}
    return coordinates

def havDist(loc1, loc2, unit='km'):
    '''
    

    Parameters
    ----------
    loc1 : coordinates in degrees (tuple: Lat,long)
    loc2 : coordinates in degrees (tuple: Lat,long)
    unit : 'km' for kilometers, otherwise miles

    Returns
    -------
        distance between two locations

    '''
    # convert coordinates tuples to dictionaries in radians
    loc1 = coord2rad(loc1)
    loc2 = coord2rad(loc2)
    # Haversine formula
    dlon = loc2['long'] - loc1['long']
    dlat = loc2['lat'] - loc1['lat']
    a = sin(dlat / 2)**2 + \
        cos(loc1['lat']) * cos(loc2['lat']) * \
        sin(dlon / 2)**2
        
    c = 2 * asin(sqrt(a))
    # Radius of earth kilometers
    r = 6371 if unit == 'km' else 3956 # miles if not km
    # calculate the result
    return (c * r)


def getCityData():
    '''
    Description:
        
    Reads world cities data from a CSV file and processes it into a dictionary.

    Returns
    -------
    new_data : A dictionary where the keys are tuples representing city locations 
    (latitude, longitude),and the values are dictionaries containing city information.

    '''
    
    # Open the CSV file containing world cities data in read mode
    with open("worldcitiesF23.csv","r") as f:
        # Create a CSV DictReader object to read the file as a dictionary
        read = csv.DictReader(f)
        # Convert a everyline into list
        data = [line for line in read]
        # Initializing a new dictionary
        new_data = {}
        for item in data:
            lat = float(item.pop('lat')) # converting string into a float
            lng = float(item.pop('lng')) # converting string into a float
            location = (lat,lng) # create a tuple representing the location
            # Convert population data to integer, setting it to 0 if the value is an empty string
            item['pop'] = 0 if item['pop'] == "" else int(item['pop'])
            new_data[location] = item # Appending data into dictionary
    # Return the final dictionary containing city data which are easy to access
    return new_data
            
cityDict=getCityData()
   
    
def findCities(loc,dic,rad):
    '''
    

    Parameters
    ----------
    loc : A tuple representing the coordinates (latitude, longitude) of the center location.
    dic : A dictionary containing city information where keys are tuples of coordinates
        and values are dictionaries with city details.
    rad : The radius (in kilometers) within which to find cities from the given location.

    Returns
    -------
    nearCities : 
        A list of dictionaries, each containing information about a city within the specified radius.
        Each dictionary includes 'city', 'country', 'pop' (population), and 'distance' from the center.


    '''

    nearCities = []
    for cord,info in dic.items():
        # Calculate the haversine distance between the given location and the city data
        distance = havDist(loc, cord)
        # To check if the city is within the specified radius
        if distance < rad:
            # Append city details to the result list
            nearCities.append({
                'city':info['city'],
                'country':info['country'],
                'pop':info['pop'],
                'distance':round(distance,2)
                })
    return nearCities


def getQuakeData():
    '''
    Reads earthquake data from a CSV file and processes it into a dictionary.


    Returns
    -------
    quakeData : A dictionary where the keys are tuples representing earthquake locations 
    (latitude, longitude), and the values are dictionaries containing earthquake information.

    '''
    
    quakeData = {}
    
    with open('earthquakesF23.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
        
        for d in data:
            
            # Extract latitude and longitude values and create a tuple representing the location
            lat = float(d.pop('Latitude'))
            lng = float(d.pop('Longitude'))
            location = (lat, lng)
            d['Magnitude'] = float(d['Magnitude'])
            # Handling bad values errors for dateTime
            try:
                # Extract date and time, then create a datetime object
                dateTime = dt.strptime(f"{d['Date']} {d['Time']}", '%m/%d/%Y %H:%M:%S')
                
                # Convert Magnitude to float
               
                d['datetime'] = dateTime
                
                # Remove redundant fields
                del d['Date']
                del d['Time']
                
                # Store the data in quakeData with the location as the key
                quakeData[location] = d
                
            except:
                # Modified datetime format according to string
                datetime=dt.strptime(f'{d["Date"]}',"%Y-%m-%dT%H:%M:%S.%fZ")
                del d['Date']
                del d['Time']
                d['datetime'] = datetime
                quakeData[location] =  d
    
    return quakeData




### Step 3 :  Prompt the user for selecting the various range of categories 
###           for analyzing the earthquake data

# Acquire earthquake data using the getQuakeData function
qDict = getQuakeData()

# Extract the mainSelected list, containing tuples of earthquake locations and data
mainSelected = [((lat,lng),v) for (lat,lng),v in qDict.items()]

# Announce
print('\n*** Earthquake Data ***')
print(f"\nAcquired data {len(cityDict)} cities.")
print(f"Acquired data {len(qDict)} earthquakes.")

# Input prompt to decide whether to proceed with data selection
select=input("Confirm 'yes' in order to be selected? ")
tyLst = sorted(list((set(data['Type']for _,data in mainSelected ))))
# Check if the user wants to proceed with data selection
if select == 'yes':
    print("\nSELECT tremor type : ")
    print("Choices are... \nEarthquake, Explosion, Nuclear Explosion, Rock Burst")
    while True:
        # Input prompt to enter the tremor type
        typeCat1=input("Enter values full value or-else first 3 characters : ")
        
        if typeCat1=="":
            # If the input is empty, select all records
            tySelected=list(map(lambda x:x,qDict.items()))
            print("Accepted..")
            tv=f"{tyLst}"
            print(f"{tyLst}")
            print(f"Selected {len(tySelected)} records")
            break
        
        for i in tyLst:
            # Check if the entered tremor type is valid
            if typeCat1 == i[:3] or typeCat1 in i:
                typeCat = i  
                
        if typeCat in tyLst:
            # Filter records based on the selected tremor type
            tySelected=list(filter(lambda x:x[1]['Type']==typeCat,qDict.items()))
            print("Accepted..")
            tv = f'{typeCat}'
            print(f"{typeCat}")
            print(f"Selected {len(tySelected)} records")
            
            # Prompt user to move to latitude selection
            response=input("\nConfirm 'yes' in order to move to latitude? ")
            if response=="yes":
                break
            else:
                continue
        
        else:
            print("Please enter the correct choice")
else:
    # If the user does not want to select data, consider all records
    tySelected=list(map(lambda x:x,qDict.items()))
    tv=f"{tyLst}"
    print("Accepted..")
    print(f"{tyLst}")
    print(f"Selected {len(tySelected)} records")
    

  
# Extract a sorted list of latitudes from the selected earthquake data
latLst = sorted([lat for (lat,lng), _ in tySelected])

print("\nSELECT latitude : Enter two values seperated by comma")
print(f"range is {latLst[0]} through {latLst[-1]}")

# Continuously prompt the user for latitude input
while True:
    try:
        # To get minimum and maximum latitude values from user input
        lat1,lat2=input("\nEnter minimum/maximum latitude values: ").split(",")
        lat1,lat2=float(lat1),float(lat2)
        latMin = min(lat1, lat2)
        latMax = max(lat1,lat2)
        
        # Check if the entered latitude range is within the available data range
        if latLst[0]< latMin and latMax< latLst[-1]:
            latSelected = [((lat,lng),v) for (lat,lng),v in tySelected if latMin < lat < latMax]
            print("Accepted...")
            print({'min':latMin,'max':latMax})
            print(f"Selected {len(latSelected)} records")
            
            # Prompt user to move to longitude selection
            response = input("\nConfirm 'yes' in order to move to longitude? ")
            if response == 'yes':
                break
            else:
                continue
        else:
            print(f"one or more values out of range <({lat1},{lat2})>")
    except:
        # Handle any exceptions and consider all records if input is empty string
        latSelected=[((lat,lng),data) for (lat,lng),data in tySelected]
        print("Accepted...")
        print({'min':latLst[0],'max':latLst[-1]})
        print(f"Selected {len(latSelected)} records")
        
        # Prompt user to move to longitude selection
        response = input("\nConfirm 'yes' in order to move to longitude? ")
        if response == 'yes':
            break
        else:
            continue

# Extract a sorted list of longitudes from the selected earthquake data
lngLst = sorted([lng for (lat,lng), _ in latSelected])

print("\nSELECT longitude : Enter two values seperated by comma")
print(f"range is {lngLst[0]} through {lngLst[-1]}")

while True:
    try:
        # To get minimum and maximum longitude values from user input
        lng1,lng2=input("\nEnter minimum/maximum longitude values: ").split(",")
        lng1,lng2=float(lng1),float(lng2)
        lngMin = min(lng1, lng2)
        lngMax = max(lng1,lng2)
        
        # Check if the entered longitude range is within the available data range
        if lngLst[0]< lngMin and lngMax< lngLst[-1]:
            # Filter earthquake data based on the selected longitude range
            lngSelected = [((lat,lng),v) for (lat,lng),v in latSelected if lngMin < lng < lngMax]
            print("Accepted...")
            print({'min':lngMin,'max':lngMax})
            print(f"Selected {len(lngSelected)} records")
            
            # Prompt user to move to date selection
            response = input("\nConfirm 'yes' in order to move to dates? ")
            if response == 'yes':
                break
            else:
                continue
            break
        else:
            print(f"one or more values out of range <({lng1},{lng2})>")
    except:
        # Handle any exceptions and consider all records if input is empty string
        lngSelected=[((lat,lng),data) for (lat,lng),data in latSelected]
        print("Accepted...")
        print({'min':lngLst[0],'max':lngLst[-1]})
        print(f"Selected {len(lngSelected)} records")
        # Prompt user to move to date selection
        response = input("\nConfirm 'yes' in order to move to dates? ")
        if response == 'yes':
            break
        else:
            continue
    

# Extract a sorted list of dates from the selected earthquake data
dtLst = sorted([data['datetime'].date() for loc, data in lngSelected])
print("\nSELECT date mm/dd/yy: Enter two values seperated by comma")
print(f"range is {dtLst[0]} through {dtLst[-1]}")

# Continuously prompt the user for date input
while True:
    try:
        # Attempt to get minimum and maximum date values from user input
        dt1,dt2 = input("\nEnter minimum/maximum date values: ").split(",")
        dt1,dt2 = dt.strptime(dt1,'%m/%d/%Y'),dt.strptime(dt2,'%m/%d/%Y')
        dt1,dt2 = dt1.date(), dt2.date()
        dtMin = min(dt1,dt2)
        dtMax = max(dt1,dt2)
        
        # Check if the entered date range is within the available data range
        if dtLst[0]< dtMin and dtMax< dtLst[-1]:
            
            # Filter earthquake data based on the selected date range
            dtSelected = [((lat,lng),v) for (lat,lng),v in lngSelected if dtMin <= v['datetime'].date() <= dtMax]
            print("Accepted...")
            d=f"{dt.strftime(dt1,'%m/%d/%Y')} to {dt.strftime(dt2,'%m/%d/%Y')}"
            print({'min':dt.strftime(dt1,'%m/%d/%Y'),
                   'max':dt.strftime(dt2,'%m/%d/%Y')})
            print(f"Selected {len(dtSelected)} records")
            
            # Prompt user to move to magnitude selection
            response = input("\nConfirm 'yes' in order to move to magnitude? ")
            if response == 'yes':
                break
            else:
                continue
            break
        else:
            print(f"one or more values out of range <({dt1},{dt2})>")
            
    except:
        # Handle any exceptions and consider all records if input is empty string
        dtSelected=[((lat,lng),data) for (lat,lng),data in lngSelected]
        d=f"{dt.strftime(dtLst[0],'%m/%d/%Y')} to {dt.strftime(dtLst[-1],'%m/%d/%Y')}"
        print("Accepted...")
        print({'min':dt.strftime(dtLst[0],'%m/%d/%Y'),
               'max':dt.strftime(dtLst[-1],'%m/%d/%Y')})
        print(f"Selected {len(dtSelected)} records")
        
        # Prompt user to move to magnitude selection
        response = input("\nConfirm 'yes' in order to move to magnitude? ")
        if response == 'yes':
            break
        else:
            continue
      
# Extract a sorted list of magnitudes from the selected earthquake data   
magLst = sorted([d['Magnitude'] for _ ,d in dtSelected])

print("\nSELECT Magnitude : Enter two values seperated by comma")
print(f"range is {magLst[0]} through {magLst[-1]}")

# Continuously prompt the user for magnitude input          
while True:
    try:
        # Attempt to get minimum and maximum magnitude values from user input
        mag1,mag2 = input("\nEnter minimum/maximum magnitude values: ").split(",")
        mag1,mag2=float(mag1),float(mag2)
        magMin = min(mag1,mag2)
        magMax = max(mag1,mag2)
        
        # Check if the entered magnitude range is within the available data range
        if magLst[0]< magMin and magMax< magLst[-1]:
            
            # Filter earthquake data based on the selected magnitude range
            magSelected = [((lat,lng),v) for (lat,lng),v in dtSelected if magMin <= v['Magnitude'] <= magMax]
            print("Accepted...")
            print({'min':magMin,'max':magMax})
            print(f"Selected {len(magSelected)} records")
            
            # Prompt user to move to analysis or continue
            response = input("\nRespond with yes if Want to move to Analysis? ")
            if response == "yes":
                break
            else:
                continue
        else:
            print(f"one or more values out of range <({mag1},{mag2})>")
    except:
        # Handle any exceptions and consider all records if input is empty string
        magSelected=[((lat,lng),data) for (lat,lng),data in dtSelected]
        print("Accepted...")
        print({'min':magLst[0],'max':magLst[-1]})
        print(f"Selected {len(magSelected)} records")
        
        # Prompt user to move to analysis or continue
        response = input("\nRespond with yes if Want to move to Analysis? ")
        if response == "yes":
            break
        else:
            continue
        
        
### Step 03 : Plot the graphs for the selected data and cities affected near location.    

    
# Sort magSelected based on Magnitude values
magSelected.sort(key=lambda x:x[1]['Magnitude'])

# Extract latitude, longitude, and magnitude lists from magSelected
lats=[lat for (lat,lng),data in magSelected]
lngs=[lng for (lat,lng),data in magSelected]
mags=[data['Magnitude'] for (lat,lng),data in magSelected]

# Create a scatter plot using latitude, longitude, and magnitude
plt.scatter(lngs,lats,c=mags)
plt.xlabel('longitude in degrees')
plt.ylabel('latitude in degrees')
plt.colorbar(label='magnitude')
plt.title(f"{tv}\n{d}")
plt.show()

# Extract unique years from the datetime data in magSelected
yearSelected=sorted(list(set(map(lambda x: x[1]['datetime'].year,magSelected))))
events={}

# Count the number of events for each year and create a bar plot
for year in yearSelected:
    info=[data for loc,data in magSelected
               if data['datetime'].year==year]
    events[year]=len(info)
    
# Create a bar plot using events.keys(), events.values()
plt.bar(events.keys(),events.values(),color='blue')
plt.xlabel('year')
plt.ylabel('Number of events')
plt.title(f"{tv}\n{d}")
plt.show()

# Calculate the average magnitude for each year and create a scatter plot
magsAvg={}
for year in yearSelected:
    mag=[data['Magnitude'] for loc,data in magSelected
               if data['datetime'].year==year]
    magsAvg[year]=sum(mag)/len(mag)

# Create a plot bar using magsAvg.keys(), magsAvg.values()
plt.scatter(magsAvg.keys(),magsAvg.values())
plt.xlabel('year')
plt.ylabel('average magnitude')
nl='\n'
plt.title(f"{tv}\n{d}")
plt.show()
    

# Extract information about the largest earthquake
largest_quake_location = magSelected[-1][0]
largest_quake_data = magSelected[-1][1]

# Print information about the largest earthquake
print(f"Largest quake is at {largest_quake_location}")
print('\t\n', largest_quake_data)

# Calculate the affected area radius based on the magnitude
radius = 10 ** (0.5 * largest_quake_data['Magnitude'] - 2)

# Find cities within the radius of the largest earthquake
affectedCities = findCities(largest_quake_location, cityDict, radius)

# Calculate the total population of affected cities
total_population_affected = sum([city['pop'] for city in affectedCities])


# Print information about the affected cities and total population

print(f'\nClosest cities in the radius are {radius} km')
print('\t', *affectedCities, f'Total population affected {total_population_affected=}', sep='\n\t')


print(f"{len(affectedCities)} affected cities within {radius} km..")
# closest_cities for large quake location and 5000 km radius
close_cities=findCities(largest_quake_location, cityDict,5000)
print("closest city is...")
# printing the closest city data
close_cities.sort(key = lambda x:x['distance'])
print(close_cities[0])
    

    
    
    
    
    
    
    