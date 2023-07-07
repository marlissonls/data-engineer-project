import pandas as pd
from psycopg2 import Error
from db_config import conn as db_conn
from os.path import dirname

DATASOURCE_PATH = dirname(dirname(__file__))

query_dict = {
    'deaths_br_nz': """SELECT brasil.data AS data, brasil.regiao AS br_pais, brasil.obitos_novos AS br_obitos, new_zealand.regiao AS nz_pais, new_zealand.obitos_novos AS nz_obitos
                       FROM brasil INNER JOIN new_zealand ON brasil.data = new_zealand.data
                       WHERE brasil.data >= '2020-02-25' AND brasil.data <= '2021-02-27'
                       ORDER BY brasil.data ASC""",
    
    'cases_br_nz': """SELECT brasil.data AS data, brasil.regiao AS br_pais, brasil.casos_novos AS br_casos, new_zealand.regiao AS nz_pais, new_zealand.casos_novos AS nz_casos
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

    'br_panorama': """SELECT data, brasil.regiao AS br_pais, obitos_novos AS br_obitos, obitos_acumulado AS br_obitos_acumulado, casos_novos AS br_casos, casos_acumulado AS br_casos_acumulado
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

def get_data_for_analytics(query: str) -> list[tuple]:
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

def save_data_to_csv_for_analytics(analyzed_situation: str, analysis_columns: list):
    analysis_list_of_tuples: list[tuple] = get_data_for_analytics(query_dict[analyzed_situation])

    analysis_list_of_lists: list[list] = list(map(list, analysis_list_of_tuples))

    analysis_dataframe: pd.DataFrame = pd.DataFrame(analysis_list_of_lists, columns=analysis_columns)

    analysis_dataframe[analysis_columns[0]] = pd.to_datetime(analysis_dataframe[analysis_columns[0]], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')

    analysis_dataframe.to_csv(f'{DATASOURCE_PATH}/analytics/{analyzed_situation}.csv', index=False)

# MORTES BRASIL X NOVA ZELÂNDIA ENTRE 2020-02-25 E 2021-02-27
save_data_to_csv_for_analytics('deaths_br_nz',     ['data', 'br_obitos', 'nz_obitos'])
# CASOS BRASIL X NOVA ZELÂNDIA ENTRE 2020-02-25 E 2021-02-27
save_data_to_csv_for_analytics('cases_br_nz',      ['data', 'br_casos', 'nz_casos'])
# PANORAMA BRASIL DE TODO O PERÍODO
save_data_to_csv_for_analytics('br_panorama',      ['data', 'br_obitos', 'br_obitos_acumulado', 'br_casos','br_casos_acumulado'])
# ANÁLISE DO DESEMPENHO DA VACINAÇÃO NO BRASIL APÓS 2021-02-27
save_data_to_csv_for_analytics('deaths_x_vacinas', ['data', 'br_obitos', 'vacinas_acumulado'])
# ANÁLISE DO MAPA DE CALOR DURANTE TODO O PERÍODO
save_data_to_csv_for_analytics('states_heat_map',  ['data', 'regiao', 'estado', 'obitos_novos', 'obitos_acumulado', 'casos_novos', 'casos_acumulado'])
# MORTES ARARAQUARA X SÃO CARLOS ENTRE 17 jan 2021 E 10 abr 2021
save_data_to_csv_for_analytics('deaths_cities',    ['data', 'araraquara_obitos', 'sao_carlos_obitos'])
# CASOS ARARAQUARA X SÃO CARLOS ENTRE 17 jan 2021 E 10 abr 2021
save_data_to_csv_for_analytics('cases_cities',     ['data', 'araraquara_casos', 'sao_carlos_casos'])

db_conn.close()