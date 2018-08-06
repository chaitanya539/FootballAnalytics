import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

football = pd.read_excel('all_skill.xlsx')
players = pd.read_excel('Dim_Players.xlsx')

game = pd.merge(football, players, how = 'left' , on = 'Player', validate = 'many_to_one')

players.Player.value_counts().sort_values(ascending = False)

game.fillna(0, inplace = True)

####################checking data quality######################################
#treating for quality on adhoc basis
print(players.loc[players.Player == 'Carlos Sánchez'])

players = players[~((players.Player  == 'Carlos Sánchez') & (players.Country =='Uruguay'))]

#merge completes with validation
game = pd.merge(football, players, how = 'left' , on = 'Player', validate = 'many_to_one')

game.columns

game = game[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Country', 'Position', 'DoB(Age)', 'Caps', 'Goals',
       'Club', 'Club-Country','Apps',
       'Mins', 'Total_Aerial_Duels', 'Won', 'Lost', 'Rating', 'Total_Shots',
       'OutOfBox', 'SixYardBox', 'PenaltyArea', 'Total_Goals',
       'SixYardBox_Goals', 'PenaltyArea_Goals', 'OutOfBox_Goals',
       'Unsuccessful', 'Successful', 'Total_Dribbles', 'UnsuccessfulTouches',
       'Dispossessed', 'TotalTackles', 'DribbledPast', 'TotalAttemptedTackles',
       'Total_Interceptions', 'Fouled', 'Fouls', 'Yellow', 'Red',
       'CaughtOffside', 'Total_Clearances', 'ShotsBlocked', 'CrossesBlocked',
       'PassesBlocked', 'Total_Saves', 'Saves_In_SixYardBox',
       'Saves_In_PenaltyArea', 'Saves_From_OutOfBox', 'Total_Passes', 'AccLB',
       'InAccLB', 'AccSP', 'InAccSP', 'Total_Key_Passes', 'Long', 'Short',
       'Cross', 'Corner', 'Throughball', 'Freekick', 'Throwin', 'Other',
       'Total_Assists', 'Captain_Flag', 'Age', 'Chetan_Flag',
       'Deshbhakti_Flag']]


#super impartant
game.iloc[:,14:66] = game.iloc[:,14:66].convert_objects(convert_numeric=True)

game.dtypes
game.Tournament.describe()

#EDA on midfeilders in different tournaments

#Midfeilder analysis
midfeilders = game[game.Position == 'MF']

# Null value treatment
midfeilders.fillna(0, inplace = True)

###########################  Basic EDA  ####################################
MF_agg = midfeilders.assign(n=0).groupby(['Tournament', 'Season'], as_index = False).agg(
                                              {'OutOfBox_Goals':'mean',
                                               'SixYardBox_Goals': 'mean',
                                               'PenaltyArea_Goals': 'mean',
                                               'n':'count'})

MF_agg = MF_agg[~((MF_agg.OutOfBox_Goals==0) & (MF_agg.SixYardBox_Goals == 0))]
MF_agg['H1'] = np.where((MF_agg.OutOfBox_Goals - MF_agg.SixYardBox_Goals)>0 , True, False)

MF_agg.H1.value_counts()

#####################  Plotting   #############################

import colorsys
N = 5
HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)

plt.style.use('seaborn-whitegrid')
color_list = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'grey', 'brown','teal', 'maroon']

import itertools
colors = itertools.cycle(RGB_tuples)
color=next(colors)

q = MF_agg.groupby('Season')

for i, (Season,group) in enumerate(q):
    plt.scatter(x = group.Tournament, y = (group.OutOfBox_Goals - group.SixYardBox_Goals)
             , c = [next(colors)]*len(group.n), s=group.n*4, alpha=0.5,
            cmap='viridis', label = Season)
    plt.legend(loc = 'lower right',fontsize=8,ncol=4) #, mode="expand"
    
q = MF_agg.groupby('Tournament')

