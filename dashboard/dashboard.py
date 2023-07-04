import dash
from dash import dcc, html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import json

CENTER_LAT, CENTER_LON = -14.272572694355336, -51.25567404158474

# =====================================================================
# Data Generation
df = pd.read_csv("../data_source/curated/brazil_data/HISTORICO_COVIDBR_TODO_O_PERIODO_REGIAO_BRASIL.csv", sep=";")
df_1 = pd.read_csv("../data_source/curated/brazil_data/HISTORICO_COVIDBR_TODO_O_PERIODO_REGIAO_ESTADOS.csv", sep=";")
df_states = df_1[(~df_1["estado"].isna())]
df_brasil = df[df["regiao"] == "Brasil"]
# df_states.to_csv("df_states_1.csv", index=False)
# df_brasil.to_csv("df_brasil_1.csv", index=False)

# =====================================================================
# Data Load
df_states = pd.read_csv("df_states_1.csv")
df_brasil = pd.read_csv("df_brasil_1.csv")

#Converter a coluna 'Date_reported' para o tipo datetime
df_brasil['data'] = pd.to_datetime(df_brasil['data'])

token = open("../dashboard/Dashboard COVID-19/.mapbox_token").read()
brazil_states = json.load(open("../dashboard/Dashboard COVID-19/geojson/brazil_geo.json", "r"))

brazil_states["features"][0].keys()

df_states_ = df_states[df_states["data"] == "2021-02-27"]
select_columns = {"casosAcumulado": "Casos Acumulados", 
                "casosNovos": "Novos Casos", 
                "obitosAcumulado": "Óbitos Totais",
                "obitosNovos": "Óbitos por Dia"}


# =====================================================================
# Filtrar o DataFrame até a data específica
filtro_mortes_comeco_vacinacao_br = pd.to_datetime('2021-02-27')
df_brasil = df_brasil.loc[(df_brasil['data'] >= filtro_mortes_comeco_vacinacao_br)]

# =====================================================================

df_deaths_nz = pd.read_csv('../data_source/curated/new_zeland_data/clean_data_mortos_diarios_nz_comeco_vacinacao.csv')

df_deaths_br = pd.read_csv('../data_source/curated/brazil_data/HISTORICO_COVIDBR_TODO_O_PERIODO_REGIAO_BRASIL.csv', sep=";")

df_cases_nz_first = pd.read_csv('../data_source/curated/world_data/clean_data_covid_case_world.csv')#casosNovos

df_cases_nz_second = pd.read_csv('../data_source/curated/world_data/clean_data_second_covid_case_world.csv')#casosNovos

# Renomear a coluna desejada em um dos DataFrames
df_deaths_nz = df_deaths_nz.rename(columns={'coduf': 'regiao'})

# Adicionar coluna 'country' para identificar o país de origem dos dados
df_deaths_nz['country'] = 'Nova Zelândia'
df_deaths_br['country'] = 'Brasil'

# Combinando os DF's
df_combined_br_nz = pd.concat([df_deaths_br, df_deaths_nz])

## TODO CASOS COVID
# Filtrando o DataFrame df_cases_nz_second pela coluna 'country' com valor 'Nova Zelândia'
filtered_df_cases_nz_first = df_cases_nz_first[df_cases_nz_first['regiao'] == 'New Zealand']
filtered_df_cases_nz_second = df_cases_nz_second[df_cases_nz_second['regiao'] == 'New Zealand']

# Criando um novo DataFrame com as colunas desejadas do DataFrame filtrado

merged_df_cases_nz_first = pd.DataFrame({
    'regiao': filtered_df_cases_nz_first['regiao'],
    'data': filtered_df_cases_nz_first['data'],
    'casosNovos': filtered_df_cases_nz_first['casosNovos']
})

merged_df_cases_nz_second = pd.DataFrame({
    'regiao': filtered_df_cases_nz_second['regiao'],
    'data': filtered_df_cases_nz_second['data'],
    'casosNovos': filtered_df_cases_nz_second['casosNovos']
})

