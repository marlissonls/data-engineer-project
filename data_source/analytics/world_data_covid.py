import pandas as pd

# # TODO: 1. COVID cases
# # Leitura do arquivo CSV que contém os casos de covid no mundo e criação do DataFrame inicial

df_covid_case_world = pd.read_csv('../raw/WHO-COVID-19-global-data.csv')

#print(df_covid_case_world.columns)

#Renomear as colunas

colunas_pt = {
    'Date_reported': 'data',
    'Country_code': 'coduf',
    'Country': 'regiao',
    'WHO_region': 'continente',
    'New_cases': 'casosNovos',
    'Cumulative_cases': 'casosAcumulado',
    'New_deaths': 'obitosNovos',
    'Cumulative_deaths': 'obitosAcumulado'
}
df_covid_case_world = df_covid_case_world.rename(columns=colunas_pt)

#Converter a coluna 'data' para o tipo datetime
df_covid_case_world['data'] = pd.to_datetime(df_covid_case_world['data'])


# # Remoção de linhas duplicadas
filtered_df_covid_case_world = df_covid_case_world.drop_duplicates()
# print(filtered_df_covid_case_world)

# # # Salvando o DataFrame modificado em um arquivo CSV
filtered_df_covid_case_world.to_csv('clean_data_covid_case_world.csv', index=False)


## TODO 3 - MORTES COVID NZ

# Verificar se "NZ" está presente na coluna "coduf"
result = filtered_df_covid_case_world['coduf'].str.contains('NZ', na=False)

# Filtrar o DataFrame usando o resultado da verificação
df_filtered_nz = df_covid_case_world[result]

tipos_de_dados = df_filtered_nz.dtypes

# print(tipos_de_dados)
#
# print(df_filtered_nz)

# # Salvando o DataFrame filtrado em um arquivo CSV
df_filtered_nz.to_csv('clean_data_mortos_totais_nz_covid.csv', index=False)



