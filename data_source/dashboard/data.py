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
# Filtrar o DataFrame até a data específica
filtro_mortes_comeco_vacinacao_br = pd.to_datetime('2021-02-27')
df_brasil = df_brasil.loc[(df_brasil['data'] >= filtro_mortes_comeco_vacinacao_br)]

# =====================================================================

df_deaths_nz = pd.read_csv(f'{DATA_SOURCE}/data_source/curated/new_zeland_data/clean_data_mortos_diarios_nz_comeco_vacinacao.csv')

df_deaths_br = pd.read_csv(f'{DATA_SOURCE}/data_source/curated/brazil_data/HISTORICO_COVIDBR_TODO_O_PERIODO_REGIAO_BRASIL.csv', sep=";")

df_cases_nz_first = pd.read_csv(f'{DATA_SOURCE}/data_source/curated/world_data/clean_data_covid_case_world.csv')#casosNovos

df_cases_nz_second = pd.read_csv(f'{DATA_SOURCE}/data_source/curated/world_data/clean_data_second_covid_case_world.csv')#casosNovos

# Renomear a coluna desejada em um dos DataFrames
df_deaths_nz = df_deaths_nz.rename(columns={'coduf': 'regiao'})

# Adicionar coluna 'country' para identificar o país de origem dos dados
df_deaths_nz['country'] = 'Nova Zelândia'
df_deaths_br['country'] = 'Brasil'

# Combinando os DF's
df_combined_br_nz = pd.concat([df_deaths_br, df_deaths_nz])

## TODO CASOS COVID
# Filtrando o DataFrame df_cases_nz_second pela coluna 'country' com valor 'Nova Zelândia'
filtered_df_cases_nz_first = df_cases_nz_first[df_cases_nz_first['regiao'] == 'New Zealand']
filtered_df_cases_nz_second = df_cases_nz_second[df_cases_nz_second['regiao'] == 'New Zealand']

# Criando um novo DataFrame com as colunas desejadas do DataFrame filtrado

merged_df_cases_nz_first = pd.DataFrame({
    'regiao': filtered_df_cases_nz_first['regiao'],
    'data': filtered_df_cases_nz_first['data'],
    'casosNovos': filtered_df_cases_nz_first['casosNovos']
})

merged_df_cases_nz_second = pd.DataFrame({
    'regiao': filtered_df_cases_nz_second['regiao'],
    'data': filtered_df_cases_nz_second['data'],
    'casosNovos': filtered_df_cases_nz_second['casosNovos']
})

merged_df_cases_brasil = pd.DataFrame({
    'regiao': df_deaths_br['regiao'],
    'data': df_deaths_br['data'],
    'casosNovos': df_deaths_br['casosNovos'],
    'country': df_deaths_br['country']

})

# # Concatenando os DataFrames
merged_df_cases_nz = pd.concat([merged_df_cases_nz_first, merged_df_cases_nz_second], ignore_index=True)
#
merged_df_cases_nz['country'] = 'Nova Zelândia'

# Combinando os DF's dos casos durante o lockdown
df_combined_br_nz_cases = pd.concat([merged_df_cases_brasil, merged_df_cases_nz])


#TODO FILTRO POR DATAS

# Filtrar os dados dos mortos de COVID entre 2020-03-14 e 2020-03-28
start_date_first_part = '2020-03-14'
end_date_first_part = '2020-03-28'
filtered_df_combined_br_nz = df_combined_br_nz.loc[(df_combined_br_nz['data'] >= start_date_first_part) & (df_combined_br_nz['data'] <= end_date_first_part)].copy()

# Filtrar os dados dos casos de COVID entre 2020-03-14 e 2020-03-28
filtered_df_combined_br_nz_cases = df_combined_br_nz_cases.loc[(df_combined_br_nz_cases['data'] >= start_date_first_part) & (df_combined_br_nz_cases['data'] <= end_date_first_part)].copy()

# Filtrar os dados dos mortos de COVID entre 2020-03-29 e 2020-06-08
start_date_second_part = '2020-03-29'
end_date_second_part = '2020-06-08'
filtered_df_combined_br_nz_second_part = df_combined_br_nz.loc[(df_combined_br_nz['data'] >= start_date_second_part) & (df_combined_br_nz['data'] <= end_date_second_part)].copy()

# Filtrar os dados dos casos de COVID entre 2020-03-29 e 2020-06-08
filtered_df_combined_br_nz_cases_second_part = df_combined_br_nz_cases.loc[(df_combined_br_nz_cases['data'] >= start_date_second_part) & (df_combined_br_nz_cases['data'] <= end_date_second_part)].copy()

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


