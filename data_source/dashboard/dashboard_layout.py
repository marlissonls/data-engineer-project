import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from data_source.dashboard.data import df_states, select_columns, fig, fig2
from data_source.dashboard.data import df_vacinacao_obito
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Row([
                    html.Div([
                        #html.Img(id="logo", src=app.get_asset_url("g3-2.png"), height=130),
                        html.H1("COVID-19 - Análise do Impacto no Brasil",
                            id='title1',
                            style={'color': 'white'}
                        ),
                        dcc.Dropdown(
                            id='country-dropdown',
                            options=[
                                {'label': 'Brasil', 'value': 'Brasil'},
                                {'label': 'Nova Zelândia', 'value': 'Nova Zelândia'},
                                {'label': 'Araraquara', 'value': 'Araraquara'},
                                {'label': 'São Carlos', 'value': 'São Carlos'}
                            ],
                            value=['Brasil', 'Nova Zelândia', 'Araraquara', 'São Carlos'],
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
                                id='graph_lockdown_cases',
                                config={'displayModeBar': 'hover'},
                                style={'height': '250px'}
                                )],
                                className='create_container2 four columns',
                                style={'height': '250px'}),

                        html.Div([
                            dcc.Graph(
                                id='graph_lockdown_death',
                                config={'displayModeBar': 'hover'},
                                style={'height': '250px'})],
                                className='create_container2 four columns',
                                style={'height': '250px'}),

                        html.Div([
                            dcc.Graph(
                                id='graph_lockdown_cases_sc_ar',
                                config={'displayModeBar': 'hover'},
                                style={'height': '250px'})],
                                className='create_container2 four columns',
                                style={'height': '250px'}),

                        html.Div([
                            dcc.Graph(
                                id='graph_lockdown_death_sc_ar',
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
                            "background-color": "#1f2c56", 'height': '420px', "margin-top": "10px"
                            }),
                        ], id="teste", style={'margin-right': '15px'}),
                    html.Div([
                        dcc.Dropdown(
                            id='brasil-dropdown',
                            options=[
                                {'label': 'Brasil', 'value': 'Brasil'},
                            ],
                            value=['Brasil'],
                            style={"margin-top": "7px"},
                            multi=True
                        ),
                        dcc.Graph(id='graph_corr', style={"background-color": "#1f2c56", 'height': '420px', "margin-top": "8px", 'width': '420px'})], style={'height': '420px', 'margin-right': '15px'}),
                    dbc.Col([
                        dcc.Loading(
                            id="loading-1",
                            type="default",
                            children=[dcc.Graph(id="choropleth-map", figure=fig, style={'height': '420px', 'width': '420px', "margin-top": "102px"})],
                        )], )
                ], style={
                        "background-color": "#192444", 'display': 'flex', 'flex-direction': 'row',
                        'align-items': 'center', 'justify-content': 'center',
                        'margin-bottom': '25px', 'width': '90%', 'margin-left':'60px'}),

                ]),
             ], fluid=True,)

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
                y=df_country['br_obitos'],
                name=f'Novos Óbitos - {country}'
            )
        )
        traces.append(
            go.Scatter(
                x=df_country['data'],
                y=df_country['vacinas_acumulado'],
                name=f'Vacinações Totais - {country}',
                yaxis='y2'
            )
        )

    layout = go.Layout(
        title='Correlação - Óbitos Novos vs. Total de Vacinações',
        hovermode='closest',
        plot_bgcolor='#1f2c56',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            title='Novos Óbitos',
            linewidth=0.1,
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            linecolor='white'
        ),
        yaxis2=dict(
            title='Total de Vacinações',
            overlaying='y',
            side='right',
            linewidth=0.1,
            titlefont=dict(color='orange'),
            tickfont=dict(color='orange')
        ),
        xaxis=dict(
            visible=True,
            color='white',
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='white',
            linewidth=0.1,
            ticks='outside',
            tickfont=dict(family='Arial', size=12, color='white')),
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
