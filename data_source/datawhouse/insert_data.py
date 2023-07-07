import pandas as pd
from db_config import conn as db_conn
from dwhouse import tabelas_dict
from os.path import dirname
import numpy as np

DATASOUCE_PATH = dirname(dirname(__file__))

brasil_csv: pd.DataFrame =           pd.read_csv(f'{DATASOUCE_PATH}/curated/brazil_data/historico_covidbr_todo_periodo_regiao_brasil.csv', sep=';')
brasil_estado_csv: pd.DataFrame =    pd.read_csv(f'{DATASOUCE_PATH}/curated/brazil_data/historico_covidbr_todo_periodo_regiao_estados.csv', sep=';')
brasil_vacinacao_csv: pd.DataFrame = pd.read_csv(f'{DATASOUCE_PATH}/curated/brazil_data/clean_data_mortos_apos_vacinacao_brasil_correlacao.csv')
sp_cidades: pd.DataFrame =           pd.read_csv(f'{DATASOUCE_PATH}/curated/brazil_data/historico_araraquara_saocarlos_sp_1jan_30jun_2021.csv', sep=';')
new_zeland_csv: pd.DataFrame =       pd.read_csv(f'{DATASOUCE_PATH}/curated/new_zeland_data/clean_data_obitos_totais_nz_covid.csv')
araraquara: pd.DataFrame =           sp_cidades[sp_cidades['municipio'] == 'Araraquara'].copy()
sao_carlos: pd.DataFrame =           sp_cidades[sp_cidades['municipio'] == 'São Carlos'].copy()

brasil_csv['data'] =                 pd.to_datetime(brasil_csv['data']).dt.strftime('%Y-%m-%dT12:00:00.000+00:00')
brasil_estado_csv['data'] =          pd.to_datetime(brasil_estado_csv['data']).dt.strftime('%Y-%m-%dT12:00:00.000+00:00')
brasil_vacinacao_csv['data'] =       pd.to_datetime(brasil_vacinacao_csv['data']).dt.strftime('%Y-%m-%dT12:00:00.000+00:00')
new_zeland_csv['data'] =             pd.to_datetime(new_zeland_csv['data']).dt.strftime('%Y-%m-%dT12:00:00.000+00:00')
araraquara['data'] =                 pd.to_datetime(araraquara['data']).dt.strftime('%Y-%m-%dT12:00:00.000+00:00')
sao_carlos['data'] =                 pd.to_datetime(sao_carlos['data']).dt.strftime('%Y-%m-%dT12:00:00.000+00:00')

brasil_list: np.recarray =           brasil_csv.to_records(index=False)
brasil_estado_list: np.recarray =    brasil_estado_csv.to_records(index=False)
brasil_vacinacao_list: np.recarray = brasil_vacinacao_csv.to_records(index=False)
new_zeland_list: np.recarray =       new_zeland_csv.to_records(index=False)
araraquara_list: np.recarray =       araraquara.to_records(index=False)
sao_carlos_list: np.recarray =       sao_carlos.to_records(index=False)

def populate_datawarehouse(table_name: str, dataframe):
    cur = db_conn.cursor()
    
    cur.execute(f'DROP TABLE IF EXISTS {table_name};')
    db_conn.commit()
    
    cur.execute(f'{tabelas_dict[table_name]};')
    db_conn.commit()

    for data in dataframe:
        data = np.where(np.asarray(data).dtype == np.int64, data.astype(int), data)
            
        values = '('
        for i in range(len(data)):
            values += '%s,'
        values = values[:-1]
        values += ')'

        cur.execute(f"INSERT INTO {table_name} VALUES {values}", data)
        db_conn.commit()

populate_datawarehouse('brasil', brasil_list)
populate_datawarehouse('brasil_estados', brasil_estado_list)
populate_datawarehouse('brasil_vacina', brasil_vacinacao_list)
populate_datawarehouse('new_zealand', new_zeland_list)
populate_datawarehouse('araraquara', araraquara_list)
populate_datawarehouse('sao_carlos', sao_carlos_list)

db_conn.close()