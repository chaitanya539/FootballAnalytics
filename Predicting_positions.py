# -*- coding: utf-8 -*-
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
y1 = pd.get_dummies(y)

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y1, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting classifier to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train.MF)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test.MF, y_pred)

print('percentage accuracy for predicting the position of a midfeilder is' , 100*(cm[0][0]+cm[1][1])/cm.sum())
### repeating the same for goalkeeper

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train.GK)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test.GK, y_pred)

print('percentage accuracy for predicting the position of a goalkeeper is' , 100*(cm[0][0]+cm[1][1])/cm.sum())
#repeating the same for Forwards

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train.FW)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test.FW, y_pred)

print('percentage accuracy for predicting the position of a forward is' , 100*(cm[0][0]+cm[1][1])/cm.sum())

#repeating the same for defenders
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train.DF)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test.DF, y_pred)
print('percentage accuracy for predicting the position of a defender is' , 100*(cm[0][0]+cm[1][1])/cm.sum())
#78% accuracy for DFs
#100% accuracy for goal keepers
#79% accuracy for Forwards
#63.7 % accuracy for Midfielders