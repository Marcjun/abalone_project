Versión de python - 3.14.7

Paso 1:
    Copiar el URL del repositorio.

Paso 2:
    Abrir Visual Studio Code.
    Terminal -> New Terminal.
        ejecutar git clone URL_DEL_REPOSITORIO
        asegurarse de estar en la carpeta abalone_project
        en caso de no estarlo (si no te aparece en la terminal como 
        ultimo lugar abalone_project, data_path) hacer:  cd abalone_proyect     
        creas el entorno: uv venv [pegar este comando en la terminal]
        instalar los requirements.txt: uv pip install -r requirements.txt [pegar este comando en la terminal]
        
Paso 3:
    Archivo/file->abrir carpeta/open 
    buscas la carpeta abalone_project donde la hayas guardado (Users\Usuario->por defecto)
    folder->seleccionar carpeta/select folder
    
Paso 4:
    Dentro de la carpeta abalone_project encontrar otras carpetas como:
        el .venv (entorno), 
        data(datos procesados en formato csv), 
        models(Guardar el modelo entrenado en formato .pkl),
        notebooks (archivo .ipynb que explica la resolucion del merge_conflict )
        result (guarda los resultados de cada ejecucion,tener en cuenta si vas a ejecutar, tenes que cambiar el numero de metrics_v[numero].json, al igual que en models tenes que cambiar model_v[numero].pkl, no llevan los corchetes)
        src (contiene los dos archivos .py, preprocess.py en donde se aplica el preprocesamiento de los datos y se guardan en formato csv y train_model.py donde se dividen los datos en train y test, se entrena un RandomForestRegressor, se buscan los hiperparametros mediante optuna y se guardan los resultados en 3 archivo metrics_v[numero].json que contien los hiperparametros y metricas de cada ejecucion, el experiments_log.csv que contiene los mismo pero con el dia y la fecha de cada ejecucion (es un data frame))
        
Paso 5:
    Abrir la terminal y darle a  aceptar que confias en la carpeta, en los creadores del proyecto 
Paso 6:
    Parate en la rama main con git switch main
    Para realizar una ejecucion puedes crear una nueva rama con git branch nueva_rama
    Para pasarte a esa rama ejecuta git switch nueva_rama
    Selecciona el archivo train_model.py
    Si vas a modifcar el archivo acordate de modificar las rutas de metrics_v[numero].json y de model_v[numero].pkl para que se almacene las metricas y hiperparametros de tu ejecucion
    Sino solo ejecutalo (Run/Ejecutar)
    Luego en la parte de la izquierda encontraras un simbolo con 3 circulos con bifurcacion
    Encontraras que tenes cambios pendientes en status changes
    Al lado de cada archivo tenes un simbolo +, precionalo, pasan a estar preparados para commit
    en la celda de mensaje coloca algun nombre para identificar que hiciste, dale a confirmar
    te aparecera en el arbol tu nuevo commit

Paso 7: Ejecutar el proyecto

    7.1. Ejecutar el preprocesamiento

        El preprocesamiento prepara los datos para utilizarlos en el entrenamiento del modelo.

        Abrir la terminal de VS Code y asegurarse de estar en la carpeta raíz del proyecto.

        Activar el entorno virtual en PowerShell:

        .\.venv\Scripts\Activate.ps1

        Ejecutar el script de preprocesamiento:

        python -m src.preprocess

        Verificar que se haya generado el archivo:

        data/processed/processed.csv

    7.2. Entrenar y evaluar el modelo

        Verificar que se haya ejecutado el preprocesamiento y que exista data/processed/processed.csv.

        Ejecutar el script de entrenamiento y evaluación:

        python -m src.train_model

        Consultar los resultados generados:

        models/model_v1.pkl: modelo entrenado, si esa es la ruta configurada en el script.

        results/metrics_v1.json: métricas de evaluación e hiperparámetros, si esa es la ruta configurada.

        results/experiments_log.csv: registro de los experimentos, si está habilitado en el script.

        El modelo utilizado es RandomForestRegressor. Se emplea Optuna para buscar hiperparámetros y se evalúa el rendimiento mediante MAE, RMSE y R². También puede calcularse MSE.

Paso 8: Resultados del ejercicio 4

        Se presentan los resultados obtenidos en las distintas versiones de los cambios de hiperparámetros.

    Versión 1

        RMSE: 2.13

        MAE: 1.51

        R²: 0.58

    Versión 2

        RMSE: 2.131806197929393

        MAE: 1.5133299740283601

        R²: 0.5783200391833824

    Versión 3

        RMSE: 2.1974098676645744

        MAE: 1.561604097003035

        R²: 0.5519673513919798
=========================================================
La Explicacion del error esta en el archivo notebook

=========================================================

