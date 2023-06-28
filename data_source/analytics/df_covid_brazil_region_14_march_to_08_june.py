import pandas as pd
from os.path import dirname

DATASOURCE_PATH = dirname(dirname(__file__))

df_brazil = pd.read_csv(f'{DATASOURCE_PATH}/curated/HIST_COVIDBR_2020_PER_14MARÇO_08JUNHO_REGIAO_BRASIL.csv', sep=';')

print(df_brazil)