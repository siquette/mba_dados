# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 16:09:05 2025

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

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

#%% funçao F

# Função para gerar pontos aleatórios dentro da área de estudo
def generate_random_points(polygon, n_points):
    minx, miny, maxx, maxy = polygon.bounds
    points = []
    while len(points) < n_points:
        random_point = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
        if polygon.contains(random_point):
            points.append(random_point)
    return points

# Gerar pontos aleatórios na área de estudo
n_random_points = 1000  # Número de pontos aleatórios
random_points = generate_random_points(area_estudo.unary_union, n_random_points)

# Converter os pontos aleatórios para um array de coordenadas
random_coords = np.array([(point.x, point.y) for point in random_points])

# Converter os pontos observados para um array de coordenadas
observed_coords = np.array([(point.x, point.y) for point in df_roubos.geometry])

# Construir uma árvore de busca para os pontos observados
tree = cKDTree(observed_coords)

# Calcular as distâncias do ponto aleatório mais próximo para cada ponto aleatório
distances, _ = tree.query(random_coords)

# Definir os intervalos de distância para a Função F
radii = np.linspace(0, 2000, 50)  # Ajuste conforme necessário

# Calcular a Função F
F = [np.sum(distances <= r) / n_random_points for r in radii]

# Calcular a Função F esperada sob um padrão CSR
F_expected = radii / radii[-1]  # Função F esperada é linear para um padrão CSR

# Plotar a Função F
plt.plot(radii, F, label='Função F Observada')
plt.plot(radii, F_expected, label='Função F Esperada (CSR)', linestyle='--')
plt.xlabel('Distância (metros)')
plt.ylabel('Função F')
plt.title('Função F para Análise de Padrões de Pontos')
plt.legend()
plt.show()