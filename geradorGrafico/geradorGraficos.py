"""
Análise de Dados da COVID-19

Este código lê os dados da COVID-19 de um arquivo CSV, extrai informações relevantes para países e realiza análises sobre o número de novos casos. Também gera um gráfico de linha para visualizar os dados.

Autor: [Seu Nome]

Data: [Data]

"""

import pandas as pd
import matplotlib.pyplot as plt


# Passo 1: Ler os dados de um arquivo CSV
df = pd.read_csv('data.csv')

# Passo 2: Extrair informações para países
paises = df.loc[df.place_type == 'Country', :]

# Passo 3: Selecionar colunas relevantes para análise
data = paises[['Date_reported', 'Country_code', 'New_cases', 'New_deaths']]

# Função para filtrar os dados desde o primeiro caso reportado até uma data específica
def desde1caso(data, paises, situacao, start_date, end_date):
    """
    Filtra os dados da COVID-19 para países desde o primeiro caso reportado até uma data específica.

    Args:
        data (DataFrame): DataFrame contendo os dados da COVID-19
        paises (list): Lista de códigos de país para filtrar
        situacao (str): Nome da coluna que representa a situação a ser analisada (por exemplo, 'New_cases' para novos casos)
        start_date (str): Data de início no formato 'AAAA-MM-DD'
        end_date (str): Data de término no formato 'AAAA-MM-DD'

    Returns:
        DataFrame: Dados da COVID-19 filtrados para os países e intervalo de datas especificados
    """

    covid_1 = pd.DataFrame()

    for pais in paises:
        try:
            # Filtrar os dados para o país específico
            df_pais = data.loc[data.Country_code == pais]

            # Agrupar os dados por data e calcular a soma da situação especificada (por exemplo, novos casos, novas mortes)
            df_pais = df_pais.groupby('Date_reported').sum()[situacao].reset_index()

            # Renomear a coluna para o código do país
            df_pais = df_pais.rename(columns={situacao: pais})

            # Definir a data como índice
            df_pais = df_pais.set_index('Date_reported')

            # Concatenar os dados para cada país
            covid_1 = pd.concat([covid_1, df_pais], axis=1)
        except:
            print("Não há dados de " + situacao + " para " + pais)

    # Filtrar os dados para o intervalo de datas especificado
    covid_1 = covid_1.loc[start_date:end_date]

    return covid_1


# Especificar o intervalo de datas e países para análise
start_date = '2020-03-14'
end_date = '2020-03-28'
df_paises = desde1caso(data, ['BR', 'NZ'], 'New_cases', start_date, end_date)

# Imprimir os dados filtrados
print(df_paises)

# Plotar os dados
plt.plot(df_paises)
plt.legend(df_paises.columns)
plt.ylim(ymin=0)
plt.xlim(xmin=0)
plt.show()