merged_df_cases_brasil = pd.DataFrame({
    'regiao': df_deaths_br['regiao'],
    'data': df_deaths_br['data'],
    'casosNovos': df_deaths_br['casosNovos'],
    'country': df_deaths_br['country']

})

# # Concatenando os DataFrames
merged_df_cases_nz = pd.concat([merged_df_cases_nz_first, merged_df_cases_nz_second], ignore_index=True)
#
merged_df_cases_nz['country'] = 'Nova Zelândia'

# Combinando os DF's dos casos durante o lockdown
df_combined_br_nz_cases = pd.concat([merged_df_cases_brasil, merged_df_cases_nz])


#TODO FILTRO POR DATAS

# Filtrar os dados dos mortos de COVID entre 2020-03-14 e 2020-03-28
start_date_first_part = '2020-03-14'
end_date_first_part = '2020-03-28'
filtered_df_combined_br_nz = df_combined_br_nz.loc[(df_combined_br_nz['data'] >= start_date_first_part) & (df_combined_br_nz['data'] <= end_date_first_part)].copy()

# Filtrar os dados dos casos de COVID entre 2020-03-14 e 2020-03-28
filtered_df_combined_br_nz_cases = df_combined_br_nz_cases.loc[(df_combined_br_nz_cases['data'] >= start_date_first_part) & (df_combined_br_nz_cases['data'] <= end_date_first_part)].copy()

# Filtrar os dados dos mortos de COVID entre 2020-03-29 e 2020-06-08
start_date_second_part = '2020-03-29'
end_date_second_part = '2020-06-08'
filtered_df_combined_br_nz_second_part = df_combined_br_nz.loc[(df_combined_br_nz['data'] >= start_date_second_part) & (df_combined_br_nz['data'] <= end_date_second_part)].copy()

# Filtrar os dados dos casos de COVID entre 2020-03-29 e 2020-06-08
filtered_df_combined_br_nz_cases_second_part = df_combined_br_nz_cases.loc[(df_combined_br_nz_cases['data'] >= start_date_second_part) & (df_combined_br_nz_cases['data'] <= end_date_second_part)].copy()

# =====================================================================


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], meta_tags=[{"name": "viewport", "content": "width=device-width"}])


fig = px.choropleth_mapbox(df_states_, locations="estado",
    geojson=brazil_states, center={"lat": -16.95, "lon": -47.78},
    zoom=4, color="casosNovos", color_continuous_scale="Redor", opacity=0.4,
    hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": True}
    )
fig.update_layout(
                # mapbox_accesstoken=token,
                paper_bgcolor='rgba(0,0,0,0)',
                mapbox_style="carto-darkmatter",
                autosize=True,
                margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                showlegend=False,)
df_data = df_states[df_states["estado"] == "RO"]


fig2 = go.Figure(layout={"template": "plotly_white"})
fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))
fig2.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#1f2c56',
    autosize=True,
    margin=dict(l=10, r=10, b=10, t=10),
    )


