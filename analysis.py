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

matches = load_data('/Users/jsp/Desktop/KermadecProjects/WorldCupStreamlit/matches_clean.csv')

#-----
# introsection
st.title('World Cup Analysis | October 2020')
st.subheader('Data from 1930 - 2014')
st.subheader('by Rosy, Jun, James')


# Total of attendance and goals by year
st.header('Goal Insights')
st.write('blah blah blah')
summatches = matches.groupby('Year').sum()
attendance = summatches['Attendance']
goals = summatches['GoalsTotal']

fig = plt.figure(figsize=(3, 3))
plt.scatter(attendance, goals)
plt.xlabel('Attendance')
plt.xlim(0,4000000)
plt.ylabel('Goals')
plt.title('Attendance & Goals Correlation')
fig.tight_layout()
st.pyplot(fig)


# Number of match and Average goal chart
st.subheader('Matches and Goals Data')
Average_goal = load_data('/Users/jsp/Desktop/KermadecProjects/WorldCupStreamlit/Average_goal.csv')

year = Average_goal['Year'].tolist()
number_of_match = Average_goal['number_of_match'].tolist()
average_goal = Average_goal['average_goal'].tolist()
x = np.arange(len(year))  
fig,ax1 = plt.subplots(figsize=(13,5))
fig.suptitle("Number of match and Average goal by year")
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


st.header('Champion Insights')
st.write('blahblaskdfjla;jef')


# Map of top 3
Top_3 = load_data('/Users/jsp/Desktop/KermadecProjects/WorldCupStreamlit/Top3.csv')

st.subheader('Where are the World Cup Winners')
# Plot winner on map
slide = st.slider("Winning time", 1, 5)
winner = Top_3[(Top_3['Winner'] >= int(slide))]
st.map(winner,1.3)

st.write('bleh blah lbuer ')

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


option = st.selectbox('Select a country for addtional details', ('Argentina', 'Austria', 'Brazil', 'Chile', 'Germany', 'Italy', 'Spain', 'France', 'England', ' Netherlands', 'Czechoslovakia', 'Hungary', 'Sweden', 'Poland', 'USA', 'Croatia', 'Turkey', 'Portugal', 'Uruguay'))
Country_Details = countryDetails(str(option))
Country_Details.reset_index(level = 0, inplace=True)
Country_Details.columns = ['Year', 'Number_of_match', 'Winning_match']
st.table(Country_Details)


# Select box
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

if st.checkbox('Show performance raw data'):
    st.subheader('Raw data')
    st.dataframe(selectCountry)


st.header('Recommendations')
# Chance of host country in Top 3

winners_final = load_data('/Users/jsp/Desktop/KermadecProjects/WorldCupStreamlit/winners_final.csv')
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


# >>> col1, col2, col3 = st.beta_columns(3)
# >>>
# >>> with col1:
# ...    st.header("A cat")
# ...    st.image("https://static.streamlit.io/examples/cat.jpg", use_column_width=True)
# ...
# >>> with col2:
# ...    st.header("A dog")
# ...    st.image("https://static.streamlit.io/examples/dog.jpg", use_column_width=True)
# ...
# >>> with col3:
# ...    st.header("An owl")
# ...    st.image("https://static.streamlit.io/examples/owl.jpg", use_column_width=True)



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
