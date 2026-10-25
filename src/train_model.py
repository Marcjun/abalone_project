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
#division de datos de train en ajuste y validacion:
X_ajuste, X_val, y_ajuste, y_val = train_test_split(
   		X_train, y_train, test_size=0.3, random_state=42
)
#con optuna busco la mejor combinacion de hiperparametros 
def func_objec (trial):

  cant_estimators = trial.suggest_int('n_estimators', 50, 200)# cantidad de árboles del bosque.
  max_profundidad = trial.suggest_int('max_depth', 3, 20)# profundidad máxima de cada árbo
  min_samples_split = trial.suggest_int('min_samples_split', 2, 10)# mínimo de observaciones que debe tener cada hoja

  modelo = RandomForestRegressor(
      n_estimators = cant_estimators,
      max_depth= max_profundidad,
      min_samples_split= min_samples_split,
      random_state= 42
  )
  modelo.fit(X_ajuste, y_ajuste)
  y_val_pred = modelo.predict(X_val)

  MAE = mean_absolute_error(y_val, y_val_pred)
  MSE = mean_squared_error(y_val, y_val_pred)
  RMSE = root_mean_squared_error(y_val, y_val_pred)
  R2 = r2_score(y_val, y_val_pred)
  trial.set_user_attr("MAE", MAE)
  trial.set_user_attr("MSE", MSE)
  trial.set_user_attr("R2", R2)
  return  RMSE