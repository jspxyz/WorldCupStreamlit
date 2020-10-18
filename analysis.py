# imports section

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
import matplotlib as mpl
import streamlit as st 


# Loading Data
@st.cache(allow_output_mutation=True)
def load_data(path):
    data = pd.read_csv(path)
    return data

matches = load_data('https://raw.githubusercontent.com/jspxyz/WorldCupStreamlit/main/matches_clean.csv')

#-----
# introsection
st.title('World Cup Analysis | October 2020')
st.subheader('Data from 1930 - 2014')
st.subheader('by Rosy, Jun, James')
st.image('https://cdni.rt.com/files/2018.07/article/5b4ccd6ddda4c8aa418b45bb.jpg')


# Number of match and Average goal chart
st.subheader('Matches and Goals Data')

st.write('''After a short increase in goals through 1954, number of average goals scored per match has
plateaued under 3 goals per match.''')

Average_goal = load_data('https://raw.githubusercontent.com/jspxyz/WorldCupStreamlit/main/Average_goal.csv')

year = Average_goal['Year'].tolist()
number_of_match = Average_goal['number_of_match'].tolist()
average_goal = Average_goal['average_goal'].tolist()
x = np.arange(len(year))  
fig,ax1 = plt.subplots(figsize=(13,5))
fig.suptitle("Count of Matches and Average Goals by Year")
color = 'tab:orange'
ax1.set_xlabel('Year')
ax1.set_ylabel('Match', color=color)
ax1.plot(x, number_of_match, color=color,label='number of match')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticks(Average_goal.index)
ax1.set_xticklabels(year)

ax2 = ax1.twinx()  

color = 'tab:blue'
ax2.set_ylabel('Average goal', color=color)  
ax2.plot(x, average_goal, color=color,label='average_goal')
ax2.tick_params(axis='y', labelcolor=color)

st.pyplot(fig)

# Showing raw data
if st.checkbox('Show raw data for Matches and Goals Data above:'):
    st.subheader('Raw data')
    st.write(Average_goal)

#--------------------
#Section about Championships
st.header('Champion Insights')
st.write('''This section is dedicated to the World Cup champions. As seen in the geomap below,
Europe and South America hold the powerhouses of football.''')


# Map of top 3
Top_3 = load_data('https://raw.githubusercontent.com/jspxyz/WorldCupStreamlit/main/Top3.csv')

st.subheader('Where are the World Cup Winners')
# Plot winner on map
slide = st.slider("Winning time", 1, 5)
winner = Top_3[(Top_3['Winner'] >= int(slide))]
st.map(winner,1.3)

st.write('''Below represents all countries that have been crowned in the Top 3 at least once.
It's definitely skewed to the 8 countries seen above.''')

# adding group by chart for country WON and Top3
# Grouped bar chart show how many time each country won and in top 3
Countryname = Top_3['Countries'].tolist()
Winnerdata = Top_3['Winner'].tolist()
Totaldata = Top_3['Totaltop3'].tolist()

x = np.arange(len(Countryname))  
width = 0.35 

fig, ax = plt.subplots(figsize=(17,5))

rects1 = ax.bar(x - width/2, Totaldata, width, label='Top 3')
rects2 = ax.bar(x + width/2, Winnerdata, width, label='Winner')

ax.set_ylabel('Number of occurence')
ax.set_xlabel('Countries')
ax.set_title('Country won and in top 3')
ax.set_xticks(x)
ax.set_xticklabels(Countryname)
ax.legend()

