import pandas as pd
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

colunas = ['coduf', 'continente', 'regiao', 'data', 'casosAcumulado','obitosAcumulado', 'obitosNovos', 'casosAcumuladoMilhao', 'obitosNovosMilhao', 'totalVacinacoes', 'pessoasVacinadas', 'novasVacinacoes']

# columns_type = df_covid_vaccination_world[colunas].dtypes
# print(columns_type)

# Criando um novo DataFrame com as colunas selecionadas
df_covid_vaccination_world_copy = df_covid_vaccination_world.loc[:, colunas]


# Filtrar os dados entre 2020-12-08 e 2021-01-17
start_date_first_part = '2020-12-08'
end_date_first_part = '2021-01-17'
filtered_vaccination_world_copy = df_covid_vaccination_world_copy.loc[(df_covid_vaccination_world_copy['data'] >= start_date_first_part) & (df_covid_vaccination_world_copy['data'] <= end_date_first_part)].copy()

# # Remoção de linhas duplicadas
filtered_vaccination_world_copy = filtered_vaccination_world_copy.drop_duplicates()

# dados_brazil = filtered_df_covid_vaccination_world_copy[filtered_df_covid_vaccination_world_copy['location'].str.contains('Brazil')][colunas]
# print(dados_brazil['total_vaccinations'])

# # Salvando o DataFrame modificado em um arquivo CSV
#filtered_vaccination_world_copy.to_csv('clean_data_vaccination_world.csv', index=False)

print(filtered_vaccination_world_copy)

# # TODO: 2. COVID cases - 2021-01-19 e 2021-02-27

#Um exemplo foi o início da campanha de vacinação contra a covid-19, ocorrida em 2021-02-27

# Filtrar os dados dos mortos por COVID entre 2021-01-19 e 2021-02-27
start_date_second_part = '2021-01-19'
end_date_second_part = '2021-02-27'
filtered_second_vaccination_world_copy = df_covid_vaccination_world_copy.loc[(df_covid_vaccination_world_copy['data'] >= start_date_second_part) & (df_covid_vaccination_world_copy['data'] <= end_date_second_part)].copy()

# # Remoção de linhas duplicadas
filtered_second_vaccination_world_copy = filtered_second_vaccination_world_copy.drop_duplicates()

# # Salvando o DataFrame modificado em um arquivo CSV
#filtered_second_vaccination_world_copy.to_csv('clean_data_second_vaccination_world.csv', index=False)

print(filtered_second_vaccination_world_copy)

## TODO 3 - COVID MORTES ANTES DA VACINA - 14/03/2020 ATÉ 07/12/2020
#'coduf', 'data','obitosAcumulado', 'obitosNovos', 'totalVacinacoes', 'pessoasVacinadas', 'novasVacinacoes'

# # Filtrar os dados dos mortos por COVID entre 2020-03-14 e 2020-12-07

start_date_morte_antes_vacinacao = '2020-03-14'
end_date_morte_antes_vacinacao = '2020-12-07'

filtered_df_covid_case_world_antes_vacinacao = df_covid_vaccination_world_copy.loc[(df_covid_vaccination_world_copy['data'] >= start_date_morte_antes_vacinacao) & (df_covid_vaccination_world_copy['data'] <= end_date_morte_antes_vacinacao)].copy()

# # # Remoção de linhas duplicadas
filtered_df_covid_case_world_antes_vacinacao = filtered_df_covid_case_world_antes_vacinacao.drop_duplicates()

# Criar um novo DataFrame com as colunas desejadas
df_coluna_mortos_antes_vacinacao = filtered_df_covid_case_world_antes_vacinacao[['coduf', 'data', 'obitosNovos', 'totalVacinacoes', 'pessoasVacinadas', 'novasVacinacoes']].copy()


#print(df_coluna_mortos_antes_vacinacao)

#result = df_coluna_mortos_antes_vacinacao['coduf'].str.contains('BR', na=False)

# Exibir as linhas do DataFrame onde "NZ" está presente na coluna "coduf"
#print(df_coluna_mortos_antes_vacinacao[result])

# # # Salvando o DataFrame modificado em um arquivo CSV
#df_coluna_mortos_antes_vacinacao.to_csv('clean_data_mortos_diarios_antes_vacinacao-mundo.csv', index=False)

# TODO 4 - COVID MORTES DEPOIS DA VACINA - 08/12/2020 - ATÉ HOJE
# 'coduf', 'data','obitosAcumulado', 'obitosNovos', 'totalVacinacoes', 'pessoasVacinadas', 'novasVacinacoes'

# Filtrar o DataFrame até a data específica
filtro_mortes_depois_da_vacinacao_mundo= pd.to_datetime('2021-02-27')

df_mortes_depois_ds_vacinacao_filtrado = df_covid_vaccination_world_copy.loc[(df_covid_vaccination_world_copy['data'] >= filtro_mortes_depois_da_vacinacao_mundo)]

# Criar um novo DataFrame com as colunas desejadas
df_coluna_mortos_vacinacao = df_mortes_depois_ds_vacinacao_filtrado[['coduf', 'data', 'obitosNovos', 'obitosAcumulado', 'totalVacinacoes', 'pessoasVacinadas', 'novasVacinacoes']].copy()

# # # Remoção de linhas duplicadas
df_coluna_mortos_vacinacao = df_coluna_mortos_vacinacao.drop_duplicates()

#print(df_coluna_mortos_vacinacao)

# # # Salvando o DataFrame modificado em um arquivo CSV
df_coluna_mortos_vacinacao.to_csv('clean_data_mortos_diarios_apos_comeco_vacinacao_mundo.csv', index=False)

#criando o DF que usaremos para fazer a correlação do total de óbitos acumulados por total de vacinações
df_covid_vaccination_correlacao = pd.read_csv(
    '../curated/world_data/clean_data_mortos_diarios_apos_comeco_vacinacao_mundo.csv')

#Buscando só pelos dados do BRA
df_covid_vaccination_correlacao = df_covid_vaccination_correlacao.loc[df_covid_vaccination_correlacao['coduf'] == 'BRA'].copy()

#tranformando data pra datetime
df_covid_vaccination_correlacao['data'] = pd.to_datetime(df_covid_vaccination_correlacao['data'])

# Filtrar o DataFrame até a data específica, pois os dados depois de julho/22 estão com muitas colunas faltantes

start_date_morte_antes_vacinacao = '2021-02-27'
end_date_morte_antes_vacinacao = '2022-07-17'

df_mortes_depois_ds_vacinacao_filtrado_br_limite = df_covid_vaccination_correlacao.loc[(df_covid_vaccination_correlacao['data'] >= start_date_morte_antes_vacinacao) & (df_covid_vaccination_correlacao['data'] <= end_date_morte_antes_vacinacao)].copy()



print(df_mortes_depois_ds_vacinacao_filtrado_br_limite)

#dropando o coduf para poder fazer a correlação, não é possível fazer com string
df_mortes_depois_ds_vacinacao_filtrado_br_limite.drop('coduf', axis=1, inplace=True)

df_correlation_matrix = df_mortes_depois_ds_vacinacao_filtrado_br_limite


print(df_correlation_matrix.corr())

# # # # Salvando o DataFrame modificado em um arquivo CSV
df_coluna_mortos_vacinacao.to_csv('clean_data_mortos_apos_vacinacao_brasil_correlacao.csv', index=False)

