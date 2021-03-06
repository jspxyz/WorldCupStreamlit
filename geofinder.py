import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import streamlit as st
# import geopandas
from opencage.geocoder import OpenCageGeocode
# from pprint import pprint

# key for geocoder
key = '00ad2adcfadd4b32b3612bd75c680741'
geocoder = OpenCageGeocode(key)

# testing opencage city finder
# query = 'Bijuesca, Spain'  
# results = geocoder.geocode(query)
# lat = results[0]['geometry']['lat']
# lng = results[0]['geometry']['lng']
# print (lat, lng)

matches = pd.read_csv('matches.csv', encoding='latin1')

# create empty lists
list_lat = []   
list_long = []

# iterate over rows in dataframe
for index, row in matches.iterrows(): 
    city = row['City'].strip()
    state = row['Host Country']
    query = str(city)+','+str(state)
    print(query)

    results = geocoder.geocode(query)
    print(results)
    lat = results[0]['geometry']['lat']
    long = results[0]['geometry']['lng']

    list_lat.append(lat)
    list_long.append(long)

print(list_lat)
print(list_long)

# create new columns from lists    
matches['latitude'] = list_lat   
matches['longitude'] = list_long