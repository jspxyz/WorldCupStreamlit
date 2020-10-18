import numpy as np
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import streamlit as st

# 0.0 reading datafiles
matches = pd.read_csv('matches_clean.csv', encoding='latin1')
players = pd.read_csv('players_clean.csv', encoding='latin1')
winners = pd.read_csv('winners_final.csv')

#-------------------------------------------------
##### Start of Streamlit code

st.title('World Cup Analysis | October 2020')
st.header('Data from 1930 - 2014')
st.header('by Rosy, Jun, James')

st.subheader('Can Attendance impact the number of goals scored?')
st.write('Last week, we mentioned there could be a correlation between goals scored and attendance. To briefly review, we noticed there was an obvious uptick in attendance over the years.')

# tracking attendance by year
st.subheader('Attendance by Year')
Year = winners['Year'].tolist()
Attendance = winners['Attendance'].tolist()

fig = plt.figure(figsize=(10,6))
plt.bar(Year, Attendance)

plt.title('Attendance by Year')
plt.xlabel('Year')
plt.ylabel('Attendance')

plt.xticks(Year,labels=Year,rotation=90)
plt.grid(linestyle='--')

st.pyplot(fig)

# attendance and goals by year
st.write('''Below we see the chart displayed last week showing a strong correlation 
between Attendance and Goals. Whoa! Could it be that the more fans there are, 
the more players want to score?''')

# Total of attendance and goals by year
summatches = matches.groupby('Year').sum()
attendance = summatches['Attendance']
goals = summatches['GoalsTotal']

fig = plt.figure(figsize=(4, 4))
plt.scatter(attendance, goals)
plt.xlabel('Attendance')
plt.xlim(0,4000000)
plt.ylabel('Goals')
plt.title('Attendance & Goals Correlation')
st.pyplot(fig)

# matches and goals by year
st.write('''No, no. Do not let anyone tell you that audience can impact a game by that match. 
Simply changing the attendance variable with the number of matches shows a very similar correlation. 
Very obvious now that the number of goals scored in a World Cup is obviously driven mainly by the 
number of matches played per tournament.''')
summatches = matches.groupby('Year').sum()
countmatches = matches.groupby('Year').count()
# attendance = summatches['Attendance']
matchcount = countmatches['MatchID']
goals = summatches['GoalsTotal']

fig = plt.figure(figsize=(4, 4))
plt.scatter(matchcount, goals)
plt.xlabel('Match Count')
# plt.xlim(0,)
plt.ylabel('Goals')
plt.title('Matches & Goals Correlation')
st.pyplot(fig)


# Top 20 matches with highest attendence
st.write('However, looking into the Top 20 matches, may tell us why Attendance may have some relationship with a country.')
def game_info(input):
    team1 = input[0]
    team2 = input[1]
    year = input[2]
    winner = input[3]
    host = input[4]
    return f'Host: {host} | {year}: {team1} vs {team2} ({winner})'

matches_trunk = matches[['Year', 'City', 'Attendance', 'Home Team Name', 'Away Team Name', 'WinningTeam', 'Host Country']]
matches_trunk['Competition'] = matches_trunk[['Home Team Name', 'Away Team Name', 'Year', 'WinningTeam', 'Host Country']].apply(game_info, axis = 1)
matches_trunk_10 = matches_trunk.sort_values(by='Attendance', ascending= False)
matches_trunk_10 = matches_trunk_10[['Attendance', 'Competition']].head(20)

# Visualization of Top 10 Matches of Attendance
fig, ax = plt.subplots(figsize=(12, 10))
ax.barh(matches_trunk_10['Competition'], matches_trunk_10['Attendance'])
plt.xlabel('Attendance')
plt.title('Top 20 matches with highest Attendance')
st.pyplot(fig)

st.write('''Notice anything? If you are guessing that any game with Brazil has a high attendance, 
you are close. What we are seeing is that Attendance is extremely high for matches when the Host 
country also happens to be playing in that match.
Yes, this also seems to be pretty obvious. This is our first time doing this. Give us a break.
And enjoy the little geoslider below to see where all the World Cup matches have been played!''')

# geo slider map of all matches played
# slider by attendance
st.subheader('World Cup Matches by Attendance | Worldview')
slide = st.slider('Choose your attendance size:', 1000, 150000, 15000)
matches_by_attendance = matches[(matches['Attendance'] > int(slide))][['latitude', 'longitude']]
st.map(matches_by_attendance)

# geo slider map of all matches played
# slider by goal
# st.subheader('World Cup Matches by Goals')
# slide = st.slider('Choose your Number of Goals:', 0, 15, 1)
# matches_by_goals = matches[(matches['GoalsTotal'] > int(slide))][['latitude', 'longitude']]
# st.map(matches_by_goals)

#-----------------------------#
# excess example code

# st.subheader('Price by neighborhood example')
# st.selectbox('Select an area', ('Brooklyn','Manhattan', 'Queens', 'Bronx', 'Staten Island'))
# price per type
# price_house_type = df[df['neighborhood_group'] ==
#                     str(user_area)].groupby('room_type').mean()['price']
# st.dataframe(price_house_type)
#
# df = pd.DataFrame(
#     {'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
#      'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
#      'Latitude': [-34.58, -15.78, -33.45, 4.60, 10.48],
#      'Longitude': [-58.66, -47.91, -70.66, -74.08, -66.86]})
# gdf = geopandas.GeoDataFrame(
#     df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))
# st.write(gdf.head())
# world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
# ax = world[world.continent == 'South America'].plot(
#     color='white', edgecolor='black')
# gdf.plot(ax=ax, color='red')
# st.pyplot()