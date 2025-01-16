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
    "/home/ras/Documentos/mba/CelularesSubtraidos_2024.xlsx", 
    sheet_name="CELULAR_SEM DUPLI"
)

df_drogas_24_1 = pd.read_excel(
	"/home/ras/Documentos/mba/SPDadosCriminais_2024.xlsx",
	sheet_name = "JAN-JUN_2024"
	)

df_drogas_24_2 = pd.read_excel(
	"/home/ras/Documentos/mba/SPDadosCriminais_2024.xlsx",
	sheet_name = "JUL-NOV_2024"
	)

#%% limpesa roubos
pd.set_option('display.max_columns', None)

print(df_roubos_24.dtypes)

#ver indice colunas
for idx, col in enumerate(df_roubos_24):
    print(f"Índice: {idx}, Coluna: {col}")
    
#excluir coluna por indice    
df_roubos_24 = df_roubos_24.drop(df_roubos_24.columns[[0,1,2,3,8,9,10,11,14,19,20,21,25,27,28,29,31,42,43,44,51]], axis=1)



print(df_roubos_24["CIDADE"].unique())

#filtrar por cidade

df_roubos_24 = df_roubos_24[df_roubos_24["CIDADE"] == "S.PAULO"]

#filrar por bairro
bairros = df_roubos_24["BAIRRO"].unique()

df_bairros = pd.DataFrame(bairros, columns=["Bairros"])

print(df_bairros.to_string())

bairros_centro_expandido = ["LIBERDADE","JARDIM PAULISTA", "SÉ","CENTRO HISTÓRICO DE SÃO PAULO", "CENTRO","REPUBLICA", "REPÚBLICA", "BELA VISTA","CONSOLAÇÃO", "CONSOLACAO","BOM RETIRO","BARRA FUNDA", "HIGIENÓPOLIS", "PARAÍSO", "VILA MARIANA", "ACLIMAÇÃO", "CAMBUCI", "SANTA CECILIA", "SANTA CECÍLIA", "CERQUEIRA CÉSAR", "JARDIM AMERICA","JARDIM AMÉRICA","JARDIM ANÁLIA FRANCO", "ÁGUA BRANCA"]

df_roubos_24 = df_roubos_24[df_roubos_24["BAIRRO"].isin(bairros_centro_expandido)]
