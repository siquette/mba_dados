# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 16:00:24 2025

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


#%% funçao K

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

# Converter coordenadas dos pontos observados para um array numpy 2D
coords = np.array([[geom.x, geom.y] for geom in df_roubos.geometry])

# Área da região de estudo
xmin, ymin, xmax, ymax = area_estudo.total_bounds
area = (xmax - xmin) * (ymax - ymin)

# Número total de pontos
n_points = len(coords)

# Definir os raios (distâncias) para a Função K
radii = np.linspace(0, 2000, 50)  # Ajuste conforme necessário

# Calcular a Função K Observada (com correção de borda por toróide)
K_observed = []
for r in radii:
    count = 0
    for i in range(n_points):
        for j in range(i + 1, n_points):
            # Distância euclidiana com correção de borda por toróide
            dx = abs(coords[i, 0] - coords[j, 0])
            dy = abs(coords[i, 1] - coords[j, 1])
            dx = min(dx, xmax - xmin - dx)
            dy = min(dy, ymax - ymin - dy)
            dist = np.sqrt(dx**2 + dy**2)

            if dist <= r:
                count += 1
    K_observed.append((2 * area / (n_points * (n_points - 1))) * count)

# Calcular a Função K Esperada sob CSR
K_expected = np.pi * radii ** 2

# Plotar a Função K
plt.plot(radii, K_observed, label='Função K Observada')
plt.plot(radii, K_expected, label='Função K Esperada (CSR)', linestyle='--')
plt.xlabel('Distância (metros)')
plt.ylabel('K(r)')
plt.title('Função K de Ripley')
plt.legend()
plt.show()