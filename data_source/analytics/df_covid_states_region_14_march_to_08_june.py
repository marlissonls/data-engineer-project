import pandas as pd
from os.path import dirname

DATASOURCE_PATH = dirname(dirname(__file__))

df_states = pd.read_csv(f'{DATASOURCE_PATH}/curated/HIST_COVIDBR_2020_PER_14MARÇO_08JUNHO_REGIAO_ESTADOS.csv', sep=';')

# Divide o DataFrame por estado em um dicionário
states_dict = {}
for estado in df_states['estado'].unique():
    states_dict[estado] = df_states[df_states['estado'] == estado]

print(states_dict['PE'].reset_index(drop=True))