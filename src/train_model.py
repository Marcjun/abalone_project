import json
import pandas as pd
import joblib 
import optuna as op
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split 
from sklearn.metrics import mean_squared_error, r2_score,  mean_absolute_error,  root_mean_squared_error

#fijando la semilla (random_state) tanto en la división como en el modelo
#Dividir los datos en entrenamiento y test
#division de datos en train y test

abalone=pd.read_csv('data/processed/processed.csv')
X = abalone.drop(columns=["Rings","Age"])
y = abalone["Age"]

X_train, X_test, y_train, y_test = train_test_split(
		X, y, test_size=0.3, random_state=42
)
