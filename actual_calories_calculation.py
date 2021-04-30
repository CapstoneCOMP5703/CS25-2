# -*- coding: utf-8 -*-
"""actual_calories_calculation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jYoswiEyfxGkOxoCoUg6RPoezIYUgaNi
"""

import pandas as pd
import os
from google.colab import drive
drive.mount('/content/drive')

path = "/content/drive/My Drive"

os.chdir(path)
os.listdir(path)

df = pd.read_csv("calorie2.csv")
print(df.head(5))

order=['id','userId','sport','duration','distance','avg_heart_rate','avg_speed','calories']
df=df[order]

from xgboost import XGBRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.model_selection import cross_validate
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_val_score

df=pd.get_dummies(df,columns=['sport'],prefix_sep='_',dummy_na=False,drop_first=False)

X=df.loc[:,df.columns!='calories']
y=df.loc[:,'calories']

model_xgb=XGBRegressor(learning_rate=0.08,n_estimators=1000,max_depth=5,min_child_weight=1)

cv = ShuffleSplit(n_splits=10, test_size=0.3, random_state=0)

scores=cross_val_score(model_xgb,X,y,cv=cv)

print(scores)
print(scores.mean())

df1 = pd.read_csv("calorie_test.csv")

order=['id','userId','sport','duration','distance','avg_heart_rate','avg_speed','calories']
df1=df1[order]

df1=pd.get_dummies(df1,columns=['sport'],prefix_sep='_',dummy_na=False,drop_first=False)

x_test=df1.loc[:,df1.columns!='calories']
y_test=df1.loc[:,'calories']

model_xgb.fit(X,y)

y_train_pred=model_xgb.predict(X)
y_test_pred=model_xgb.predict(x_test)

print(y_test_pred)
print(y_test)

from sklearn.metrics import r2_score,mean_squared_error
import numpy as np

print("R2_score Test:%.3f" % r2_score(y_test,y_test_pred))

rmse=np.sqrt(mean_squared_error(y_test,y_test_pred))
print(rmse)

model_xgb.score(x_test,y_test)

from sklearn.externals import joblib

joblib.dump(model_xgb,'model_xgb.pkl')