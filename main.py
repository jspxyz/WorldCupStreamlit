import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# reading datafiles
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

# 2.0 Adding Columns


st.title('World Cup Analysis | October 2020')
st.header('by Rosy, Jun, James')

matches