#=====================================CORRELAÇÃO ÓBITOS vs VACINAÇÃO===============================================#

df_correlacao_vacinas_mortes = pd.read_csv(f'{DATA_SOURCE}/data_source/curated/brazil_data/clean_data_mortos_apos_vacinacao_brasil_correlacao.csv')

filtered_df_correlacao_vacinas_mortes = df_correlacao_vacinas_mortes[df_correlacao_vacinas_mortes['coduf'] == 'BRA']

# print(filtered_df_correlacao_vacinas_mortes)
# Criando um novo DataFrame com as colunas desejadas do DataFrame filtrado

df_correlacao_vacinas_mortes_copy = pd.DataFrame({
    'coduf': filtered_df_correlacao_vacinas_mortes['coduf'],
    'data': filtered_df_correlacao_vacinas_mortes['data'],
    'obitosAcumulado': filtered_df_correlacao_vacinas_mortes['obitosAcumulado'],
    'novasVacinacoes': filtered_df_correlacao_vacinas_mortes['novasVacinacoes'],
    'obitosNovos': filtered_df_correlacao_vacinas_mortes['obitosNovos'],
    'totalVacinacoes': filtered_df_correlacao_vacinas_mortes['totalVacinacoes']
})

# Converter a coluna 'data' para o tipo de dados datetime
df_correlacao_vacinas_mortes_copy['data'] = pd.to_datetime(df_correlacao_vacinas_mortes_copy['data'])

# Criar uma cópia do DataFrame original
df_correlacao_vacinas_mortes_copy = filtered_df_correlacao_vacinas_mortes.copy()

# Substituir os valores zerados pelos valores vizinhos
df_correlacao_vacinas_mortes_copy['totalVacinacoes'] = df_correlacao_vacinas_mortes_copy['totalVacinacoes'].replace(0, np.nan)
df_correlacao_vacinas_mortes_copy['totalVacinacoes'] = df_correlacao_vacinas_mortes_copy['totalVacinacoes'].fillna(method='ffill')
df_correlacao_vacinas_mortes_copy['totalVacinacoes'] = df_correlacao_vacinas_mortes_copy['totalVacinacoes'].fillna(method='bfill')

df_correlacao_vacinas_mortes_copy['novasVacinacoes'] = df_correlacao_vacinas_mortes_copy['novasVacinacoes'].replace(0, np.nan)
df_correlacao_vacinas_mortes_copy['novasVacinacoes'] = df_correlacao_vacinas_mortes_copy['novasVacinacoes'].fillna(method='ffill')
df_correlacao_vacinas_mortes_copy['novasVacinacoes'] = df_correlacao_vacinas_mortes_copy['novasVacinacoes'].fillna(method='bfill')

# Verificar os valores preenchidos
dados_preenchidos = df_correlacao_vacinas_mortes_copy['totalVacinacoes'].tolist()

# Adicionar coluna 'country' para identificar o país de origem dos dados
df_correlacao_vacinas_mortes_copy['country'] = 'Brasil'

# # # # Salvando o DataFrame modificado em um arquivo CSV
df_correlacao_vacinas_mortes_copy.to_csv('clean_data_mortos_apos_vacinacao_brasil_correlacao.csv', index=False)

print(df_correlacao_vacinas_mortes_copy)

# fig_corr = go.Figure(
#     data=[
#         go.Scatter(
#             x=df_correlacao_vacinas_mortes_copy['data'],
#             y=df_correlacao_vacinas_mortes_copy['obitosNovos'],
#             name='Novos Óbitos',
#             yaxis='y1'
#         ),
#         go.Scatter(
#             x=df_correlacao_vacinas_mortes_copy['data'],
#             y=df_correlacao_vacinas_mortes_copy['totalVacinacoes'],
#             name='Vacinações Totais',
#             yaxis='y2'
#         )
#     ],
#     layout=go.Layout(
#         title='Correlação - Óbitos Novos vs. Total de Vacinações',
#         yaxis=dict(
#             title='Novos Óbitos',
#             titlefont=dict(color='white'),
#             tickfont=dict(color='white')
#         ),
#         yaxis2=dict(
#             title='Vacinações Totais',
#             overlaying='y',
#             side='right',
#             titlefont=dict(color='orange'),
#             tickfont=dict(color='orange')
#         ),
#         xaxis=dict(title='Valores X'),
#         legend=dict(orientation='h'),
#     )
# )
#
#
#
