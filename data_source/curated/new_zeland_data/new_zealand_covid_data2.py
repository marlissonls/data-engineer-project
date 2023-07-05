import pandas as pd

df = pd.read_csv('clean_data_mortos_totais_nz_covid.csv')

print(df.info())

""" df = df.drop(['continente'], axis=1)

df['obitosAcumulado'] = df['obitosAcumulado'].astype(int)

df['obitosNovos'] = df['obitosNovos'].astype(int)

df['totalVacinacoes'] = df['totalVacinacoes'].astype(int)

df['novasVacinacoes'] = df['novasVacinacoes'].astype(int) 

df = df[['regiao', 'coduf', 'data', 'casosNovos', 'casosAcumulado', 'obitosNovos', 'obitosAcumulado']]

print(df)

df.to_csv('clean_data_mortos_totais_nz_covid.csv', index=False)"""