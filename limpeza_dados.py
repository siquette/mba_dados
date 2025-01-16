# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 16:46:13 2025

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

#%% limpesa

import pandas as pd

# Função para limpar DataFrame removendo colunas e filtrando por cidade
def clean_dataframe(df, columns_to_drop, city_column, city_name, neighborhood_column=None, neighborhoods_central=None):
    # Remover colunas indesejadas
    df_cleaned = df.drop(df.columns[columns_to_drop], axis=1)
    
    # Filtrar por cidade
    df_cleaned = df_cleaned[df_cleaned[city_column] == city_name]
    
    # Se fornecido, filtrar por bairros centrais
    if neighborhood_column and neighborhoods_central:
        df_cleaned = df_cleaned[df_cleaned[neighborhood_column].isin(neighborhoods_central)]
    
    return df_cleaned

# Função para obter lista de bairros únicos
def get_unique_neighborhoods(df, neighborhood_column):
    neighborhoods = df[neighborhood_column].unique()
    df_neighborhoods = pd.DataFrame({"Bairros": neighborhoods})
    print("Lista de bairros únicos:")
    print(df_neighborhoods.to_string(index=False))
    return df_neighborhoods

# Função principal para processar df_roubos_24
def process_roubos(df_roubos_24):
    # Configuração de opções Pandas
    pd.set_option('display.max_columns', None)
    
    # Informações do DataFrame
    print("Tipos de dados das colunas:")
    print(df_roubos_24.dtypes)
    
    print("\nÍndices e nomes das colunas:")
    for idx, col in enumerate(df_roubos_24.columns):
        print(f"Índice: {idx}, Coluna: {col}")

    # Limpeza do DataFrame de roubos
    colunas_excluir_roubos = [0, 1, 2, 3, 8, 9, 10, 11, 14, 19, 20, 21, 25, 27, 28, 29, 31, 42, 43, 44, 51]
    bairros_centro_expandido_roubos = ["LIBERDADE","JARDIM PAULISTA", "SÉ","CENTRO HISTÓRICO DE SÃO PAULO", "CENTRO","REPUBLICA", "REPÚBLICA", "BELA VISTA", "CONSOLAÇÃO", "CONSOLACAO","BOM RETIRO","BARRA FUNDA", "HIGIENÓPOLIS", "PARAÍSO", "VILA MARIANA", "ACLIMAÇÃO", "CAMBUCI", "SANTA CECILIA", "SANTA CECÍLIA", "CERQUEIRA CÉSAR", "JARDIM AMERICA","JARDIM AMÉRICA","JARDIM ANÁLIA FRANCO", "ÁGUA BRANCA"]

    df_roubos_24_clean = clean_dataframe(df_roubos_24, colunas_excluir_roubos, "CIDADE", "S.PAULO", "BAIRRO", bairros_centro_expandido_roubos)

    # Lista de bairros únicos
    get_unique_neighborhoods(df_roubos_24_clean, "BAIRRO")

    df_roubos_24_clean.to_csv('df_roubos_24', index=False)

# Função principal para processar DataFrames de drogas
def process_drogas(df_drogas_24_1, df_drogas_24_2):
    # Configuração de opções Pandas
    pd.set_option('display.max_columns', None)
    
    # Exibir informações dos DataFrames
    print("Informações do DataFrame df_drogas_24_1:")
    df_drogas_24_1.info()
    print("\nInformações do DataFrame df_drogas_24_2:")
    df_drogas_24_2.info()

    # Limpeza dos DataFrames de drogas
    colunas_excluir_drogas = [0, 1, 2, 17, 18, 21]
    df_drogas_24_1_clean = df_drogas_24_1.drop(df_drogas_24_1.columns[colunas_excluir_drogas], axis=1)
    df_drogas_24_2_clean = df_drogas_24_2.drop(df_drogas_24_2.columns[colunas_excluir_drogas], axis=1)
    
    # Concatenar os DataFrames
    df_concat_24 = pd.concat([df_drogas_24_1_clean, df_drogas_24_2_clean], axis=0, ignore_index=True)

    # Filtrar por cidade e natureza
    bairros_centro_expandido_drogas = ["Liberdade","Consolação", "Cambuci", "Vila da Saúde", "Moema", "Vila Mariana","Ibirapuera","Jardim Anália Franco","JARDIM PAULISTA", "BELA VISTA","SÉ", "CENTRO HISTÓRICO DE SÃO PAULO","CENTRO","LIBERDADE","REPUBLICA", "REPÚBLICA", "BOM RETIRO","CONSOLAÇÃO", "CONSOLACAO", "SANTA CECILIA","SANTA CECÍLIA","CERQUEIRA CÉSAR", "HIGIENÓPOLIS","PARAÍSO","VILA MARIANA","ACLIMAÇÃO","CAMBUCI", "BARRA FUNDA", "ÁGUA BRANCA","PACEMBU","CERQUEIRA CESAR", "VILA BUARQUE", "JARDINS",  "JARDIM AMÉRICA", "VILA NOVA CONCEIÇÃO","JARDIM PAULISTANO", "Sé", "Jardim America",  "Barra Funda", "Vila Maria Baixa", "Jardim America da Penha", "Consolação", "Luz","Santa Cecilia", "Planalto Paulista", "Jardim Europa", "Cerqueira César",  "Vila Romana", "Pompeia", "Aclimação", "Higienópolis", "Ipiranga"]

    df_concat_24 = clean_dataframe(df_concat_24, [], "NOME_MUNICIPIO", "S.PAULO", "BAIRRO", bairros_centro_expandido_drogas)
    df_concat_24 = df_concat_24[df_concat_24["NATUREZA_APURADA"].isin(["PORTE DE ENTORPECENTES", "TRÁFICO DE ENTORPECENTES"])]

    # Lista de bairros únicos
    get_unique_neighborhoods(df_concat_24, "BAIRRO")

    df_concat_24.to_csv('df_concat_drogas_24', index=False)

# Chamar funções principais com seus respectivos DataFrames
process_roubos(df_roubos_24)
process_drogas(df_drogas_24_1, df_drogas_24_2)