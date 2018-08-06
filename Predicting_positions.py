## -*- coding: utf-8 -*-
"""
@author: Chaitanya
"""
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
game = pd.read_csv('beautiful_game.csv', index_col= 0 )

Positional_skills = game.groupby(['Position', 'Player'], as_index = False).agg({'Mins' : 'sum',
                                                           'Total_Aerial_Duels': 'sum' ,
                                                           'Total_Shots' : 'sum',
                                                           'Total_Goals' : 'sum',
                                                           'Total_Dribbles': 'sum',
                                                           'TotalAttemptedTackles': 'sum',
                                                           'Total_Interceptions' : 'sum', 
                                                           'Fouled' : 'sum', 
                                                           'CaughtOffside' : 'sum',
                                                           'Total_Clearances' : 'sum', 
                                                           'Total_Saves' : 'sum', 
                                                           'ShotsBlocked' : 'sum', 
                                                           'PassesBlocked' : 'sum', 
                                                           'Total_Passes' : 'sum', 
                                                           'AccLB' : 'sum',
                                                           'AccSP' : 'sum',
                                                           'Freekick' : 'sum',  
                                                           'Total_Key_Passes' : 'sum',
                                                           'Corner' : 'sum', 
                                                           'Throughball': 'sum',
                                                           'Total_Assists' : 'sum'})

    
PerMinute_skills = Positional_skills.iloc[:,2:].divide(Positional_skills.Mins, axis = 0)

#Post aggregation of data
X = PerMinute_skills.iloc[:,1:]
y = Positional_skills.iloc[:,0]


from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting classifier to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

y_test = pd.DataFrame(y_test)
y_pred = pd.DataFrame(y_pred)
y_pred.columns = ['Predicted_values']
comparision = pd.concat([y_test.reset_index(drop = True), y_pred], axis = 1)
comparision['result'] = np.where(comparision.Predicted_values == comparision.Position,1,0)
print('percentage accuracy for predicting the position of a player is' , comparision.result.sum()*100/len(y_pred))
### repeating the same for goalkeeper
