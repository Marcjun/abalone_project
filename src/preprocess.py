import pandas as pd
from pathlib import Path
from sklearn.neighbors import LocalOutlierFactor

base_dir = Path(__file__).resolve().parent.parent 
# Obtiene el path de abalone_project
raw_path = base_dir/ "data" / "raw" / "abalone.csv" 
# Con esto obtiene el path de los datos crudos
processed_dir=  base_dir / "data" / "processed"
# Primero obtengo el directorio de los procesados
processed_path =  processed_dir / "processed.csv"

df = pd.read_csv(raw_path)
print(df.columns)

# Cálculo de una nueva columna age = rings + 1.5 (edad estimada en años). 
df['Age'] = df['Rings'] + 1.5

# Codificación de la variable categórica sex. 
df = pd.get_dummies(df, columns=['Sex'], dtype=int)

# Revisión de valores extremos o atípicos, con un criterio declarado
print(df.info())
#columnas_numericas = df.select_dtypes()
#
#lof = LocalOutlierFactor(n_neighbors=20, contamination='auto')
#pred_lof = lof.fit_predict(df[])


