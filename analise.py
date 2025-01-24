# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 21:45:21 2025

@author: rodri
"""
#%%
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point
from libpysal.weights import DistanceBand
import esda
from esda.pointpattern import k_function, f_function, g_function

#%%

df_roubos_raw = pd.read_csv("C:/Users/rodri/Documents/mba_tcc/Nova pasta/Nova pasta (2)/dados_tratados/df_roubos_24_recort.csv")
area = gpd.read_file("C:/Users/rodri/Documents/mba_tcc/Nova pasta/Nova pasta (2)/dados_tratados/centro_expandido_shp/centro_expandido_dissolve.shp")

#%%
meses = [1,2,3,4,5,6]
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
    
    
#%%
try:
    
    df_roubos
    area 

    # Converter colunas de latitude e longitude para numérico, tratando erros
    for col in ['LATITUDE', 'LONGITUDE']:
        try:
            df_roubos[col] = pd.to_numeric(df_roubos[col], errors='coerce')
        except KeyError:
            print(f"Coluna '{col}' não encontrada no DataFrame df_roubos.")
            raise

    # Remover linhas com valores inválidos (NaN) após a conversão
    df_roubos = df_roubos.dropna(subset=['LATITUDE', 'LONGITUDE'])

    # Criando geometria dos pontos (assumindo que os dados já estão em UTM)
    geometry = [Point(xy) for xy in zip(df_roubos.LONGITUDE, df_roubos.LATITUDE)]
    df_roubos = gpd.GeoDataFrame(df_roubos, geometry=geometry, crs="EPSG:31983")

    # Verificar se o CRS da área está definido, senão, definir como 31983
    if area.crs is None:
        area.crs = "EPSG:31983"

    # Garantir que ambos os GeoDataFrames estejam no mesmo CRS
    if df_roubos.crs != area.crs:
        area = area.to_crs(df_roubos.crs)
    
    # Extrair coordenadas como array NumPy
    coords = np.array(df_roubos.geometry.apply(lambda p: [p.x, p.y]).tolist())

    # Criando pesos espaciais (distância - ajuste o threshold conforme necessário)
    w = DistanceBand.from_dataframe(df_roubos, threshold=1000, binary=True, silence_warnings=True) # Threshold em metros


    # Função K de Ripley
    k = k_function(coords, w=w, permutations=99)
    plt.plot(k.support, k.simulations.T, color='lightgrey')
    plt.plot(k.support, k.obs, color='black')
    plt.title("Função K de Ripley")
    plt.xlabel("Distância (metros)")
    plt.ylabel("K(d)")
    plt.show()

    # Função F de espaços vazios
    f = f_function(coords, w=w, permutations=99)
    plt.plot(f.support, f.simulations.T, color='lightgrey')
    plt.plot(f.support, f.obs, color='black')
    plt.title("Função F de Espaços Vazios")
    plt.xlabel("Distância (metros)")
    plt.ylabel("F(d)")
    plt.show()

    # Função G de vizinho mais próximo
    g = g_function(coords, w=w, permutations=99)
    plt.plot(g.support, g.simulations.T, color='lightgrey')
    plt.plot(g.support, g.obs, color='black')
    plt.title("Função G de Vizinho Mais Próximo")
    plt.xlabel("Distância (metros)")
    plt.ylabel("G(d)")
    plt.show()

except FileNotFoundError:
    print("Erro: Arquivo CSV ou SHP não encontrado. Certifique-se de que os caminhos dos arquivos estejam corretos.")
except KeyError as e:
    print(f"Erro: Coluna {e} não encontrada no DataFrame.")
except Exception as e:
    print(f"Um erro ocorreu: {e}")