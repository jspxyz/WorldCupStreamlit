import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import geopandas
from opencage.geocoder import OpenCageGeocode
from pprint import pprint

# testing opencage city finder
key = '00ad2adcfadd4b32b3612bd75c680741'
geocoder = OpenCageGeocode(key)
query = 'Bijuesca, Spain'  
results = geocoder.geocode(query)
lat = results[0]['geometry']['lat']
lng = results[0]['geometry']['lng']
print (lat, lng)

matches_forcity = pd.read_csv('matches.csv', encoding='latin1')
winners = pd.read_csv('winners.csv')

# create empty lists
list_lat = []   
list_long = []
	
for index, row in matches_forcity: # iterate over rows in dataframe

    City = row['City']
    State = row['State']       
    query = str(City)+','+str(State)

    results = geocoder.geocode(query)   
    lat = results[0]['geometry']['lat']
    long = results[0]['geometry']['lng']

    list_lat.append(lat)
    list_long.append(long)

	
# create new columns from lists    

df_crime_more_cities['lat'] = list_lat   

df_crime_more_cities['lon'] = list_long
