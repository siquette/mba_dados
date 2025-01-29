#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 00:20:13 2025

@author: ras
"""

#%%
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, Polygon
from scipy.spatial.distance import pdist
#%%
# Carregando os dados (com os seus caminhos de arquivo)
df_roubos_raw = pd.read_csv("/home/ras/Documentos/mba/mba_dados-main/dados_tratados/df_roubos_24_recort.csv")
area = gpd.read_file("/home/ras/Documentos/mba/mba_dados-main/dados_tratados/centro_expandido_shp/centro_expandido_dissolve.shp")

#%%
meses = [1,2]
df_roubos = df_roubos_raw[df_roubos_raw['MES'].isin(meses)]
df_roubos = df_roubos[['LATITUDE', 'LONGITUDE']]

#%%
try:
    df_roubos  # DataFrame com dados de roubos
    area  # GeoDataFrame com a área de estudo

    # Converter colunas de latitude e longitude para numérico, tratando erros
    for col in ['LATITUDE', 'LONGITUDE']:
        try:
            df_roubos[col] = pd.to_numeric(df_roubos[col], errors='coerce')
        except KeyError:
            print(f"Coluna '{col}' não encontrada no DataFrame df_roubos.")
            raise

    # Remover linhas com valores inválidos (NaN) após a conversão
    df_roubos = df_roubos.dropna(subset=['LATITUDE', 'LONGITUDE'])

    # Criando geometria dos pontos
    geometry = [Point(xy) for xy in zip(df_roubos.LONGITUDE, df_roubos.LATITUDE)]
    df_roubos = gpd.GeoDataFrame(df_roubos, geometry=geometry, crs="EPSG:4326")

    # Verificar se o CRS da área está definido, senão, definir como 4326
    if area.crs is None:
        area.crs = "EPSG:4326"
    
    # Reprojetar ambos os GeoDataFrames para um sistema métrico (UTM Zona 23S - EPSG:31983)
    utm_crs = "EPSG:31983"  # UTM Zona 23S, adequado para São Paulo
    df_roubos = df_roubos.to_crs(utm_crs)
    area = area.to_crs(utm_crs)

    # 1. Visualização
    fig, ax = plt.subplots(figsize=(10, 6))
    area.plot(ax=ax, color='lightgray', edgecolor='black')
    df_roubos.plot(ax=ax, marker='o', color='red', markersize=5)
    plt.title('Distribuição Espacial dos Roubos (Projeção Métrica)')
    plt.xlabel('Coordenada X (metros)')
    plt.ylabel('Coordenada Y (metros)')
    plt.show()

    # 2. Histograma de Distâncias
    # Extrair coordenadas como array NumPy
    coords = np.array(df_roubos.geometry.apply(lambda p: [p.x, p.y]).tolist())
    
    # Calcular distâncias apenas se houver coordenadas válidas
    if coords.size > 0:
        distancias = pdist(coords)  # Cálculo das distâncias (em metros)
        plt.hist(distancias, bins=20, edgecolor='black')
        plt.title('Histograma de Distâncias entre Roubos (em metros)')
        plt.xlabel('Distância (metros)')
        plt.ylabel('Frequência')
        plt.show()
    else:
        print("Não há coordenadas válidas para calcular as distâncias.")

except FileNotFoundError:
    print("Erro: Arquivo CSV ou SHP não encontrado. Certifique-se de que os caminhos dos arquivos estejam corretos.")
except KeyError as e:
    print(f"Erro: Coluna {e} não encontrada no DataFrame.")
except Exception as e:
    print(f"Um erro ocorreu: {e}")
    
    