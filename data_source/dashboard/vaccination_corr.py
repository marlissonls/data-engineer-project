from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from dashboard.dashboard_layout import app
from dashboard.data import df_vacinacao_obito

##===============correlação vacina vs óbito=======================##

@app.callback(
    Output('graph_corr', 'figure'),
    [Input('brasil-dropdown', 'value')]
)
def vaccinarion_corr_death_graph(countries):
    print('Selected countries:', countries)

    df_corr = df_vacinacao_obito[df_vacinacao_obito['country'].isin(countries)]
    print('Filtered DataFrame:')
    print(df_corr)

    traces = []

    for country in countries:
        df_country = df_corr[df_corr['country'] == country]
        traces.append(
            go.Scatter(
                x=df_country['data'],
                y=df_country['obitosNovos'],
                name=f'Novos Óbitos - {country}'
            )
        )
        traces.append(
            go.Scatter(
                x=df_country['data'],
                y=df_country['totalVacinacoes'],
                name=f'Vacinações Totais - {country}',
                yaxis='y2'
            )
        )

    layout = go.Layout(
        title='Correlação - Óbitos Novos vs. Total de Vacinações',
        yaxis=dict(
            title='Novos Óbitos',
            titlefont=dict(color='black'),
            tickfont=dict(color='black')
        ),
        yaxis2=dict(
            title='Vacinações Totais',
            overlaying='y',
            side='right',
            titlefont=dict(color='orange'),
            tickfont=dict(color='orange')
        ),
        xaxis=dict(title='Valores X'),
        legend=dict(orientation='h')
    )

    return {'data': traces, 'layout': layout}