for i, (Tournament,group) in enumerate(q):
    plt.scatter(x = group.Season, y = (group.OutOfBox_Goals - group.SixYardBox_Goals)
             , c = [next(colors)]*len(group.n), s=group.n, alpha=0.5,
            cmap='viridis', label = Tournament)
    plt.legend(loc = 'lower left',fontsize=8,ncol=4) #, mode="expand"
##------------------------------------------------------------------------------------------

#while grouping, to take sum or average?
#take both 
'''some more data wrangling'''

game.columns
del game['Goals']
del game['Chetan_Flag']
del game['Deshbhakti_Flag']

##
game['Tournament-fullname'].unique()
to_check = game[game['Tournament-fullname'] == '0']
game.Tournament.unique()

t_list = []
q = game.groupby(['Tournament-fullname', 'Tournament'])
for name, group in q:
    print(name)

t_list = pd.DataFrame(t_list)
t_list.columns = ['Tournament-fullname','Tournament']
t_list = t_list[~(t_list['Tournament-fullname'] =='0')].reset_index()
del t_list['index']

#correcting tournament names 
game.loc[game.Player =='Samúel Friðjónsson', ['Tournament-fullname']] = 'Norway-Eliteserien'

#removing from tpurnament list mapping
t_list = t_list.loc[~(t_list['Tournament-fullname'] == 'Norway-Eliteserien')]


#using tournament list mapping to correct the game dataframe
to_check = to_check[to_check['Tournament-fullname']=='0']
checked = pd.merge(to_check, left_on = 'Tournament', right_on = 'Tournament')

len(game[game['Tournament-fullname'] == '0'])


checked.drop('Tournament-fullname_y', axis = 1, inplace = True)

checked.rename(columns = {'Tournament-fullname_x':'Tournament-fullname'}, inplace = True)

checked_1 = checked[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Country', 'Position', 'DoB(Age)', 'Caps',
       'Club', 'Club-Country','Apps',
       'Mins', 'Total_Aerial_Duels', 'Won', 'Lost', 'Rating', 'Total_Shots',
       'OutOfBox', 'SixYardBox', 'PenaltyArea', 'Total_Goals',
       'SixYardBox_Goals', 'PenaltyArea_Goals', 'OutOfBox_Goals',
       'Unsuccessful', 'Successful', 'Total_Dribbles', 'UnsuccessfulTouches',
       'Dispossessed', 'TotalTackles', 'DribbledPast', 'TotalAttemptedTackles',
       'Total_Interceptions', 'Fouled', 'Fouls', 'Yellow', 'Red',
       'CaughtOffside', 'Total_Clearances', 'ShotsBlocked', 'CrossesBlocked',
       'PassesBlocked', 'Total_Saves', 'Saves_In_SixYardBox',
       'Saves_In_PenaltyArea', 'Saves_From_OutOfBox', 'Total_Passes', 'AccLB',
       'InAccLB', 'AccSP', 'InAccSP', 'Total_Key_Passes', 'Long', 'Short',
       'Cross', 'Corner', 'Throughball', 'Freekick', 'Throwin', 'Other',
       'Total_Assists', 'Captain_Flag', 'Age']]

game = game[~(game['Tournament-fullname']=='0')]

game1 = game.append(checked_1)
game1.reset_index(inplace = True)
del game1['index']

game = game1
del game1

game.columns

#aggregation by averaging all the stats at player level
# and looking them at an stats per minute

#manually correcting some of the classification of players
game.loc[game.Player == 'Cédric Soares',['Position']] = 'DF'
game.loc[game.Player == 'Cédric Soares',['Country']] = 'Portugal'
game.loc[game.Player == 'José Reina',['Position']] = 'GK'
game.loc[game.Player == 'José Reina',['Country']] = 'Spain'
game.loc[game.Player == 'Rodrigo Moreno',['Position']] = 'MF'
game.loc[game.Player == 'Rodrigo Moreno',['Country']] = 'Spain'
game.loc[game.Player == 'Thiago Alcántara',['Position']] = 'MF'
game.loc[game.Player == 'Thiago Alcántara',['Country']] = 'Spain'

game.to_csv('beautiful_game.csv')
