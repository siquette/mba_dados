# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 16:44:24 2025

@author: Rodrigo-H2R
"""

#%% pacotes
import pandas as pd
import seaborn as sns
import locale
import matplotlib as plt
import numpy as np

#%% importe dados

df_roubos_24 = pd.read_excel(
    "C:/Users/Vivian - H2R/Downloads/mba/dados/CelularesSubtraidos_2024.xlsx", 
    sheet_name="CELULAR_SEM DUPLI"
)

df_drogas_24_1 = pd.read_excel(
	"C:/Users/Vivian - H2R/Downloads/mba/dados/SPDadosCriminais_2024.xlsx",
	sheet_name = "JAN-JUN_2024"
	)

df_drogas_24_2 = pd.read_excel(
	"C:/Users/Vivian - H2R/Downloads/mba/dados/SPDadosCriminais_2024.xlsx",
	sheet_name = "JUL-NOV_2024"
	)

#%% limpesa roubos
# Exibir todas as colunas no DataFrame
pd.set_option('display.max_columns', None)

# Exibir os tipos de dados das colunas
print("Tipos de dados das colunas:")
print(df_roubos_24.dtypes)

# Verificar índice e nome das colunas de forma clara
print("\nÍndices e nomes das colunas:")
for idx, col in enumerate(df_roubos_24.columns):
    print(f"Índice: {idx}, Coluna: {col}")

# Excluir colunas usando os índices especificados
colunas_excluir = [0, 1, 2, 3, 8, 9, 10, 11, 14, 19, 20, 21, 25, 27, 28, 29, 31, 42, 43, 44, 51]
df_roubos_24 = df_roubos_24.drop(df_roubos_24.columns[colunas_excluir], axis=1)

# Exibir os valores únicos da coluna "CIDADE"
print("\nValores únicos na coluna 'CIDADE':")
print(df_roubos_24["CIDADE"].unique())


#filtrar por cidade

df_roubos_24 = df_roubos_24[df_roubos_24["CIDADE"] == "S.PAULO"]




duplicados_roubos = df_roubos_24[df_roubos_24['NUM_BO'].duplicated()]

if not duplicados_roubos.empty:
	print("bos duplicados")
	print(duplicados_roubos)
else:
	print("nenhum bo duplicado")

df_roubos_24 = df_roubos_24.drop_duplicates(subset="NUM_BO", keep=False)

df_roubos_24 = df_roubos_24.dropna(subset=['LATITUDE', 'LONGITUDE'])# Remove linhas com valores NaN

df_roubos_24 = df_roubos_24[(df_roubos_24['LATITUDE'] != 0) & (df_roubos_24['LONGITUDE'] !=0 )]  # Remove linhas com zeros


#%% limpeza df drogas

# Visualizar as 15 primeiras linhas de cada DataFrame original (df_drogas_24_1 e df_drogas_24_2)
df_d_h = df_drogas_24_1.head(15)
df_d_h_2 = df_drogas_24_2.head(15)

# Exibir informações dos DataFrames originais
print("Informações do DataFrame df_drogas_24_1:")
df_drogas_24_1.info()
print("\nInformações do DataFrame df_drogas_24_2:")
df_drogas_24_2.info()

# Excluir colunas desnecessárias de ambos os DataFrames
colunas_excluir = [0, 1, 2, 17, 18, 21]
df_drogas_24_1 = df_drogas_24_1.drop(df_drogas_24_1.columns[colunas_excluir], axis=1)
df_drogas_24_2 = df_drogas_24_2.drop(df_drogas_24_2.columns[colunas_excluir], axis=1)

# Concatenar os dois DataFrames
df_concat_24 = pd.concat([df_drogas_24_1, df_drogas_24_2], axis=0, ignore_index=True)

# Filtrar apenas os registros da cidade de São Paulo
df_concat_24 = df_concat_24[df_concat_24["NOME_MUNICIPIO"] == "S.PAULO"]



df_concat_24 = df_concat_24[(df_concat_24["NATUREZA_APURADA"] == "PORTE DE ENTORPECENTES") | (df_concat_24["NATUREZA_APURADA"] == "TRÁFICO DE ENTORPECENTES")]

df_concat_24_drogas = df_concat_24


duplicados_drogas = df_concat_24_drogas[df_concat_24_drogas['NUM_BO'].duplicated()]

if not duplicados_drogas.empty:
	print("bos duplicados")
	print(duplicados_drogas)
else:
	print("nenhum bo duplicado")

df_concat_24_drogas = df_concat_24_drogas.drop_duplicates(subset='NUM_BO', keep=False)

df_concat_24_drogas = df_concat_24_drogas.dropna(subset=['LATITUDE', 'LONGITUDE'])# Remove linhas com valores NaN

df_concat_24_drogas = df_concat_24_drogas[(df_concat_24_drogas['LATITUDE'] != 0) & (df_concat_24_drogas['LONGITUDE'] !=0 )]  # Remove linhas com zeros

#%%

df_concat_24_drogas .to_csv('df_concat_drogas_24', index=False)
df_roubos_24.to_csv('df_roubos_24', index=False)
#%%
import geopandas as gpd

# Renomear colunas para evitar truncamento
df_concat_24_drogas = df_concat_24_drogas.rename(columns=lambda x: x[:10])

# Remover colunas duplicadas
df_concat_24_drogas = df_concat_24_drogas.loc[:, ~df_concat_24_drogas.columns.duplicated()]


# Converter colunas datetime para string (se existirem)
for col in df_concat_24_drogas.select_dtypes(include=['datetime64[ns]']).columns:
    df_concat_24_drogas[col] = df_concat_24_drogas[col].astype(str)

# Criar o GeoDataFrame
gdf_drogas = gpd.GeoDataFrame(
    df_concat_24_drogas,
    geometry=gpd.points_from_xy(df_concat_24_drogas['LONGITUDE'], df_concat_24_drogas['LATITUDE']),
    crs="EPSG:4326"  # Define o CRS como WGS 84
)

# Salvar como Shapefile
gdf_drogas.to_file("df_drogas_24.shp", driver="ESRI Shapefile")
#%%

# Renomear colunas para evitar truncamento
df_roubos_24 = df_roubos_24.rename(columns=lambda x: x[:10])

# Remover colunas duplicadas
df_roubos_24 = df_roubos_24.loc[:, ~df_roubos_24.columns.duplicated()]

# Converter colunas datetime para string (se existirem)
for col in df_roubos_24.select_dtypes(include=['datetime64[ns]']).columns:
    df_roubos_24[col] = df_roubos_24[col].astype(str)

# Criar o GeoDataFrame
gdf_roubos = gpd.GeoDataFrame(
    df_roubos_24,
    geometry=gpd.points_from_xy(df_roubos_24['LONGITUDE'], df_roubos_24['LATITUDE']),
    crs="EPSG:4326"  # Define o CRS como WGS 84
)

# Salvar como Shapefile
gdf_roubos.to_file("df_roubos_24.shp", driver="ESRI Shapefile")