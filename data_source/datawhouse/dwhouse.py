from psycopg2 import Error as DBError
from db_config import conn as db_conn, cursor
from os.path import dirname

DWH_PATH = dirname(__file__)

"""
id uuid NOT NULL CONSTRAINT br_pk PRIMARY KEY CONSTRAINT br_pk_gen DEFAULT gen_random_uuid(),
id uuid NOT NULL CONSTRAINT states_pk PRIMARY KEY CONSTRAINT states_pk_gen DEFAULT gen_random_uuid(),
id uuid NOT NULL CONSTRAINT br_vaci_pk PRIMARY KEY CONSTRAINT br_vaci_pk_gen DEFAULT gen_random_uuid(),
id uuid NOT NULL CONSTRAINT nz_pk PRIMARY KEY CONSTRAINT nz_pk_gen DEFAULT gen_random_uuid(),
id uuid NOT NULL CONSTRAINT araraq_pk PRIMARY KEY CONSTRAINT araraq_pk_gen DEFAULT gen_random_uuid(),
id uuid NOT NULL CONSTRAINT scarlos_pk PRIMARY KEY CONSTRAINT scarlos_pk_gen DEFAULT gen_random_uuid(),
"""

tabelas_dict = {
    'brasil': '''CREATE TABLE IF NOT EXISTS public.brasil (
    regiao text NOT NULL,
    coduf integer NOT NULL,
    data timestamptz NOT NULL UNIQUE,
    semana_epidemiologica integer NOT NULL,
    populacaotcu2019 integer NOT NULL,
    casos_novos integer NOT NULL,
    casos_acumulado integer NOT NULL,
    obitos_acumulado integer NOT NULL,
    obitos_novos integer NOT NULL,
    recuperados_novos integer NOT NULL,
    em_acompanhamento_novos integer NOT NULL);''',

    'brasil_estados': '''CREATE TABLE IF NOT EXISTS public.brasil_estados (
    regiao text NOT NULL,
    estado text NOT NULL,
    coduf integer NOT NULL,
    data timestamptz NOT NULL,
    semana_epidemiologica integer NOT NULL,
    populacaotcu2019 integer NOT NULL,
    casos_acumulado integer NOT NULL,
    casos_novos integer NOT NULL,
    obitos_acumulado integer NOT NULL,
    obitos_novos integer NOT NULL);''',

    'brasil_vacina': '''CREATE TABLE IF NOT EXISTS public.brasil_vacina (
    regiao text NOT NULL,
    coduf integer NOT NULL,
    data timestamptz NOT NULL UNIQUE,
    casos_acumulado integer NOT NULL,
    obitos_novos integer NOT NULL,
    obitos_acumulado integer NOT NULL,
    novas_vacinacoes integer NOT NULL,
    total_vacinacoes integer NOT NULL,
    pessoas_vacinadas integer NOT NULL);''',

    'new_zealand': '''CREATE TABLE IF NOT EXISTS public.new_zealand (
    regiao text NOT NULL,
    coduf text NOT NULL,
    data timestamptz NOT NULL UNIQUE,
    casos_novos integer NOT NULL,
    casos_acumulado integer NOT NULL,
    obitos_novos integer NOT NULL,
    obitos_acumulado integer NOT NULL);''',

    'araraquara': '''CREATE TABLE IF NOT EXISTS public.araraquara (
    municipio text NOT NULL,
    estado text NOT NULL,
    data timestamptz NOT NULL UNIQUE,
    casos_novos integer NOT NULL,
    casos_acumulado integer NOT NULL,
    obitos_novos integer NOT NULL,
    obitos_acumulado integer NOT NULL);''',

    'sao_carlos': '''CREATE TABLE IF NOT EXISTS public.sao_carlos (
    municipio text NOT NULL,
    estado text NOT NULL,
    data timestamptz NOT NULL UNIQUE,
    casos_novos integer NOT NULL,
    casos_acumulado integer NOT NULL,
    obitos_novos integer NOT NULL,
    obitos_acumulado integer NOT NULL);'''
}

tabelas_query = ''
for key in tabelas_dict:
    tabelas_query += tabelas_dict[key] + '\n\n'

if tabelas_query:
    try:
        cursor.execute(tabelas_query)
        db_conn.commit()
    except DBError as e:
        db_conn.rollback()
        print(f"Erro: {str(e)}")