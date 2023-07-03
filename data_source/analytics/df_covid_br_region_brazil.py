import pandas as pd
from os.path import dirname

DATASOURCE_PATH = dirname(dirname(__file__))

df_brasil = pd.read_csv(f'{DATASOURCE_PATH}/curated/brazil_data/HISTORICO_COVIDBR_TODO_O_PERIODO_REGIAO_BRASIL.csv', sep=';')

# Filtro dos casos no Brasil do dia 14 a 28 de março de 2020
df_brasil['casosNovos'][(df_brasil['data'] >= '2020-03-14') & (df_brasil['data'] <= '2020-03-28')]

# Filtro das mortes no Brasil do dia 29 de março até 08 de junho de 2020
df_brasil['obitosNovos'][(df_brasil['data'] >= '2020-03-29') & (df_brasil['data'] <= '2020-06-08')]

# Filtro das mortes no Brasil do dia 28 de fevereiro 2021 até os dias atuais
# Adendo: as mortes a partir de 4 de março de 2023 passaram a ser registradas por semana, isso muda a granularidade das mortes e afeta o gráfico.
df_brasil['obitosNovos'][(df_brasil['data'] >= '2021-02-28') & (df_brasil['data'] <= '2023-03-04')]