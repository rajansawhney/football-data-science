#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 11:34:26 2020

Script for lesson 5 of "Friends of Tracking" #FoT

Data can be found at: https://github.com/metrica-sports/sample-data

Accompanying video tutorials can be found here: https://www.youtube.com/channel/UCUBFJYcag8j2rm_9HkrrA7w

GitHub repo: https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking

@author: Laurie Shaw (@EightyFivePoint)
"""


import Metrica_IO as mio
import Metrica_Viz as mviz
import Metrica_Velocities as mvel
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# set up initial path to data
DATADIR = '/Users/rsawhney/dev/football-data-science/analysis-with-tracking-data/data'
game_id = 2 # let's look at sample match 2

# read in the event data
events = mio.read_event_data(DATADIR,game_id)

# read in tracking data
tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')

# Convert positions from metrica units to meters (note change in Metrica's coordinate system since the last lesson)
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)
events = mio.to_metric_coordinates(events)

# reverse direction of play in the second half so that home team is always attacking from right->left
tracking_home,tracking_away,events = mio.to_single_playing_direction(tracking_home,tracking_away,events)

# Making a movie of the second home team goal
#PLOTDIR = DATADIR
#mviz.save_match_clip(tracking_home.iloc[73600:73600+500],tracking_away.iloc[73600:73600+500],PLOTDIR,fname='home_goal_2',include_player_velocities=False)

# Calculate player velocities
tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True)
tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True)
# **** NOTE *****
# if the lines above produce an error (happens for one version of numpy) change them to the lines below:
# ***************
#tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True,filter_='moving_average')
#tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True,filter_='moving_average')

# plot a random frame, plotting the player velocities using quivers
mviz.plot_frame( tracking_home.loc[10000], tracking_away.loc[10000], include_player_velocities=True, annotate=True)

# Create a Physical summary dataframe for home players
home_players = np.unique( [ c.split('_')[1] for c in tracking_home.columns if c[:4] == 'Home' ] )
home_summary = pd.DataFrame(index=home_players)

# Calculate minutes played for each player
minutes = []
for player in home_players:
    # search for first and last frames that we have a position observation for each player (when a player is not on the pitch positions are NaN)
    column = 'Home_' + player + '_x' # use player x-position coordinate
    player_minutes = ( tracking_home[column].last_valid_index() - tracking_home[column].first_valid_index() + 1 ) / 25 / 60. # convert to minutes
    minutes.append( player_minutes )
home_summary['Minutes Played'] = minutes
home_summary = home_summary.sort_values(['Minutes Played'], ascending=False)

# Calculate total distance covered for each player
distance = []
for player in home_summary.index:
    column = 'Home_' + player + '_speed'
    player_distance = tracking_home[column].sum()/25./1000 # this is the sum of the distance travelled from one observation to the next (1/25 = 40ms) in km.
    distance.append( player_distance )
home_summary['Distance [km]'] = distance

# make a simple bar chart of distance covered for each player
plt.subplots()
ax = home_summary['Distance [km]'].plot.bar(rot=0)
ax.set_xlabel('Player')
ax.set_ylabel('Distance covered [km]')

# plot positions at KO (to find out what position each player is playing)
mviz.plot_frame( tracking_home.loc[51], tracking_away.loc[51], include_player_velocities=False, annotate=True)

# now calculate distance covered while: walking, joggings, running, sprinting
walking = []
jogging = []
running = []
sprinting = []
for player in home_summary.index:
    column = 'Home_' + player + '_speed'
    # walking (less than 2 m/s)
    player_distance = tracking_home.loc[tracking_home[column] < 2, column].sum()/25./1000
    walking.append( player_distance )
    # jogging (between 2 and 4 m/s)
    player_distance = tracking_home.loc[ (tracking_home[column] >= 2) & (tracking_home[column] < 4), column].sum()/25./1000
    jogging.append( player_distance )
    # running (between 4 and 7 m/s)
    player_distance = tracking_home.loc[ (tracking_home[column] >= 4) & (tracking_home[column] < 7), column].sum()/25./1000
    running.append( player_distance )
    # sprinting (greater than 7 m/s)
    player_distance = tracking_home.loc[ tracking_home[column] >= 7, column].sum()/25./1000
    sprinting.append( player_distance )
    
home_summary['Walking [km]'] = walking
home_summary['Jogging [km]'] = jogging
home_summary['Running [km]'] = running
home_summary['Sprinting [km]'] = sprinting

# make a clustered bar chart of distance covered for each player at each speed
ax = home_summary[['Walking [km]','Jogging [km]','Running [km]','Sprinting [km]']].plot.bar(colormap='coolwarm')
ax.set_xlabel('Player')
ax.set_ylabel('Distance covered [m]')

# sustained sprints: how many sustained sprints per match did each player complete? Defined as maintaining a speed > 7 m/s for at least 1 second
nsprints = []
sprint_threshold = 7 # minimum speed to be defined as a sprint (m/s)
sprint_window = 1*25 # minimum duration sprint should be sustained (in this case, 1 second = 25 consecutive frames)
for player in home_summary.index:
    column = 'Home_' + player + '_speed'
    # trick here is to convolve speed with a window of size 'sprint_window', and find number of occassions that sprint was sustained for at least one window length
    # diff helps us to identify when the window starts
    player_sprints = np.diff( 1*( np.convolve( 1*(tracking_home[column]>=sprint_threshold), np.ones(sprint_window), mode='same' ) >= sprint_window ) )
    nsprints.append( np.sum( player_sprints == 1 ) )
home_summary['# sprints'] = nsprints
         
# Plot the trajectories for each of player 10's sprints
player = '10'
column = 'Home_' + player + '_speed' # spped
column_x = 'Home_' + player + '_x' # x position
column_y = 'Home_' + player + '_y' # y position
# same trick as before to find start and end indices of windows of size 'sprint_window' in which player speed was above the sprint_threshold
player_sprints = np.diff( 1*( np.convolve( 1*(tracking_home[column]>=sprint_threshold), np.ones(sprint_window), mode='same' ) >= sprint_window ) )
player_sprints_start = np.where( player_sprints == 1 )[0] - int(sprint_window/2) + 1 # adding sprint_window/2 because of the way that the convolution is centred
player_sprints_end = np.where( player_sprints == -1 )[0] + int(sprint_window/2) + 1
# now plot all the sprints
fig,ax = mviz.plot_pitch()
for s,e in zip(player_sprints_start,player_sprints_end):
    ax.plot(tracking_home[column_x].iloc[s],tracking_home[column_y].iloc[s],'ro')
    ax.plot(tracking_home[column_x].iloc[s:e+1],tracking_home[column_y].iloc[s:e+1],'r')
    
# END


""" 
HOMEWORK
# 1. Plot passes and shot leading up to the second and third goal
"""
# all shots
shots = events[events['Type']=='SHOT']
goals = shots[shots['Subtype'].str.contains('-GOAL')].copy()

#2nd goal (scored by away team - blue) - index of goal event is 823
mviz.plot_events( events.loc[818:823], indicators = ['Marker','Arrow'], annotate=True, color='b' )

#3rd goal (scored by home team - red) - index of goal event is 1118
# filter out shot and passes
passes_shots = events[events['Type'].isin(['SHOT', 'PASS'])]
mviz.plot_events( passes_shots.loc[1109:1118], indicators = ['Marker','Arrow'], annotate=True, color='r' )

"""
# 2. Plot all the shots by Player 9 of the home team. Use diffrent symbol and transparency (alphabet)
"""

home_player9_shots = events[ (events.From=='Player9') & (events.Type=='SHOT') & (events.Team=='Home') ]

home_player9_shots_goal = home_player9_shots[home_player9_shots['Subtype'].str.contains('-GOAL')].copy()
home_player9_shots_nogoal = home_player9_shots[~home_player9_shots['Subtype'].str.contains('-GOAL')].copy()

fig, ax = mviz.plot_events(home_player9_shots_goal, indicators = ['Marker', 'Arrow'], annotate=False, color='g', alpha=1, marker_style='s')
mviz.plot_events(home_player9_shots_nogoal, figax = (fig, ax), indicators = ['Marker', 'Arrow'], annotate=False, color='r', alpha=0.2, marker_style='o')


"""
# 3. Plot position of all players at Player 9's goal using tracking data
"""
goal_frame = home_player9_shots_goal['Start Frame'] 
fig, ax = mviz.plot_frame( tracking_home.loc[goal_frame], tracking_away.loc[goal_frame], PlayerAlpha=0.3)
fig, ax = mviz.plot_events(home_player9_shots_goal, figax = (fig, ax), indicators = ['Marker', 'Arrow'], annotate=True)

"""
# 4. Calculate distance covered by each player
"""
teams = ['Home', 'Away']
data = [tracking_home, tracking_away]
 
for name, data in zip(teams, data):
    team_players = np.unique( [c.split('_')[1] for c in data.columns if c[:4] == name ])
    team_summary = pd.DataFrame(index=team_players)
    
    # Calculate total distance covered for each player
    distance = []
    for player in team_summary.index:
        column = name + '_' + player + '_speed'
        player_distance = data[column].sum()/25./1000 # this is the sum of distance travelled from one observation to the next (1/25 = 40ms) in kilometers
        distance.append(player_distance)
        
    team_summary['Distance [km]'] = distance
    team_summary = team_summary.sort_values(['Distance [km]'], ascending=False)
    
    print("***** " + name + " team summary *****")
    print(team_summary)
    
    #make bar chart of distance covered by each player
    fig, ax = plt.subplots()
    ax = team_summary['Distance [km]'].plot.bar(rot=0)
    ax.set_xlabel('Player')
    ax.set_ylabel('Distance covered [km]')
    fig.suptitle(name + 'Team', y=0.95)
    




