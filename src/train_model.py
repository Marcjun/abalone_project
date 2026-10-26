import json
import pandas as pd
import joblib 
import os
import optuna as op
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split 
from sklearn.metrics import mean_squared_error, r2_score,  mean_absolute_error,  root_mean_squared_error
from datetime import datetime
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


#  cant_estimators = trial.suggest_int('n_estimators', 50, 200)# cantidad de árboles del bosque.
#  max_profundidad = trial.suggest_int('max_depth', 3, 20)# profundidad máxima de cada árbo
#  min_samples_split = trial.suggest_int('min_samples_split', 2, 10)# mínimo de observaciones que debe tener cada hoja

  cant_estimators = trial.suggest_int('n_estimators', 10, 400)# cantidad de árboles del bosque.
  max_profundidad = trial.suggest_int('max_depth', 5, 50)# profundidad máxima de cada árbo
  min_samples_split = trial.suggest_int('min_samples_split', 2, 30)# mínimo de observaciones que debe tener cada hoja

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


estudio = op.create_study(
    direction="minimize",
    sampler=op.samplers.TPESampler(seed=42)
    )
#estudio.optimize(func_objec, n_trials=25)
estudio.optimize(func_objec, n_trials=15)

Mejores_params=estudio.best_params
#Entrenar  un modelo de regresión  RandomForestRegressor
pipe = RandomForestRegressor(**Mejores_params, random_state=42) # n_estimators define la cantidad de árboles en el bosque
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
metricas_test= {
  'MAE' : mean_absolute_error(y_test, y_pred),
  'MSE' : mean_squared_error(y_test, y_pred),
  'RMSE' : root_mean_squared_error(y_test, y_pred),
  'R2' : r2_score(y_test, y_pred)
}

for nombre, valor in metricas_test.items():
    print(f"{nombre}: {valor:.2f}")
#Guardar el modelo entrenado 
joblib.dump(pipe, "models/model_v2.pkl", compress=3)
<<<<<<< HEAD
#Guardar sus métricas (MAE, RMSE, R²), hiperparámetros y semilla en results/metrics_v2.json
=======
#Guardar sus métricas (MAE, RMSE, R²), hiperparámetros y semilla en results/metrics_v1.json
>>>>>>> origin/main
datos=	{
		"Métricas":{
		"RMSE": metricas_test['RMSE'],
		"MAE": metricas_test['MAE'],
		"R2": metricas_test['R2']
		},
		"Hiperparámetros":{
		"n_estimators":Mejores_params['n_estimators'],
		"max_depth":Mejores_params['max_depth'],
		"min_samples_split":Mejores_params['min_samples_split']
		},
		"semilla":42
}
with open("results/metrics_v2.json", "w") as f:
    json.dump(datos, f)
#Registrar la ejecución en results/experiments_log.csv
# Registrar la ejecución en results/experiments_log.csv
try:
    df_info = pd.read_csv('results/experiments_log.csv')
    valor = df_info['id_experimento'].iloc[-1]
except (pd.errors.EmptyDataError, IndexError):
    valor = 0

info = {
    "id_experimento": valor+1,
    "DateTime": datetime.now(),
    "model_version": "v1",
    "Hiper_n_estimators":Mejores_params['n_estimators'],
    "Hiper_max_depth":Mejores_params['max_depth'],
    "Hiper_min_samples_split":Mejores_params['min_samples_split'],
    "RMSE": metricas_test['RMSE'],
    "MAE": metricas_test['MAE'],
    "R2": metricas_test['R2']
}
info=pd.DataFrame([info])
info.to_csv(
    'results/experiments_log.csv',
    mode="a",#agrega el nuevo registro al final del archivo, en vez de sobrescribirlo.
    index=False,
    header=os.path.getsize('results/experiments_log.csv') == 0
)