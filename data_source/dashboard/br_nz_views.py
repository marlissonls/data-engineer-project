import dash
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from dashboard.interactivity import app
from dashboard.data import df_case_nz_br
from dashboard.data import df_deaths_nz_br
from dashboard.data import filtered_df_combined_ar_sc

#gráfico lockdown - MORTES - NZ vs BR
@app.callback(
    Output('graph_lockdown_cases', 'figure'),
    [Input('country-dropdown', 'value')]
)
def graph_lockdown_cases(selected_countries):
    filtered_df = df_case_nz_br[df_case_nz_br['country'].isin(selected_countries)]

    traces = []

    for country in selected_countries:
        country_df = filtered_df[filtered_df['country'] == country]

        traces.append(
            go.Scatter(
                x=country_df['data'],
                y=country_df['br_casos'],
                mode='lines',
                name=country,
                line=dict(width=1.5),
                hoverinfo='text',
                hovertext=(
                        '<b>Data</b>: ' + country_df['data'].astype(str) + '<br>' +
                        '<b>Casos no Brasil</b>: ' + country_df['br_casos'].astype(str) + '<br>'
                )
            )
        )

        traces.append(
            go.Scatter(
                x=country_df['data'],
                y=country_df['nz_casos'],
                mode='lines',
                name='Nova Zelândia',
                line=dict(width=1.5),
                hoverinfo='text',
                hovertext=(
                        '<b>Data</b>: ' + country_df['data'].astype(str) + '<br>' +
                        '<b>Casos na Nova Zelândia</b>: ' + country_df['nz_casos'].astype(str) + '<br>'
                )
            )
        )

    layout = go.Layout(
        yaxis=dict(title='Casos de COVID-19', color='white'),
        hovermode='closest',
        plot_bgcolor='#1f2c56',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title='<b>Data</b>',
            visible=True,
            color='white',
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='white',
            linewidth=1,
            ticks='outside',
            tickfont=dict(family='Arial', size=12, color='white')
        ),
        legend={
            'orientation': 'h',
            'bgcolor': '#1f2c56',
            'x': 0.5,
            'y': 2,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(
            family='sans-serif',
            size=12,
            color='white'
        )
    )

    return {'data': traces, 'layout': layout}

#gráfico lockdown - CASOS - NZ vs BR
@app.callback(
    Output('graph_lockdown_death', 'figure'),
    [Input('country-dropdown', 'value')]
)
def graph_lockdown_death(selected_countries):
    filtered_df = df_deaths_nz_br[df_deaths_nz_br['country'].isin(selected_countries)]

    traces = []

    for country in selected_countries:
        country_df = filtered_df[filtered_df['country'] == country]

        traces.append(
            go.Scatter(
                x=country_df['data'],
                y=country_df['br_obitos'],
                mode='lines',
                name=country,
                line=dict(width=1.5),
                hoverinfo='text',
                hovertext=(
                        '<b>Data</b>: ' + country_df['data'].astype(str) + '<br>' +
                        '<b>óbitos no Brasil</b>: ' + country_df['br_obitos'].astype(str) + '<br>'
                )
            )
        )

        traces.append(
            go.Scatter(
                x=country_df['data'],
                y=country_df['nz_obitos'],
                mode='lines',
                name='Nova Zelândia',
                line=dict(width=1.5),
                hoverinfo='text',
                hovertext=(
                        '<b>Data</b>: ' + country_df['data'].astype(str) + '<br>' +
                        '<b>óbitos na Nova Zelândia</b>: ' + country_df['nz_obitos'].astype(str) + '<br>'
                )
            )
        )

    layout = go.Layout(
        yaxis=dict(title='Óbitos de COVID-19', color='white'),
        hovermode='closest',
        plot_bgcolor='#1f2c56',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title='<b>Data</b>',
            visible=True,
            color='white',
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='white',
            linewidth=1,
            ticks='outside',
            tickfont=dict(family='Arial', size=12, color='white')
        ),
        legend={
            'orientation': 'h',
            'bgcolor': '#1f2c56',
            'x': 0.5,
            'y': 2,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(
            family='sans-serif',
            size=12,
            color='white'
        )
    )

    return {'data': traces, 'layout': layout}

#gráfico lockdown - MORTES - Araraquara vs São Carlos
@app.callback(
    Output('graph_lockdown_cases_sc_ar', 'figure'),
    [Input('country-dropdown', 'value')]
)
def graph_lockdown_cases_sc_ar(selected_countries):
    filtered_df = df_deaths_nz_br[df_deaths_nz_br['municipio'].isin(selected_countries)]

    traces = []
    for country in selected_countries:
        country_df = filtered_df[filtered_df['municipio'] == country]

        traces.append(dict(
            x=country_df['data'],
            y=country_df['casosNovos'],
            mode='lines',
            name=country,
            line=dict(width=1.5),
            hoverinfo='text',
            hovertext=(
                    '<b>Data</b>: ' + country_df['data'].astype(str) + '<br>' +
                    '<b>Casos de  COVID-19</b>: ' + country_df['casosNovos'].astype(str) + '<br>'
            )
        )
        )

    layout = go.Layout(
        yaxis=dict(title='Casos de  COVID-19', color='white'),
        hovermode='closest',
        plot_bgcolor='#1f2c56',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title='<b></b>',
            visible=True,
            color='white',
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='white',
            linewidth=1,
            ticks='outside',
            tickfont=dict(family='Arial', size=12, color='white')
        ),
        legend={
            'orientation': 'h',
            'bgcolor': '#1f2c56',
            'x': 0.5,
            'y': 2,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(
            family='sans-serif',
            size=12,
            color='white'
        )
    )

    return {'data': traces, 'layout': layout}


#gráfico lockdown - CASOS - Araraquara vs São Carlos

@app.callback(
    Output('graph_lockdown_death_sc_ar', 'figure'),
    [Input('country-dropdown', 'value')]
)
def graph_lockdown_death_sc_ar(selected_countries):
        filtered_df = filtered_df_combined_ar_sc[filtered_df_combined_ar_sc['municipio'].isin(selected_countries)]

        traces = []

        for country in selected_countries:
            country_df = filtered_df[filtered_df['municipio'] == country]

            traces.append(dict(
                x=country_df['data'],
                y=country_df['obitosNovos'],
                mode='lines',
                name=country,
                line=dict(width=1.5),
                hoverinfo='text',
                hovertext=(
                        '<b>Data</b>: ' + country_df['data'].astype(str) + '<br>' +
                        '<b>Mortos por COVID-19</b>: ' + country_df['obitosAcumulado'].astype(str) + '<br>'
                )
            )
            )

        layout = go.Layout(
            yaxis=dict(title='Mortos por COVID-19', color='white'),
            hovermode='closest',
            plot_bgcolor='#1f2c56',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title='<b></b>',
                visible=True,
                color='white',
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor='white',
                linewidth=1,
                ticks='outside',
                tickfont=dict(family='Arial', size=12, color='white')
            ),
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'x': 0.5,
                'y': 2,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            font=dict(
                family='sans-serif',
                size=12,
                color='white'
            )
        )

        return {'data': traces, 'layout': layout}