def autolabel01(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel01(rects1)
autolabel01(rects2)

fig.tight_layout()

st.pyplot(fig)



# New Section--------------------------------
# How was each country perform in all World Cup?
st.subheader('Each Country\'s overall individual performance.')

#function to get country details
def countryDetails(country):
    # setting datetime
    matches['Datetime'] = pd.to_datetime(matches['Datetime'])

    # setting years to Ints and using year as index
    matches['Year']= matches['Year'].astype('int')
    matches.set_index('Year')

    # finding all matches played by Countries
    country_matches = matches[(matches['Home Team Name']==country) | (matches['Away Team Name']==country)]

    # reset index to year
    country_matches.set_index('Year')

    # finding number of matches played by Countries by year
    country_match = country_matches.groupby('Year').agg(Number_of_match=('City','count'))

    # finding interesting win conditions
    country_matches['Win conditions'].unique()

    # finding Countries winning matches
    Country_winning_matches = country_matches[country_matches['WinningTeam']==country].groupby('Year').agg(Winning_match=('WinningTeam','count'))

    # creating Countries Table of number of matches played and matches won
    country_table_final = country_match.merge(Country_winning_matches , how='left', left_index=True, right_on='Year')
    country_table_final.set_index('Year',inplace=True)
    country_table_final.fillna('0',inplace=True)

    return country_table_final


option = st.selectbox('Select a country for addtional details', ('Argentina', 'Austria', 'Brazil', 'Chile', 'Croatia', 'Czechoslovakia', 'England', 'France', 'Germany', 'Hungary', 'Italy', ' Netherlands', 'Poland', 'Portugal', 'Spain', 'Sweden', 'Turkey', 'USA', 'Uruguay'))
Country_Details = countryDetails(str(option))
Country_Details.reset_index(level = 0, inplace=True)
Country_Details.columns = ['Year', 'Number_of_match', 'Winning_match']
Country_Details['Winning_match'] = Country_Details['Winning_match'].astype(int)


# Select country from select option
selectCountry = Country_Details

# Grouped bar chart for selectCountry
selectCountry['Winning_match'] = selectCountry['Winning_match'].astype(int)

year = selectCountry['Year'].tolist()
number_of_match = selectCountry['Number_of_match'].tolist()
winning_match = selectCountry['Winning_match'].tolist()
x = np.arange(len(year))
width = 0.35 
fig, ax = plt.subplots(figsize=(17,7))
rects1 = ax.bar(x - width/2, number_of_match, width, label='number of match')
rects2 = ax.bar(x + width/2, winning_match, width, label='winning match')
ax.set_ylabel('Match')
ax.set_xlabel('Year')
ax.set_title('Performance in World Cup')
ax.set_xticks(selectCountry.index)
ax.set_xticklabels(year)
ax.legend()

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
fig.tight_layout()
st.pyplot(fig)

# showing data for above
st.table(Country_Details)

# commented out below since we already show the raw data above
# if st.checkbox('Show performance raw data'):
#     st.subheader('Raw data')
#     st.dataframe(selectCountry)

# Brazil, Germany and Italy photos
col1, col2, col3 = st.beta_columns(3)
with col1:
    st.header("Brazil")
    st.image("https://www.livechennai.com/images/World_Cup/2002_WC.jpg", use_column_width=True)
with col2:
    st.header("Germany")
    st.image("https://cdn.britannica.com/58/179158-050-A1E1419E/players-triumph-West-German-trophy-2014-FIFA-October-1990.jpg", use_column_width=True)
with col3:
    st.header("Italy")
    st.image("https://www.livechennai.com/images/World_Cup/2006_WC.jpg", use_column_width=True)


st.header('Recommendations')
# Chance of host country in Top 3

winners_final = load_data('https://raw.githubusercontent.com/jspxyz/WorldCupStreamlit/main/winners_final.csv')
st.markdown('Chance that host country in Top 3')
st.text(winners_final[['Hostwinner', 'Hosttop3']].mean())
if st.checkbox('Show winner raw data'):
    st.subheader('Raw data')
    st.dataframe(winners_final)

st.markdown('Breakdown of all countries that have placed in the Top 3')
st.table(Top_3[['Countries','Winner','Runners-Up','Third']])

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(Top_3)

st.header('A little extra, if we have time')
st.subheader('All Matches World Wide')
st.write('Below is a world map of all the cities that have held matches, with attendance size as a slider bar.')
# geo slider map of all matches played
# slider by attendance
st.subheader('World Cup Matches by Attendance | Worldview')
slide = st.slider('Choose your attendance size:', 1000, 180000, 15000)
matches_by_attendance = matches[(matches['Attendance'] > int(slide))][['latitude', 'longitude']]
st.map(matches_by_attendance)


st.subheader('Top 20 Matches All Time')
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

#------------------
# additional code not used but left for examples

# Detailed podium
# st.subheader('How well were they doing?')
# option = st.selectbox('Select a country you love', Top_3['Countries'].unique())
# Country_Achievement = Top_3[Top_3['Countries'] == str(option)][['Countries', 'Winner','Runners-Up','Third']]
# st.table(Country_Achievement)

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(Top_3)
#------------------


# st.sidebar.header('User Input Features')
# selected_year = st.sidebar.selectbox('Year', list(reversed(range(1930,2015))))


# >>> col1, col2 = st.beta_columns([3, 1])
# >>> data = np.random.randn(10, 1)
# >>>
# >>> col1.subheader("A wide column with a chart")
# >>> col1.line_chart(data)
# >>>
# >>> col2.subheader("A narrow column with the data")
# >>> col2.write(data)
#------------------




# example selector box
# option = st.selectbox('Select a country you love', Top_3['Countries'].unique())
# Country_Achievement = Top_3[Top_3['Countries'] == str(option)][['Countries', 'Winner','Runners-Up','Third']]
# st.table(Country_Achievement)

# example 2 selector box
# st.subheader('Price by neighborhood example')
# st.selectbox('Select an area', ('Brooklyn','Manhattan', 'Queens', 'Bronx', 'Staten Island'))
# price per type
# price_house_type = df[df['neighborhood_group'] ==
#                     str(user_area)].groupby('room_type').mean()['price']
# st.dataframe(price_house_type)
