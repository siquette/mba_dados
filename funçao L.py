# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 16:10:36 2025

@author: Rodrigo-H2R
"""

#%%
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from libpysal.weights import DistanceBand
from pointpats import PointPattern



#%%

df_roubos_raw = pd.read_csv("C:/Users/Vivian - H2R/Downloads/mba/scrip/dados_tratados/df_roubos_24_recort.csv",dtype={0: str})
area_estudo = gpd.read_file("C:/Users/Vivian - H2R/Downloads/mba/scrip/dados_tratados/centro_expandido_shp/centro_expandido_dissolve.shp")

#%%
meses = [1]
df_roubos = df_roubos_raw[df_roubos_raw['MES'].isin(meses)]
df_roubos = df_roubos[['LATITUDE', 'LONGITUDE']]

#%%
# Verificar se as colunas de latitude e longitude existem no DataFrame
if not {'LATITUDE', 'LONGITUDE'}.issubset(df_roubos.columns):
    raise KeyError("As colunas 'LATITUDE' e/ou 'LONGITUDE' não foram encontradas no DataFrame 'df_roubos'.")

# Converter colunas de latitude e longitude para numérico, substituindo erros por NaN
df_roubos['LATITUDE'] = pd.to_numeric(df_roubos['LATITUDE'], errors='coerce')
df_roubos['LONGITUDE'] = pd.to_numeric(df_roubos['LONGITUDE'], errors='coerce')

# Remover linhas com valores inválidos (NaN) após a conversão
df_roubos = df_roubos.dropna(subset=['LATITUDE', 'LONGITUDE'])

# Criar geometria dos pontos
geometry = [Point(xy) for xy in zip(df_roubos.LONGITUDE, df_roubos.LATITUDE)]
df_roubos = gpd.GeoDataFrame(df_roubos, geometry=geometry, crs="EPSG:4326")

# Verificar se o CRS da área de estudo está definido, senão, definir como EPSG:4326
if area_estudo.crs is None:
    area_estudo.crs = "EPSG:4326"

# Reprojetar ambos os GeoDataFrames para um sistema métrico (UTM Zona 23S - EPSG:31983)
utm_crs = "EPSG:31983"  # UTM Zona 23S, adequado para São Paulo
df_roubos = df_roubos.to_crs(utm_crs)
area_estudo = area_estudo.to_crs(utm_crs)

# Visualização
fig, ax = plt.subplots(figsize=(10, 6))
area_estudo.plot(ax=ax, color='lightgray', edgecolor='black')
df_roubos.plot(ax=ax, marker='o', color='red', markersize=5)
plt.title('Distribuição Espacial dos Roubos (Projeção Métrica)')
plt.xlabel('Coordenada X (metros)')
plt.ylabel('Coordenada Y (metros)')
plt.show()

#%%
df_roubos = gpd.GeoDataFrame(
    df_roubos,
    geometry=gpd.points_from_xy(df_roubos.LONGITUDE, df_roubos.LATITUDE),
    crs="EPSG:4326"
)

#%%
 df_roubos = df_roubos.to_crs(area_estudo.crs)


#%%
import geopandas as gpd
import matplotlib.pyplot as plt
from astropy.stats import RipleysKEstimator
import numpy as np

#%% funçao L

# Converter coordenadas para um array numpy
coords = df_roubos.geometry.apply(lambda geom: (geom.x, geom.y)).tolist()
coords = np.array(coords, dtype=float)

# Obter os limites da área de estudo
xmin, ymin, xmax, ymax = area_estudo.total_bounds
area = (xmax - xmin) * (ymax - ymin)

# Criar o objeto RipleysKEstimator (sem x e y)
rk = RipleysKEstimator(area=area)


# Definir os raios (distâncias)
r = np.linspace(0, 2000, 50) # Ajuste conforme necessário

# Calcular a Função K (passando x e y aqui)
K = rk(data=coords, radii=r) # ou K = rk(coords, r) dependendo da versão


# Calcular a Função L
L = np.sqrt(K/np.pi) - r

# Plotar a função L(r)
plt.plot(r, L, label='Função L(r) observada')
plt.xlabel('Distância (metros)')
plt.ylabel('L(r)')
plt.title('Função L(r) para Análise de Padrões de Pontos')
plt.hlines(0, 0, 2000, color='r', label='Aleatório')
plt.legend()
plt.show()
