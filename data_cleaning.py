# file that cleaned our datasets, and added columns

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
