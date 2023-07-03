import pandas as pd
from os.path import dirname

DATASOURCE_PATH = dirname(dirname(__file__))

df_brazil = pd.read_csv(f'{DATASOURCE_PATH}/curated/brazil_data/HISTORICO_COVIDBR_TODO_O_PERIODO_REGIAO_BRASIL.csv', sep=';')

#print(df_brazil)

print(df_brazil[(df_brazil['data'] >= '2020-03-14') & (df_brazil['data'] <= '2020-03-28')])