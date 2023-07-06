import pandas as pd
import os
import sys
from dotenv import load_dotenv
import psycopg2

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_database = os.getenv("DB_DATABASE")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_database, user=db_user, password=db_password)
cursor = conn.cursor()

#brasil_csv = pd.read_csv('../data_source/curated/brazil_data/historico_covidbr_todo_periodo_regiao_brasil.csv')
#brasil_estado_csv = pd.read_csv('../data_source/curated/brazil_data/historico_covidbr_todo_periodo_regiao_estados.csv')
#brasil_vacinacao = pd.read_csv('../data_source/curated/brazil_data/clean_data_mortos_apos_vacinacao_brasil_correlacao.csv')
#new_zeland_csv = pd.read_csv('../data_source/curated/new_zeland_data/clean_data_obitos_totais_nz_covid.csv')

tabelas =  """CREATE TABLE IF NOT EXISTS public.brasil (
    id uuid NOT NULL CONSTRAINT br_pk PRIMARY KEY CONSTRAINT br_pk_gen DEFAULT gen_random_uuid(),
    regiao text NOT NULL,
    coduf integer NOT NULL,
    data timestamptz NOT NULL,
    semanaepidemiologica integer NOT NULL,
    populacaotcu2019 integer NOT NULL,
    casosacumulado integer NOT NULL,
    obitosacumulado integer NOT NULL,
    obitosnovos integer NOT NULL,
    recuperadosnovos integer NOT NULL,
    emacompanhamentonovos integer NOT NULL);

    CREATE TABLE IF NOT EXISTS public.brasil_estados (
    id uuid NOT NULL CONSTRAINT states_pk PRIMARY KEY CONSTRAINT states_pk_gen DEFAULT gen_random_uuid(),
    regiao text NOT NULL,
    estado text NOT NULL,
    coduf integer NOT NULL,
    data timestamptz NOT NULL,
    semanaepidemiologica integer NOT NULL,
    populacaotcu2019 integer NOT NULL,
    casosacumulado integer NOT NULL,
    obitosacumulado integer NOT NULL,
    obitosnovos integer NOT NULL);

    CREATE TABLE IF NOT EXISTS public.brasil_vacina (
    id uuid NOT NULL CONSTRAINT br_vaci_pk PRIMARY KEY CONSTRAINT br_vaci_pk_gen DEFAULT gen_random_uuid(),
    regiao text NOT NULL,
    coduf integer NOT NULL,
    data timestamptz NOT NULL,
    casosacumulado integer NOT NULL,
    obitosnovos integer NOT NULL,
    obitosacumulado integer NOT NULL,
    novasvacinacoes integer NOT NULL,
    totalvacinacoes integer NOT NULL,
    pessoasvacinadas integer NOT NULL);

    CREATE TABLE IF NOT EXISTS public.new_zealand (
    id uuid NOT NULL CONSTRAINT nz_pk PRIMARY KEY CONSTRAINT nz_pk_gen DEFAULT gen_random_uuid(),
    regiao text NOT NULL,
    coduf text NOT NULL,
    data timestamptz NOT NULL,
    casosnovos integer NOT NULL,
    casosacumulado integer NOT NULL,
    obitosnovos integer NOT NULL,
    obitosacumulado integer NOT NULL);
    """

if tabelas:
    try:
        cursor.execute(tabelas)
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro: {str(e)}")