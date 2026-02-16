#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import requests

# Configuración de la página
st.set_page_config(page_title="FPC Analytics", layout="wide")
st.title("⚽ Dashboard Fútbol Profesional Colombiano")

# --- FUNCIONES PARA OBTENER DATOS ---
API_KEY = "TU_API_KEY_AQUI"
BASE_URL = "https://v3.football.api-sports.io/" # Ejemplo con API-Football

def get_data(endpoint, params={}):
    headers = {'x-apisports-key': API_KEY}
    response = requests.get(BASE_URL + endpoint, headers=headers, params=params)
    return response.json()['response']

# --- SIDEBAR: FILTRO POR EQUIPO ---
# Primero obtenemos la lista de equipos de la Liga BetPlay
equipos_data = get_data("teams", {"league": 71, "season": 2026})
lista_equipos = {item['team']['name']: item['team']['id'] for item in equipos_data}

st.sidebar.header("Configuración")
equipo_seleccionado = st.sidebar.selectbox("Selecciona tu equipo:", list(lista_equipos.keys()))
id_equipo = lista_equipos[equipo_seleccionado]

st.header("🏆 Tabla de Posiciones")
posiciones = get_data("standings", {"league": 71, "season": 2026})
# Aquí procesas el JSON para convertirlo en un DataFrame de Pandas
df_standing = pd.DataFrame(posiciones[0]['league']['standings'][0]) 
st.table(df_standing[['rank', 'team.name', 'points', 'goalsDiff']])

st.header(f"📅 Últimos Resultados: {equipo_seleccionado}")
resultados = get_data("fixtures", {"team": id_equipo, "last": 5}) # Últimos 5
for partido in resultados:
    col1, col2, col3 = st.columns(3)
    col1.write(partido['teams']['home']['name'])
    col2.write(f"{partido['goals']['home']} - {partido['goals']['away']}")
    col3.write(partido['teams']['away']['name'])

st.header(f"🔜 Próximos Encuentros")
proximos = get_data("fixtures", {"team": id_equipo, "next": 5})
for p in proximos:
    st.info(f"Fecha: {p['fixture']['date']} | {p['teams']['home']['name']} vs {p['teams']['away']['name']}")


