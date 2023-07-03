import pandas as pd
from os.path import dirname

DATASOURCE_PATH = dirname(dirname(__file__))

df_states = pd.read_csv(f'{DATASOURCE_PATH}/curated/brazil_data/HISTORICO_COVIDBR_TODO_O_PERIODO_REGIAO_ESTADOS.csv', sep=';')

# Divide o DataFrame por estado em um dicionário onde as chaves são as siglas de cada estado
states_dict = {}
for estado in df_states['estado'].unique():
    states_dict[estado] = df_states[df_states['estado'] == estado]

# Para selecionar um estado acesse o dicionário usando a sigla do estado
pernamb = states_dict['PE']

# Filtro das mortes nos Estados do dia 14 de março 2020 até 27 de fevereiro 2021
pernamb['obitosNovos'][(pernamb['data'] >= '2020-03-14') & (pernamb['data'] <= '2021-02-27')]