from dash.dependencies import Input, Output
import plotly.graph_objects as go
from dashboard.interactivity import app
from dashboard.data import filtered_df_combined_br_nz
from dashboard.data import filtered_df_combined_br_nz_second_part
from dashboard.data import filtered_df_combined_br_nz_cases
from dashboard.data import filtered_df_combined_br_nz_cases_second_part

@app.callback(
    Output('first_part_lockdown_death_graph', 'figure'),
    [Input('country-dropdown', 'value')]
)
def graph_lockdown_first(selected_countries):
    filtered_df = filtered_df_combined_br_nz[filtered_df_combined_br_nz['country'].isin(selected_countries)]

    traces = []

    for country in selected_countries:
        country_df = filtered_df[filtered_df['country'] == country]

        traces.append(
            go.Scatter(
                x=country_df['data'],
                y=country_df['obitosNovos'],
                mode='lines',
                name=country,
                line=dict(width=1.5),
                hoverinfo='text',
                hovertext=(
                    '<b>Data</b>: ' + country_df['data'].astype(str) + '<br>' +
                    '<b>Mortes por COVID-19</b>: ' + country_df['obitosNovos'].astype(str) + '<br>'
                )
            )
        )

    layout = go.Layout(
        yaxis=dict(title='Mortes por COVID-19', color='white'),
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


#gráfico da segunda parte do lockdown - MORTES
@app.callback(
    Output('second_part_lockdown_death_graph', 'figure'),
    [Input('country-dropdown', 'value')]
)
def graph_lockdown_second(selected_countries):
    filtered_df = filtered_df_combined_br_nz_second_part[filtered_df_combined_br_nz_second_part['country'].isin(selected_countries)]

    traces = []

    for country in selected_countries:
        country_df = filtered_df[filtered_df['country'] == country]

        traces.append(dict(
            x=country_df['data'],
            y=country_df['obitosNovos'],
            mode='lines',
            name=country,
            line=dict(width=1.5),
            hoverinfo='text',
            hovertext=(
                '<b>Data</b>: ' + country_df['data'].astype(str) + '<br>' +
                '<b>Mortes por COVID-19</b>: ' + country_df['obitosNovos'].astype(str) + '<br>'
                )
            )
        )
    layout = go.Layout(
        height=250,
        yaxis=dict(title='Mortes por COVID-19', color='white'),
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

#gráfico da primeira parte do lockdown - CASOS
@app.callback(
    Output('first_part_lockdown_cases_graph', 'figure'),
    [Input('country-dropdown', 'value')]
)
def graph_cases_first(selected_countries):
    filtered_df = filtered_df_combined_br_nz_cases[filtered_df_combined_br_nz_cases['country'].isin(selected_countries)]

    traces = []

    for country in selected_countries:
        country_df = filtered_df[filtered_df['country'] == country]

        traces.append(dict(
            x=country_df['data'],
            y=country_df['casosNovos'],
            mode='lines',
            name=country,
            line=dict(width=1.5),
            hoverinfo='text',
            hovertext=(
                '<b>Data</b>: ' + country_df['data'].astype(str) + '<br>' +
                '<b>Casos de COVID-19</b>: ' + country_df['casosNovos'].astype(str) + '<br>'
                )
            )
        )

    layout = go.Layout(
        yaxis=dict(title='Casos de COVID-19', color='white'),
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

#gráfico da segunda parte do lockdown - CASOS
@app.callback(
    Output('second_part_lockdown_cases_graph', 'figure'),
    [Input('country-dropdown', 'value')]
)
def graph_cases_second(selected_countries):
    filtered_df = filtered_df_combined_br_nz_cases_second_part[filtered_df_combined_br_nz_cases_second_part['country'].isin(selected_countries)]

    traces = []

    for country in selected_countries:
        country_df = filtered_df[filtered_df['country'] == country]

        traces.append(dict(
            x=country_df['data'],
            y=country_df['casosNovos'],
            mode='lines',
            name=country,
            line=dict(width=1.5),
            hoverinfo='text',
            hovertext=(
                '<b>Data</b>: ' + country_df['data'].astype(str) + '<br>' +
                '<b>Casos de COVID-19</b>: ' + country_df['casosNovos'].astype(str) + '<br>'
            )
        )
    )

    layout = go.Layout(
        yaxis=dict(title='Casos de COVID-19', color='white'),
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