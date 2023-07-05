import pandas as pd

df = pd.read_csv('clean_data_mortos_apos_vacinacao_brasil_correlacao.csv')

df = df.drop(['continente', 'country'], axis=1)

df['coduf'] = df['coduf'].replace('BRA', 76)

df['regiao'] = df['regiao'].replace('Brazil', 'Brasil')

df['obitosAcumulado'] = df['obitosAcumulado'].astype(int)

df['obitosNovos'] = df['obitosNovos'].astype(int)

df['totalVacinacoes'] = df['totalVacinacoes'].astype(int)

df['novasVacinacoes'] = df['novasVacinacoes'].astype(int)

df = df[['regiao', 'coduf', 'data', 'casosAcumulado', 'obitosNovos', 'obitosAcumulado', 'novasVacinacoes', 'totalVacinacoes', 'pessoasVacinadas']]

print(df)

df.to_csv('clean_data_mortos_apos_vacinacao_brasil_correlacao.csv', index=False)