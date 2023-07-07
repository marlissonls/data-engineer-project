import pandas as pd
from psycopg2 import Error
from db_config import conn as db_conn
import datetime
from os.path import dirname
import numpy as np

DATASOURCE_PATH = dirname(dirname(__file__))

query_dict = {
    'deaths_br_nz': """SELECT brasil.data AS data, brasil.obitos_novos AS br_obitos, new_zealand.obitos_novos AS nz_obitos
                       FROM brasil INNER JOIN new_zealand ON brasil.data = new_zealand.data
                       WHERE brasil.data >= '2020-02-25' AND brasil.data <= '2021-02-27'
                       ORDER BY brasil.data ASC""",
    
    'cases_br_nz': """SELECT brasil.data AS data, brasil.casos_novos AS br_casos, new_zealand.casos_novos AS nz_casos
                      FROM brasil INNER JOIN new_zealand ON brasil.data = new_zealand.data
                      WHERE brasil.data >= '2020-02-25' AND brasil.data <= '2021-02-27'
                      ORDER BY brasil.data ASC""",

    'deaths_cities': """SELECT araraquara.data AS data, araraquara.obitos_novos AS araraquara_obitos, sao_carlos.obitos_novos AS sao_carlos_obitos
                       FROM araraquara INNER JOIN sao_carlos ON araraquara.data = sao_carlos.data
                       WHERE araraquara.data >= '2021-01-17' AND araraquara.data <= '2021-04-10'
                       ORDER BY araraquara.data ASC""",

    'cases_cities': """SELECT araraquara.data AS data, araraquara.casos_novos AS araraquara_casos, sao_carlos.casos_novos AS sao_carlos_casos
                       FROM araraquara INNER JOIN sao_carlos ON araraquara.data = sao_carlos.data
                       WHERE araraquara.data >= '2021-01-17' AND araraquara.data <= '2021-04-10'
                       ORDER BY araraquara.data ASC""",

    'br_panorama': """SELECT data, obitos_novos AS br_obitos, obitos_acumulado AS br_obitos_acumulado, casos_novos AS br_casos, casos_acumulado AS br_casos_acumulado
                      FROM brasil
                      ORDER BY data ASC""",
    
    'deaths_x_vacinas': """SELECT brasil.data AS data, brasil.obitos_novos AS br_obitos, brasil_vacina.total_vacinacoes AS vacinas_acumulado
                           FROM brasil INNER JOIN brasil_vacina ON brasil.data = brasil_vacina.data
                           WHERE brasil.data >= '2021-02-27'
                           ORDER BY data ASC""",
    
    'states_heat_map': """SELECT b.data, b.regiao, b.estado, b.obitos_novos, b.obitos_acumulado, b.casos_novos, b.casos_acumulado
                          FROM brasil_estados AS b
                          INNER JOIN (
                              SELECT estado, MIN(data) AS min_data, MAX(data) AS max_data
                              FROM brasil_estados
                              GROUP BY estado
                          ) AS sub
                          ON b.estado = sub.estado
                          WHERE b.data >= sub.min_data AND b.data <= sub.max_data
                          ORDER BY b.estado ASC, b.data ASC"""
}

def get_data_for_analytics(query):
    try:
        cursor = db_conn.cursor()
        cursor.execute(query)
        db_conn.commit()
        result = cursor.fetchall()
    except Error as DBError:
        db_conn.rollback()
        cursor.close()
        print(DBError)
    else:
        return result
    finally:
        cursor.close()

# MORTES BRASIL X NOVA ZELÂNDIA ENTRE 2020-02-25 E 2021-02-27
deaths_br_nz = get_data_for_analytics(query_dict['deaths_br_nz'])
deaths_br_nz_list = [list(tupla) for tupla in deaths_br_nz]
for i in range(len(deaths_br_nz)):
    deaths_br_nz_list[i][0] = deaths_br_nz_list[i][0].strftime('%Y-%m-%d')
df_deaths_br_nz = pd.DataFrame(deaths_br_nz_list, columns=['data', 'br_obitos', 'nz_obitos'])
df_deaths_br_nz.to_csv(f'{DATASOURCE_PATH}/analytics/deaths_br_nz.csv', index=False)

# CASOS BRASIL X NOVA ZELÂNDIA ENTRE 2020-02-25 E 2021-02-27
cases_br_nz = get_data_for_analytics(query_dict['cases_br_nz'])
cases_br_nz_list = [list(tupla) for tupla in cases_br_nz]
for i in range(len(cases_br_nz)):
    cases_br_nz_list[i][0] = cases_br_nz_list[i][0].strftime('%Y-%m-%d')
df_cases_br_nz = pd.DataFrame(cases_br_nz_list, columns=['data', 'br_casos', 'nz_casos'])
df_cases_br_nz.to_csv(f'{DATASOURCE_PATH}/analytics/cases_br_nz.csv', index=False)

# PANORAMA BRASIL DE TODO O PERÍODO
br_panorama = get_data_for_analytics(query_dict['br_panorama'])
br_panorama_list = [list(tupla) for tupla in br_panorama]
for i in range(len(br_panorama)):
    br_panorama_list[i][0] = br_panorama_list[i][0].strftime('%Y-%m-%d')
df_br_panorama = pd.DataFrame(br_panorama_list, columns=['data', 'br_obitos', 'br_obitos_acumulado', 'br_casos','br_casos_acumulado'])
df_br_panorama.to_csv(f'{DATASOURCE_PATH}/analytics/br_panorama.csv', index=False)

# ANÁLISE DO DESEMPENHO DA VACINAÇÃO NO BRASIL APÓS 2021-02-27
deaths_x_vacinas = get_data_for_analytics(query_dict['deaths_x_vacinas'])
deaths_x_vacinas_list = [list(tupla) for tupla in deaths_x_vacinas]
for i in range(len(deaths_x_vacinas_list)):
    deaths_x_vacinas_list[i][0] = deaths_x_vacinas_list[i][0].strftime('%Y-%m-%d')
df_deaths_x_vacinas = pd.DataFrame(deaths_x_vacinas_list, columns=['data', 'br_obitos', 'vacinas_acumulado'])
df_deaths_x_vacinas.to_csv(f'{DATASOURCE_PATH}/analytics/deaths_x_vacinas.csv', index=False)

# ANÁLISE DO MAPA DE CALOR DURANTE TODO O PERÍODO
states_heat_map = get_data_for_analytics(query_dict['states_heat_map'])
states_heat_map_list = [list(tupla) for tupla in states_heat_map]
for i in range(len(states_heat_map_list)):
    states_heat_map_list[i][0] = states_heat_map_list[i][0].strftime('%Y-%m-%d')
df_states_heat_map = pd.DataFrame(states_heat_map_list, columns=['data', 'regiao', 'estado', 'obitos_novos', 'obitos_acumulado', 'casos_novos', 'casos_acumulado'])
df_states_heat_map.to_csv(f'{DATASOURCE_PATH}/analytics/states_heat_map.csv', index=False)
