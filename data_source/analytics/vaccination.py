import pandas as pd
import numpy as np
# # TODO: 1. COVID cases 2020-12-08 e 2021-01-17
# # Leitura do arquivo CSV que contém os dados de vacinação e criação do data frame inicial

df_covid_vaccination_world = pd.read_csv('../raw/vaccination-covid-data.csv')

#Renomear as colunas

colunas_pt = {
    'iso_code': 'coduf',
    'continent': 'continente',
    'location': 'regiao', #é o país
    'date': 'data',
    'total_cases': 'casosAcumulado',
    'total_deaths': 'obitosAcumulado',
    'new_deaths': 'obitosNovos',
    'total_cases_per_million': 'casosAcumuladoMilhao',
    'new_deaths_per_million': 'obitosNovosMilhao',
    'total_vaccinations': 'totalVacinacoes',
    'people_vaccinated': 'pessoasVacinadas',
    'new_vaccinations': 'novasVacinacoes',
}
df_covid_vaccination_world = df_covid_vaccination_world.rename(columns=colunas_pt)


#Converter a coluna 'date' para o tipo datetime

df_covid_vaccination_world['data'] = pd.to_datetime(df_covid_vaccination_world['data'])

#Converter as colunas em float para int
colunas_float = ['casosAcumulado','obitosAcumulado', 'obitosNovos', 'casosAcumuladoMilhao', 'obitosNovosMilhao', 'totalVacinacoes', 'pessoasVacinadas', 'novasVacinacoes']

df_covid_vaccination_world[colunas_float] = df_covid_vaccination_world[colunas_float].fillna(0).astype(int)

colunas = ['coduf', 'continente', 'regiao', 'data', 'casosAcumulado','obitosAcumulado', 'obitosNovos', 'totalVacinacoes', 'pessoasVacinadas', 'novasVacinacoes']

# Criando um novo DataFrame com as colunas selecionadas
df_covid_vaccination_world_copy = df_covid_vaccination_world.loc[:, colunas]

columns_type = df_covid_vaccination_world_copy[colunas].dtypes
# print(columns_type)

# Criar uma cópia do DataFrame original
df_vacinas_mundo = df_covid_vaccination_world_copy.copy()

# # Remoção de linhas duplicadas
df_vacinas_mundo = df_vacinas_mundo.drop_duplicates()

# # # # Salvando o DataFrame modificado em um arquivo CSV
df_vacinas_mundo.to_csv('clean_data_vacina_mundo.csv', index=False)

#======================PARTE DO BRASIL===================================#

# Substituir os valores zerados pelos valores vizinhos
df_vacinas_mundo['totalVacinacoes'] = df_vacinas_mundo['totalVacinacoes'].replace(0, np.nan)
df_vacinas_mundo['totalVacinacoes'] = df_vacinas_mundo['totalVacinacoes'].fillna(method='ffill')
df_vacinas_mundo['totalVacinacoes'] = df_vacinas_mundo['totalVacinacoes'].fillna(method='bfill')

df_vacinas_mundo['novasVacinacoes'] = df_vacinas_mundo['novasVacinacoes'].replace(0, np.nan)
df_vacinas_mundo['novasVacinacoes'] = df_vacinas_mundo['novasVacinacoes'].fillna(method='ffill')
df_vacinas_mundo['novasVacinacoes'] = df_vacinas_mundo['novasVacinacoes'].fillna(method='bfill')

df_vacinas_mundo['obitosNovos'] = df_vacinas_mundo['obitosNovos'].replace(0, np.nan)
df_vacinas_mundo['obitosNovos'] = df_vacinas_mundo['obitosNovos'].fillna(method='ffill')
df_vacinas_mundo['obitosNovos'] = df_vacinas_mundo['obitosNovos'].fillna(method='bfill')

df_vacinas_mundo['obitosAcumulado'] = df_vacinas_mundo['obitosAcumulado'].replace(0, np.nan)
df_vacinas_mundo['obitosAcumulado'] = df_vacinas_mundo['obitosAcumulado'].fillna(method='ffill')
df_vacinas_mundo['obitosAcumulado'] = df_vacinas_mundo['obitosAcumulado'].fillna(method='bfill')

filtered_df_correlacao_vacinas_mortes_brasil = df_vacinas_mundo[df_vacinas_mundo['coduf'] == 'BRA'].copy()

# Adicionar coluna 'country' para identificar o país de origem dos dados
filtered_df_correlacao_vacinas_mortes_brasil.loc[:, 'country'] = 'Brasil'

# Filtrar o DataFrame até a data específica, pois os dados depois de julho/22 estão com muitas colunas faltantes

start_date_morte_antes_vacinacao = '2021-02-27'
end_date_morte_antes_vacinacao = '2022-07-17'

df_mortes_depois_ds_vacinacao_filtrado_br_limite = filtered_df_correlacao_vacinas_mortes_brasil.loc[(filtered_df_correlacao_vacinas_mortes_brasil['data'] >= start_date_morte_antes_vacinacao) & (filtered_df_correlacao_vacinas_mortes_brasil['data'] <= end_date_morte_antes_vacinacao)].copy()


# # # # Salvando o DataFrame modificado em um arquivo CSV
df_mortes_depois_ds_vacinacao_filtrado_br_limite.to_csv('clean_data_mortos_apos_vacinacao_brasil_correlacao.csv', index=False)

# print(df_vacinas_mundo)
print(df_mortes_depois_ds_vacinacao_filtrado_br_limite)


#dropando o coduf para poder fazer a correlação, não é possível fazer com string
df_mortes_depois_ds_vacinacao_filtrado_br_limite.drop('coduf', axis=1, inplace=True)

df_correlation_matrix = df_mortes_depois_ds_vacinacao_filtrado_br_limite

# print(df_correlation_matrix.corr())



