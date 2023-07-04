import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dashboard.data import df_states, select_columns, fig, fig2

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Row([
                    html.Div([
                        #html.Img(id="logo", src=app.get_asset_url("g3-2.png"), height=130),
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