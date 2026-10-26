Versión de python - 3.14.7

Se busca clasificar abalones. . . 







\## Correr el Preprocessing



* 1 - Activar el ambiente virtual con:


```

./.venv/Scripts/activate

```



* 2 - Llamar al script de preprocessing con : 

```

python -m src.preprocess

```
* 3 -  Pasos para entrenar y evaluar el modelo:
```
    1.Verificar que se haya ejecutado el preprocessing y que exista el archivo  
    data/processed/processed.csv.
    2.Ejecutar el script de entrenamiento y evaluación
    3.Consultar los resultados obtenidos en la ejecucion:
        models/model_v1.pkl: modelo entrenado.
        results/metrics_v1.json: métricas de evaluación e hiperparámetros del modelo.
        results/experiments_log.csv: registro de los experimentos realizados.
        El modelo utilizado es RandomForestRegressor. Se emplea Optuna para buscar los mejores hiperparámetros y se evalúa el rendimiento mediante MAE, RMSE y R².
```

* 4 - Resultados del ejercicio 4:
Version 1era de los cambios de hiperparametros
MAE: 1.51
MSE: 4.54
RMSE: 2.13
R2: 0.58

Version 2 de los cambios de hiperparametros
RMSE:2.131806197929393
MAE:1.5133299740283601
R2: 0.5783200391833824

Verson 3 de los cambios de hiperparametros




