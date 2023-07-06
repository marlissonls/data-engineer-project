CREATE TABLE IF NOT EXISTS public.brasil (
    id uuid NOT NULL CONSTRAINT br_pk PRIMARY KEY CONSTRAINT br_pk_gen DEFAULT gen_random_uuid(),
    regiao text NOT NULL,
    coduf integer NOT NULL,
    data timestamptz NOT NULL UNIQUE,
    semana_epidemiologica integer NOT NULL,
    populacaotcu2019 integer NOT NULL,
    casos_acumulado integer NOT NULL,
    obitos_acumulado integer NOT NULL,
    obitos_novos integer NOT NULL,
    recuperados_novos integer NOT NULL,
    em_acompanhamento_novos integer NOT NULL
);

CREATE TABLE IF NOT EXISTS public.brasil_estados (
    id uuid NOT NULL CONSTRAINT states_pk PRIMARY KEY CONSTRAINT states_pk_gen DEFAULT gen_random_uuid(),
    regiao text NOT NULL,
    estado text NOT NULL,
    coduf integer NOT NULL,
    data timestamptz NOT NULL,
    semana_epidemiologica integer NOT NULL,
    populacaotcu2019 integer NOT NULL,
    casos_acumulado integer NOT NULL,
    obitos_acumulado integer NOT NULL,
    obitos_novos integer NOT NULL
);

CREATE TABLE IF NOT EXISTS public.brasil_vacina (
    id uuid NOT NULL CONSTRAINT br_vaci_pk PRIMARY KEY CONSTRAINT br_vaci_pk_gen DEFAULT gen_random_uuid(),
    regiao text NOT NULL,
    coduf integer NOT NULL,
    data timestamptz NOT NULL UNIQUE,
    casos_acumulado integer NOT NULL,
    obitos_novos integer NOT NULL,
    obitos_acumulado integer NOT NULL,
    novas_vacinacoes integer NOT NULL,
    total_vacinacoes integer NOT NULL,
    pessoas_vacinadas integer NOT NULL
);

CREATE TABLE IF NOT EXISTS public.new_zealand (
    id uuid NOT NULL CONSTRAINT nz_pk PRIMARY KEY CONSTRAINT nz_pk_gen DEFAULT gen_random_uuid(),
    regiao text NOT NULL,
    coduf text NOT NULL,
    data timestamptz NOT NULL UNIQUE,
    casos_novos integer NOT NULL,
    casos_acumulado integer NOT NULL,
    obitos_novos integer NOT NULL,
    obitos_acumulado integer NOT NULL
);

CREATE TABLE IF NOT EXISTS public.araraquara (
    id uuid NOT NULL CONSTRAINT araraq_pk PRIMARY KEY CONSTRAINT araraq_pk_gen DEFAULT gen_random_uuid(),
    municipio text NOT NULL,
    estado text NOT NULL,
    data timestamptz NOT NULL UNIQUE,
    casos_novos integer NOT NULL,
    casos_acumulado integer NOT NULL,
    obitos_novos integer NOT NULL,
    obitos_acumulado integer NOT NULL
);

CREATE TABLE IF NOT EXISTS public.sao_carlos (
    id uuid NOT NULL CONSTRAINT scarlos_pk PRIMARY KEY CONSTRAINT scarlos_pk_gen DEFAULT gen_random_uuid(),
    municipio text NOT NULL,
    estado text NOT NULL,
    data timestamptz NOT NULL UNIQUE,
    casos_novos integer NOT NULL,
    casos_acumulado integer NOT NULL,
    obitos_novos integer NOT NULL,
    obitos_acumulado integer NOT NULL
);