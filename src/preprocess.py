import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor

base_dir = Path(__file__).resolve().parent.parent 
# Obtiene el path de abalone_project
raw_path = base_dir/ "data" / "raw" / "abalone.csv" 
# Con esto obtiene el path de los datos crudos
processed_dir=  base_dir / "data" / "processed"
# Primero obtengo el directorio de los procesados
processed_path =  processed_dir / "processed.csv"

df = pd.read_csv(raw_path)

# Cálculo de una nueva columna age = rings + 1.5 (edad estimada en años). 
df['Age'] = df['Rings'] + 1.5

# Codificación de la variable categórica sex. 
df = pd.get_dummies(df, columns=['Sex'], dtype=int)

# Revisión de valores extremos o atípicos, con un criterio declarado
columnas_numericas = df.select_dtypes("float64").columns.drop("Age")

scaler = StandardScaler()
df[columnas_numericas] = scaler.fit_transform(df[columnas_numericas])

lof = LocalOutlierFactor(n_neighbors=20, contamination='auto')
pred_lof = lof.fit_predict(df[columnas_numericas])
df['outlier_lof'] = pred_lof == -1
df = df[df["outlier_lof"] == False]

df[columnas_numericas] = scaler.inverse_transform(df[columnas_numericas])
df = df.drop(columns='outlier_lof')

# Guardo el processed
df.to_csv(processed_path, index=False)

# Loggeo 
from logger import log_changes
cambios = "" \
"Saco la columna outlier_lof" 

log_changes(cambios)
