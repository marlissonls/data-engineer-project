import pandas as pd
from os.path import dirname

DATASOURCE_PATH = dirname(dirname(__file__))

df_states = pd.read_csv(f'{DATASOURCE_PATH}/curated/brazil_data/HISTORICO_COVIDBR_TODO_O_PERIODO_REGIAO_ESTADOS.csv', sep=';')

# Divide o DataFrame por estado em um dicionário onde as chaves são as siglas de cada estado
states_dict = {}
for estado in df_states['estado'].unique():
    states_dict[estado] = df_states[df_states['estado'] == estado]

# Para mostrar os dados de Pernambuco considerando o período do início da pandemia até os dias de hoje
pernamb = states_dict['PE']
#print(pernamb.reset_index(drop=True))

# Para mostrar dados de datas específicas
print(pernamb[(pernamb['data'] >= '2020-03-14') & (pernamb['data'] <= '2020-03-28')])