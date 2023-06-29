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

#print(df_covid_case_world)

# Filtrar os dados entre 2020-03-14 e 2020-03-28
start_date_first_part = '2020-03-14'
end_date_first_part = '2020-03-28'
filtered_df_covid_case_world = df_covid_case_world.loc[(df_covid_case_world['data'] >= start_date_first_part) & (df_covid_case_world['data'] <= end_date_first_part)].copy()

# # Remoção de linhas duplicadas
filtered_df_covid_case_world = filtered_df_covid_case_world.drop_duplicates()
print(filtered_df_covid_case_world)

# # Salvando o DataFrame modificado em um arquivo CSV
#filtered_df_covid_case_world.to_csv('clean_data_covid_case_world.csv', index=False)

# Filtrar os dados entre 2020-03-29 e 2020-06-08
start_date_second_part = '2020-03-29'
end_date_second_part = '2020-06-08'
filtered_second_df_covid_case_world = df_covid_case_world.loc[(df_covid_case_world['data'] >= start_date_second_part) & (df_covid_case_world['data'] <= end_date_second_part)].copy()

# # Remoção de linhas duplicadas
filtered_second_df_covid_case_world = filtered_second_df_covid_case_world.drop_duplicates()

print(filtered_second_df_covid_case_world)

# # Salvando o DataFrame modificado em um arquivo CSV
#filtered_second_df_covid_case_world.to_csv('clean_data_second_covid_case_world.csv', index=False)


