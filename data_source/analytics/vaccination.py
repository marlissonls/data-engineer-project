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

# Filtrar os dados entre 2021-01-19 e 2021-02-27
start_date_second_part = '2021-01-19'
end_date_second_part = '2021-02-27'
filtered_second_vaccination_world_copy = df_covid_vaccination_world_copy.loc[(df_covid_vaccination_world_copy['data'] >= start_date_second_part) & (df_covid_vaccination_world_copy['data'] <= end_date_second_part)].copy()

# # Remoção de linhas duplicadas
filtered_second_vaccination_world_copy = filtered_second_vaccination_world_copy.drop_duplicates()

# # Salvando o DataFrame modificado em um arquivo CSV
#filtered_second_vaccination_world_copy.to_csv('clean_data_second_vaccination_world.csv', index=False)

print(filtered_second_vaccination_world_copy)

