import pandas as pd

# # TODO: 1. COVID cases
# # Leitura do arquivo CSV que contém os casos de covid na Nova Zelândia e criação do DataFrame inicial

df_covid_case_nz = pd.read_csv('../raw/covid-case-counts-nz.csv', low_memory=False)

#Renomear as colunas
colunas_pt = {
    'Report Date': 'data',
    'Case Status': 'covidStatus',
    'Sex': 'genero',
    'Age group': 'faixaEtaria',
    'District': 'estado',
    'Overseas travel': 'viagemInternacional',
    'Infection status': 'numeroInfeccoesCovid',
    'Number of cases reported': 'casosNovos'
}
df_covid_case_nz = df_covid_case_nz.rename(columns=colunas_pt)


# # Converter a coluna 'data' para o tipo datetime

df_covid_case_nz['data'] = pd.to_datetime(df_covid_case_nz['data'], format='%Y-%m-%d')

# Filtrar os dados entre 2020-03-14 e 2020-03-28
start_date_first_part = '2020-03-14'
end_date_first_part = '2020-03-28'
filtered_df_covid_case_nz = df_covid_case_nz.loc[(df_covid_case_nz['data'] >= start_date_first_part) & (df_covid_case_nz['data'] <= end_date_first_part)].copy()

# # Remoção de linhas duplicadas
filtered_df_covid_case_nz = filtered_df_covid_case_nz.drop_duplicates()

#
# # # Salvando o DataFrame modificado em um arquivo CSV
#filtered_df_covid_case_nz.to_csv('clean_data_covid_case_nz.csv', index=False)
#
# # Filtrar os dados entre 2020-03-29 e 2020-06-08
start_date_second_part = '2020-03-29'
end_date_second_part = '2020-06-08'
filtered_second_df_covid_case_nz = df_covid_case_nz.loc[(df_covid_case_nz['data'] >= start_date_second_part) & (df_covid_case_nz['data'] <= end_date_second_part)].copy()
#
# # # Remoção de linhas duplicadas
filtered_second_df_covid_case_nz = filtered_second_df_covid_case_nz.drop_duplicates()
#
# # # Salvando o DataFrame modificado em um arquivo CSV
#filtered_second_df_covid_case_nz.to_csv('clean_data_second_covid_case_nz.csv', index=False)
#
print(filtered_df_covid_case_nz)
print(filtered_second_df_covid_case_nz)
#
#
#
# # # TODO: 2. COVID deaths
# # Leitura do arquivo CSV que contém as mortes por semana de covid na Nova Zelândia e criação do DataFrame inicial

df_deaths_covid_nz = pd.read_csv('../raw/weekly-deaths-nz.csv', low_memory=False)

colunas_pt_mortes = {
    'Week ending': 'semanaEpidemiologica',
    'Deaths within 28 days of being reported as case,Deaths attributable to COVID-19': 'obitosNovos'
}
df_deaths_covid_nz = df_deaths_covid_nz.rename(columns=colunas_pt_mortes)


# print(df_deaths_covid_nz.columns)
# # Converter a coluna 'semanaEpidemiologica' para o tipo datetime

df_deaths_covid_nz['semanaEpidemiologica'] = pd.to_datetime(df_deaths_covid_nz['semanaEpidemiologica'])

# Filtrar os dados entre 2020-03-14 e 2020-03-28

filtered_df_deaths_covid_nz = df_deaths_covid_nz.loc[(df_deaths_covid_nz['semanaEpidemiologica'] >= start_date_first_part) & (df_deaths_covid_nz['semanaEpidemiologica'] <= end_date_first_part)].copy()

# # Remoção de linhas duplicadas
filtered_df_deaths_covid_nz = filtered_df_deaths_covid_nz.drop_duplicates()

# # Salvando o DataFrame modificado em um arquivo CSV

#filtered_df_deaths_covid_nz.to_csv('clean_data_deaths_covid_nz.csv', index=False)

print(filtered_df_deaths_covid_nz)


# Filtrar os dados entre 2020-03-29 e 2020-06-08

filtered_second_df_deaths_covid_nz = df_deaths_covid_nz.loc[(df_deaths_covid_nz['semanaEpidemiologica'] >= start_date_second_part) & (df_deaths_covid_nz['semanaEpidemiologica'] <= end_date_second_part)].copy()

# # Remoção de linhas duplicadas
filtered_second_df_deaths_covid_nz = filtered_second_df_deaths_covid_nz.drop_duplicates()

# # Salvando o DataFrame modificado em um arquivo CSV
#filtered_second_df_deaths_covid_nz.to_csv('clean_data_second_deaths_covid_nz.csv', index=False)

print(filtered_second_df_deaths_covid_nz)
#



# # TODO: 3. COVID hospitalisations
# # Leitura do arquivo CSV que contém as hospitalizações por semana de covid na Nova Zelândia e criação do DataFrame inicial
#
# df_hospitalisations_covid_nz = pd.read_csv('csv_data/weekly-hospitalisations-for-covid-nz.csv')
# # print(df_hospitalisations_covid_nz.columns)
#
# # # Converter a coluna 'Admissions for COVID-19 in the week ending' para o tipo datetime
#
# df_hospitalisations_covid_nz['Admissions for COVID-19 in the week ending'] = pd.to_datetime(df_hospitalisations_covid_nz['Admissions for COVID-19 in the week ending'])
#
# # Filtrar os dados entre 2020-03-14 e 2020-03-28
#
# filtered_df_hospitalisations_covid_nz = df_hospitalisations_covid_nz.loc[(df_hospitalisations_covid_nz['Admissions for COVID-19 in the week ending'] >= start_date_first_part) & (df_hospitalisations_covid_nz['Admissions for COVID-19 in the week ending'] <= end_date_first_part)].copy()
#
# # # Remoção de linhas duplicadas
# filtered_df_hospitalisations_covid_nz = filtered_df_hospitalisations_covid_nz.drop_duplicates()
#
# # # Salvando o DataFrame modificado em um arquivo CSV
# filtered_df_hospitalisations_covid_nz.to_csv('clean_data_hospitalisations_covid_nz.csv', index=False)
#
# #print(filtered_df_hospitalisations_covid_nz)
#
#
# # # Filtrar os dados entre 2020-03-29 e 2020-06-08
#
# filtered_second_df_hospitalisations_covid_nz = df_hospitalisations_covid_nz.loc[(df_hospitalisations_covid_nz['Admissions for COVID-19 in the week ending'] >= start_date_second_part) & (df_hospitalisations_covid_nz['Admissions for COVID-19 in the week ending'] <= end_date_second_part)].copy()
#
# # # Remoção de linhas duplicadas
# filtered_second_df_hospitalisations_covid_nz = filtered_second_df_hospitalisations_covid_nz.drop_duplicates()
#
# # # Salvando o DataFrame modificado em um arquivo CSV
# filtered_second_df_hospitalisations_covid_nz.to_csv('clean_data_second_hospitalisations_covid_nz.csv', index=False)

#print(filtered_second_df_hospitalisations_covid_nz)


