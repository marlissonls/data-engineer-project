import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from os.path import dirname
import numpy as np

DATA_SOURCE = dirname(dirname(__file__))

df = pd.read_csv(f"{DATA_SOURCE}/analytics/deaths_br_nz.csv") # EXEMPLO DE IMPORTAÇÃO OU LEITURA DE CSV
df_1 = pd.read_csv(f"{DATA_SOURCE}/data_source/curated/brazil_data/HISTORICO_COVIDBR_TODO_O_PERIODO_REGIAO_ESTADOS.csv", sep=";")
df_states = df_1[(~df_1["estado"].isna())]
df_brasil = df[df["regiao"] == "Brasil"]
# df_states.to_csv("df_states_1.csv", index=False)
# df_brasil.to_csv("df_brasil_1.csv", index=False)

# =====================================================================
# Data Load
df_states = pd.read_csv(f"{DATA_SOURCE}/dashboard/datasets/df_states_1.csv")
df_brasil = pd.read_csv(f"{DATA_SOURCE}/dashboard/datasets/df_brasil_1.csv")

#Converter a coluna 'Date_reported' para o tipo datetime
df_brasil['data'] = pd.to_datetime(df_brasil['data'])

token = open(f"{DATA_SOURCE}/dashboard/Dashboard COVID-19/.mapbox_token").read()
brazil_states = json.load(open(f"{DATA_SOURCE}/dashboard/Dashboard COVID-19/geojson/brazil_geo.json", "r"))

brazil_states["features"][0].keys()

df_states_ = df_states[df_states["data"] == "2021-02-27"]
select_columns = {"casosAcumulado": "Casos Acumulados", 
                "casosNovos": "Novos Casos", 
                "obitosAcumulado": "Óbitos Totais",
                "obitosNovos": "Óbitos por Dia"}


# =====================================================================
fig = px.choropleth_mapbox(df_states_, locations="estado",
    geojson=brazil_states, center={"lat": -16.95, "lon": -47.78},
    zoom=4, color="casosNovos", color_continuous_scale="Redor", opacity=0.4,
    hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": True}
    )
fig.update_layout(
                # mapbox_accesstoken=token,
                paper_bgcolor='rgba(0,0,0,0)',
                mapbox_style="carto-darkmatter",
                autosize=True,
                margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                showlegend=False,)
df_data = df_states[df_states["estado"] == "RO"]


fig2 = go.Figure(layout={"template": "plotly_white"})
fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))
fig2.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#1f2c56',
    autosize=True,
    margin=dict(l=10, r=10, b=10, t=10),
    )


# ====================================LAURA - BR vs NZ=================================#

## TODO CASOS COVID BRASIL vs NOVA ZELÂNDIA

df_case_nz_br = pd.read_csv('../data_source/analytics/br_panorama.csv')
df_deaths_nz_br = pd.read_csv('..data_source/analytics/deaths_br_nz.csv')
# Adicionar coluna 'country' para identificar o país de origem dos dados
df_case_nz_br['country'] = 'Nova Zelândia'
df_case_nz_br['country'] = 'Brasil'
df_deaths_nz_br['country'] = 'Nova Zelândia'
df_deaths_nz_br['country'] = 'Brasil'

#==================================================SÃO CARLOS E ARARAQUARA======================================================#
df_deaths_cases_sao_carlos_araraquara = pd.read_csv('../data_source/raw/historico_araraquara_saocarlos_sp_1jan_30jun_2021.csv', sep=";")#obitosNovos/#casosNovos

#Criando um novo DataFrame com as colunas desejadas do DataFrame filtrado

new_df_deaths_cases_br_araraquara_sc = pd.DataFrame({
    'municipio': df_deaths_cases_sao_carlos_araraquara['municipio'],
    'data': df_deaths_cases_sao_carlos_araraquara['data'],
    'casosNovos': df_deaths_cases_sao_carlos_araraquara['casosNovos'],
    'obitosNovos': df_deaths_cases_sao_carlos_araraquara['obitosNovos']

})

# Filtrar os dados de COVID entre 2021-01-17 e 2021-04-10
start_date = '2021-03-18'
end_date = '2021-04-07'

filtered_df_combined_ar_sc = new_df_deaths_cases_br_araraquara_sc.loc[(new_df_deaths_cases_br_araraquara_sc['data'] >= start_date) & (new_df_deaths_cases_br_araraquara_sc['data'] <= end_date)].copy()
#
## TODO CASOS COVID BRASIL APÓS VACINAÇÃO

df_vacinacao_obito = pd.read_csv('../data_source/analytics/deaths_x_vacinas.csv')

df_vacinacao_obito['country'] = 'Brasil'






