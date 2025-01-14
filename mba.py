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

