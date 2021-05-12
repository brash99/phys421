#!/usr/bin/env python
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Library which will allow us to do simple linear regression
from scipy.stats import linregress

# Library which allows plotting of a world map
from mpl_toolkits.basemap import Basemap

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Input File (CSV)
input_data_file = "output_data/cities.csv"

# Read the previously created weather data from a file
clean_city_data = pd.read_csv(input_data_file)

clean_city_data.info()

# Cleaning of the data - first pass
#
# We need to remove any "duplicate entries" from the data, if we are going to generate a heatmap
# Problems arise if we have two cities that have exactly the same longitude.  To get around this, we
# can create a "fake" longitude, which is extremely close to the original longitude, but is just augmented
# slightly by the addition of a term proportional to the latitude.  This should result in different values of
# augmented longitude for each city in the dataframe.
clean_city_data['Augmented Longitude']=clean_city_data['Longitude']+0.0001*clean_city_data['Latitude']

# Sort the dataframe based upon this new augmented longitude.
clean_city_data.sort_values("Augmented Longitude", inplace = True)

# Drop any duplicate entries that might remain.  Note that in this example we went from 1321 entries in the 
# original dataframe to 1319 entries in the new dataframe.
clean_city_data.drop_duplicates(subset ="Augmented Longitude",keep = False, inplace = True)

clean_city_data.info()

# Cleaning of the data - second pass
#
# create a new dataframe, called parsed_data, which includes only those cities that have
# a) a temperature above 70F
# b) a temperature below 80F
# c) a wind speed < 10 mph
# d) a cloudiness = 0
#
parsed_data = clean_city_data[clean_city_data['Max Temp']>=(70-32.0)*5.0/9.0+273.15]
parsed_data = parsed_data[parsed_data['Max Temp']<=(80-32.0)*5.0/9.0+273.15]
parsed_data = parsed_data[parsed_data['Wind Speed']<=10]
parsed_data = parsed_data[parsed_data['Cloudiness']==0]

parsed_data

# Create a heatmap of the original dataframe.  We are using here the Basemap library from the mpl_toolkits module.

plt.subplots(figsize=(10, 7))

map = Basemap(projection='mill',lon_0=0)
# plot coastlines, draw label meridians and parallels.
map.drawcoastlines()
map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])

map.scatter(clean_city_data['Longitude'], clean_city_data['Latitude'], latlon=True, 
            c=clean_city_data['Humidity'])

plt.colorbar(label=r'Humidity (percent)')

# create a heatmap of the parsed data
plt.subplots(figsize=(10, 7))

map = Basemap(projection='mill',lon_0=0)
# plot coastlines, draw label meridians and parallels.
map.drawcoastlines()
map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])

map.scatter(parsed_data['Longitude'], parsed_data['Latitude'], latlon=True, 
            c=parsed_data['Humidity'])

plt.colorbar(label=r'Humidity (percent)')