import numpy as np
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import streamlit as st

# 0.0 reading datafiles
matches = pd.read_csv('matches.csv', encoding='latin1')
players = pd.read_csv('players.csv', encoding='latin1')
winners = pd.read_csv('winners.csv')

# 1.0 Data Cleaning

# 1.1 Change Winners dataset Attendance column to be integers.
# Removing '.' and replacing with ''
winners['Attendance'] = winners['Attendance'].str.replace('.', '').astype('int64')

# 1.2 Change 'Germany FR' to 'Germany' in winners & matches
winners = winners.replace('Germany FR', 'Germany')
matches = matches.replace('Germany FR', 'Germany')

# 1.3 Drop ALL Null of matches
matches = matches.dropna(how='all')

# 1.4 remove duplicates of MatchID
matches = matches.drop_duplicates()

# 1.5 Adjust Home & Away Team Names
# 1.5.1 collecting counts of incorrect home & away team names
names = matches[matches['Home Team Name'].str.contains('rn">')]['Home Team Name'].value_counts()

# 1.5.2 create index of wrong names
wrong = list(names.index)

# 1.5.3 list of correct names
correct = [name.split('>')[1] for name in wrong]

# 1.5.4 for loop to fix names in Matches Dataset
for index, wr in enumerate(wrong):
    matches = matches.replace(wrong[index], correct[index])

# 2.0 Adding Columns to Matches dataset

# 2.1 Adding WinningTeam column in Matches dataset
# 2.1.1 Create empty column list WinningTeam
matches['WinningTeam'] = pd.Series([0])

# 2.1.2 Function to determine winner of teach match
# team1, team2, score1, score2
def WinningTeamFunc(x):
    team1 = x[0]
    team2 = x[1]
    score1 = x[2]
    score2 = x[3]
    if (score1 > score2):
      return team1
    elif (score2>score1):
      return team2
    else:
      return 'Draw'

# 2.1.3 apply WinningTeamFunction to populate column
matches['WinningTeam'] = matches[['Home Team Name', 'Away Team Name', 'Home Team Goals', 'Away Team Goals']].apply(WinningTeamFunc, axis = 1)

# 2.2 Adding whether Home or Away team wins in Matches dataset
# 2.2.1 Create empty column list WinningTeam
matches['HomeAwayWin'] = pd.Series([0])

# 2.2.2 Function to determine Home or Away Team winner for each match
# score1, score2
def HomeAwayFunc(x):
    score1 = x[0]
    score2 = x[1]
    if (score1 > score2):
      return 'Home'
    elif (score2 > score1):
      return 'Away'
    else:
      return 'Draw'

# 2.2.3 apply WinningTeamFunction to populate column
matches['HomeAwayWin'] = matches[['Home Team Goals', 'Away Team Goals']].apply(HomeAwayFunc, axis = 1)

# 2.3 Adding whether Home or Away team is winnig at Halftime in Matches dataset
# 2.3.1 Create empty column list WinningTeam
matches['HalftimeWin'] = pd.Series([0])

# 2.3.2 Function to determine Home or Away Team winner at Halftime for each match
# score1, score2
def HalftimeWinFunc(x):
    score1 = x[0]
    score2 = x[1]
    if (score1 > score2):
      return 'Home'
    elif (score2 > score1):
      return 'Away'
    else:
      return 'Draw'

# 2.3.3 apply WinningTeamFunction to populate column
matches['HalftimeWin'] = matches[['Half-time Home Goals', 'Half-time Away Goals']].apply(HalftimeWinFunc, axis = 1)

# 2.4 Adding Goals Scored total column in Matches dataset
# 2.4.1 Create emtpy column list GoalsTotal
matches['GoalsTotal'] = pd.Series([0])

# 2.4.2 Function to calculate total goals scored
def GoalsTotalFunc(x):
  score1 = x[0]
  score2 = x[1]
  GoalsTotal = score1 + score2
  return GoalsTotal

# 2.4.3 apply GoalsTotalFunc to populate column
matches['GoalsTotal'] = matches[['Home Team Goals', 'Away Team Goals']].apply(GoalsTotalFunc, axis = 1)


# 2.5 Adding Goals Differential column in Matches dataset
# 2.5.1 Create emtpy column list GoalsTotal
matches['GoalsDiff'] = pd.Series([0])

# 2.5.2 Function to calculate goals differential
def GoalsDiffFunc(x):
  score1 = x[0]
  score2 = x[1]
  GoalsDiff = abs(score1 - score2)
  return GoalsDiff

# 2.4.3 apply GoalsTotalFunc to populate column
matches['GoalsDiff'] = matches[['Home Team Goals', 'Away Team Goals']].apply(GoalsDiffFunc, axis = 1)

# 3.0 Adding Columns to Winners dataset

# 3.1 Column to show if Host Country won or lost
# Create a new column
winners['Hostwinner'] = pd.Series([0])
# Create a function to populate new column to check whether host country is the winner
def HostwinnerFunc(x):
  country = x[0]
  winner = x[1]
  if country == winner:
    return 1
  elif country!= winner:
    return 0
winners['Hostwinner'] = winners[['Country', 'Winner']].apply(HostwinnerFunc, axis = 1)

# 3.2 Column to show if Host Country was in the Top 3
# Create a new column
winners['Hosttop3'] = pd.Series([0])
# Create a function to populate new column to check whether host country is in top 3
def Hosttop3Func(x):
  country = x[0]
  winner = x[1]
  runnersup = x[2]
  third = x[3]
  if country == winner or country == runnersup or country == third:
    return 1
  elif country != winner or country != runnersup or country != third:
    return 0
winners['Hosttop3'] = winners[['Country', 'Winner', 'Runners-Up', 'Third']].apply(Hosttop3Func, axis = 1)

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