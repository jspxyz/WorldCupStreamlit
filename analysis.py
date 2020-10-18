# imports section

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
import matplotlib as mpl
import streamlit as st 


@st.cache(allow_output_mutation=True)
def load_data(path):
    data = pd.read_csv(path)
    return data

# Chance of host country in Top 3

winners_final = load_data('/Users/jsp/Desktop/KermadecProjects/WorldCupStreamlit/winners_final.csv')
st.markdown('Chance that host country in Top 3')
st.text(winners_final[['Hostwinner', 'Hosttop3']].mean())
if st.checkbox('Show winner raw data'):
    st.subheader('Raw data')
    st.dataframe(winners_final)


# Map of top 3
Top_3 = load_data('/Users/jsp/Desktop/KermadecProjects/WorldCupStreamlit/Top3.csv')

st.subheader('Where are the World Cup Winners')
# Plot winner on map
slide = st.slider("Winning time", 1, 5)
winner = Top_3[(Top_3['Winner'] >= int(slide))]
st.map(winner,1.3)

# Detailed podium
st.subheader('How well were they doing?')
option = st.selectbox('Select a country you love', Top_3['Countries'].unique())
Country_Achievement = Top_3[Top_3['Countries'] == str(option)][['Countries', 'Winner','Runners-Up','Third']]
st.table(Country_Achievement)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(Top_3)


# How was each country perform in all World Cup?
st.subheader('How was a Country\'s performance?')
# Select box
Brazil = load_data('/Users/jsp/Desktop/KermadecProjects/WorldCupStreamlit/Brazil.csv')

# Grouped bar chart for Brazil

year = Brazil['Year'].tolist()
number_of_match = Brazil['number_of_match'].tolist()
winning_match = Brazil['wining_match'].tolist()
x = np.arange(len(year))  
width = 0.35 
fig, ax = plt.subplots(figsize=(17,7))
rects1 = ax.bar(x - width/2, number_of_match, width, label='number of match')
rects2 = ax.bar(x + width/2, winning_match, width, label='winning match')
ax.set_ylabel('Match')
ax.set_xlabel('Year')
ax.set_title('Brazil Performance in World Cup')
ax.set_xticks(Brazil.index)
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
    st.dataframe(Brazil)



# Number of match and Average goal chart
st.subheader('How were their performance?')
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
st.dataframe(Average_goal)










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