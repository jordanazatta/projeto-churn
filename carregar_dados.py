# --- Importar as bibliotecas --- #
import pandas as pd
import streamlit as st

@st.cache_data(show_spinner='Carregando os dados...')
def carregar_dados(): # responsável por carregar a base de dados

# --- Ler o arquivo CSV --- #
    df = pd.read_csv('telco.csv')

# --- Retornar a tabela carregada --- #
    return df