# =====================================================================
# Layout 
app.layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Row([
                    html.Div([
                    #     html.Img(id="logo", src=app.get_asset_url("g3-2.png"), height=130),
                        html.H3("COVID-19 - Análise do Impacto no Brasil",
                            id='title1',
                            style={'color': 'white'}
                        ),
                        dcc.Dropdown(
                            id='country-dropdown',
                            options=[
                                {'label': 'Brasil', 'value': 'Brasil'},
                                {'label': 'Nova Zelândia', 'value': 'Nova Zelândia'}
                            ],
                            value=['Brasil', 'Nova Zelândia'],
                            multi=True

                        ),
                        # dbc.Button("BRASIL", color="primary", id="location-button", size="lg")
                    ], style={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'wrap', 'align-items': 'center', 'justify-content': 'space-around', 'margin-bottom': '25px'}),

                    html.P("Informe a data na qual deseja obter informações:", style={"margin-top": "40px"}),
                    html.Div(
                            className="div-for-dropdown",
                            id="div-test",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=df_states.groupby("estado")["data"].min().max(),
                                    max_date_allowed=df_states.groupby("estado")["data"].max().min(),
                                    initial_visible_month=df_states.groupby("estado")["data"].min().max(),
                                    date=df_states.groupby("estado")["data"].max().min(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid #1f2c56", "background-color":'#192444'},
                                )
                            ],
                        ),
                    
                    dbc.Row([
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Casos Recuperados", className="card-text"),
                                    html.H4(style={"color": "#adfc92"}, id="casos-recuperados-text"),
                                    html.Span("Em Acompanhamento", className="card-text"),
                                    html.H5(id="em-acompanhamento-text"),
                                    ])
                                ], className='create_container', color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)", "color": "#FFFFFF"})], md=4),
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Casos Totais", className="card-text"),
                                    html.H4(style={"color": "#389fd6"}, id="casos-confirmados-text"),
                                    html.Span("Novos Casos na Data", className="card-text"),
                                    html.H5(id="novos-casos-text"),
                                    ])
                                ], className='create_container', color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF"})], md=4),
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Óbitos Confirmados", className="card-text"),
                                    html.H4(style={"color": "#DF2935"}, id="obitos-text"),
                                    html.Span("Óbitos na Data", className="card-text"),
                                    html.H5(id="obitos-na-data-text"),
                                    ])
                                ], className='create_container', color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF"})], md=4),
                    ],style={
                        'display': 'flex',
                        'flex-direction': 'row',
                        'flex-wrap': 'wrap',
                        'align-items': 'center',
                        'justify-content': 'space-between',
                        'margin-bottom': '25px'
                    }),
                    html.Div([
                        html.Div([
                            dcc.Graph(
                                id='first_part_lockdown_death_graph',
                                config={'displayModeBar': 'hover'},
                                style={'height': '250px'}
                                )],
                                className='create_container2 four columns',
                                style={'height': '250px'}),

                        html.Div([
                            dcc.Graph(
                                id='second_part_lockdown_death_graph',
                                config={'displayModeBar': 'hover'},
                                style={'height': '250px'})],
                                className='create_container2 four columns',
                                style={'height': '250px'}),

                        html.Div([
                            dcc.Graph(
                                id='first_part_lockdown_cases_graph',
                                config={'displayModeBar': 'hover'},
                                style={'height': '250px'})],
                                className='create_container2 four columns',
                                style={'height': '250px'}),

                        html.Div([
                            dcc.Graph(
                                id='second_part_lockdown_cases_graph',
                                config={'displayModeBar': 'hover'},
                                style={'height': '250px'})],
                                className='create_container2 four columns',
                                style={'height': '250px'})], className="nada",
                                style={"display": "flex", "flex-direction": "row"}),
                                ], id="mainContainer", className="nada", style={"display": "flex", "flex-direction": "column"}),
            html.Div(
                [
                    html.Div([
                        html.P("Dados Após Campanha de Vacinação Contra o COVID-19", style={"margin-top": "25px"}),
                        dcc.Dropdown(
                                        id="location-dropdown",
                                        options=[{"label": j, "value": i}
                                            for i, j in select_columns.items()
                                        ],
                                        value="obitosNovos",
                                        style={"margin-top": "10px"}
                                    ),
                        dcc.Graph(id="line-graph", figure=fig2, style={
                            "background-color": "#1f2c56", 'height': '400px', "margin-top": "10px"
                            }),
                        ], id="teste", style={'margin-right': '10px'}),
                    dbc.Col([
                        dcc.Loading(
                            id="loading-1",
                            type="default",
                            children=[dcc.Graph(id="choropleth-map", figure=fig, style={'height': '400px','margin-right': '10px', 'width': '400px', "margin-top": "100px"})],
                        )], )
                ], style={
                        "padding": "15px",
                        "background-color": "#192444", 'display': 'flex', 'flex-direction': 'row',
                        'flex-wrap': 'wrap', 'align-items': 'center', 'justify-content': 'space-around',
                        'margin-bottom': '25px', 'width': '80%'}),

                ]),
             ], fluid=True,)


# =====================================================================
# Interactivity
@app.callback(
    [
        Output("casos-recuperados-text", "children"),
        Output("em-acompanhamento-text", "children"),
        Output("casos-confirmados-text", "children"),
        Output("novos-casos-text", "children"),
        Output("obitos-text", "children"),
        Output("obitos-na-data-text", "children"),
    ], [Input("date-picker", "date"), Input("country-dropdown", "children")]
)
def display_status(date, location):
    # print(location, date)
    if location == "BRASIL":
        df_data_on_date = df_brasil[df_brasil["data"] == date]
    else:
        df_data_on_date = df_states[(df_states["estado"] == location) & (df_states["data"] == date)]

    recuperados_novos = "-" if df_data_on_date["Recuperadosnovos"].isna().values[0] else f'{int(df_data_on_date["Recuperadosnovos"].values[0]):,}'.replace(",", ".") 
    acompanhamentos_novos = "-" if df_data_on_date["emAcompanhamentoNovos"].isna().values[0]  else f'{int(df_data_on_date["emAcompanhamentoNovos"].values[0]):,}'.replace(",", ".") 
    casos_acumulados = "-" if df_data_on_date["casosAcumulado"].isna().values[0]  else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(",", ".") 
    casos_novos = "-" if df_data_on_date["casosNovos"].isna().values[0]  else f'{int(df_data_on_date["casosNovos"].values[0]):,}'.replace(",", ".") 
    obitos_acumulado = "-" if df_data_on_date["obitosAcumulado"].isna().values[0]  else f'{int(df_data_on_date["obitosAcumulado"].values[0]):,}'.replace(",", ".") 
    obitos_novos = "-" if df_data_on_date["obitosNovos"].isna().values[0]  else f'{int(df_data_on_date["obitosNovos"].values[0]):,}'.replace(",", ".") 
    return (
            recuperados_novos, 
            acompanhamentos_novos, 
            casos_acumulados, 
            casos_novos, 
            obitos_acumulado, 
            obitos_novos,
            )


@app.callback(
        Output("line-graph", "figure"),
        [Input("location-dropdown", "value"), Input("country-dropdown", "children")]
)
def plot_line_graph(plot_type, location):
    if location == "BRASIL":
        df_data_on_location = df_brasil.copy()
    else:
        df_data_on_location = df_states[(df_states["estado"] == location)]
    fig2 = go.Figure(layout={"template": "plotly_white"})
    bar_plots = ["casosNovos", "obitosNovos"]

    if plot_type in bar_plots:
        fig2.add_trace(go.Bar(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    else:
        fig2.add_trace(go.Scatter(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    
    fig2.update_layout(
        yaxis=dict(title='Números do COVID-19', color='orange'),
        hovermode='closest',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#1f2c56",
        autosize=True,
        xaxis=dict(
            visible=True,
            color='orange',
            showline=True,
            showticklabels=True,
            linecolor='orange',
            linewidth=0.5,
            ticks='outside',
            tickfont=dict(family='Arial', size=12, color='orange')),
        margin=dict(l=10, r=10, b=10, t=10),
        )
    return fig2


@app.callback(
    Output("choropleth-map", "figure"), 
    [Input("date-picker", "date")]
)
def update_map(date):
    df_data_on_states = df_states[df_states["data"] == date]

    fig = px.choropleth_mapbox(df_data_on_states, locations="estado", geojson=brazil_states, 
        center={"lat": CENTER_LAT, "lon": CENTER_LON},  
        zoom=4, color="casosAcumulado", color_continuous_scale="Redor", opacity=0.55,
        hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": False}
        )

    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", mapbox_style="carto-darkmatter", autosize=True,
                    margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)
    return fig


@app.callback(
    Output("country-dropdown", "children"),
    [Input("choropleth-map", "clickData"), Input("country-dropdown", "n_clicks")]
)
def update_location(click_data, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != "country-dropdown.n_clicks":
        state = click_data["points"][0]["location"]
        return "{}".format(state)
    
    else:
        return "BRASIL"

#======================================================LAURA PARTE=============================================#
#gráfico da primeira parte do lockdown - MORTES
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


if __name__ == "__main__":
    app.run_server(debug=False, port=8051)

