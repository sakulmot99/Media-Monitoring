import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pathlib import Path

# Load Config Parameters
from dashboard.dash_config import (
    COLOR_CODING,
    VIS_START_DATE_TALKS,
    VIS_START_DATE_ONLINE,
    DF_ELECTION,
    FONT_FAMILY,
    TEXT_COLOR,
    TIME_AGGREGATION,
    TEXT_CONFIG
)

# --- Config Objects Assigning ---
color_coding = COLOR_CODING
df_election = DF_ELECTION
vis_start_date_online = VIS_START_DATE_ONLINE
vis_start_date_talks = VIS_START_DATE_TALKS

# Global text style for HTML elements
TEXT_STYLE = {"fontFamily": FONT_FAMILY, "color": TEXT_COLOR}

# --- Load datasets (parent.parent preserved) ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "datasets"

df_online_news = pd.read_csv(DATASETS_DIR / "PARTIES_ANALYSIS.csv")
df_talkshows = pd.read_csv(DATASETS_DIR / "TALKSHOW_PARTY_ANALYSIS.csv")


def prepare_df(df: pd.DataFrame, start_date: pd.Timestamp) -> pd.DataFrame:
    df = df.copy()
    df["week_start"] = pd.to_datetime(df["week_start"], errors="coerce")
    df = df[df["week_start"] >= start_date].reset_index(drop=True)
    return df

df_online_news = prepare_df(df_online_news, vis_start_date_online)
df_talkshows = prepare_df(df_talkshows, vis_start_date_talks)

# Use online news as default (matches current behavior)
df_visibility = df_talkshows

party_columns = [
    col.replace("_total", "")
    for col in df_visibility.columns
    if col.endswith("_total")
]


def get_active_df(dataset_key: str) -> pd.DataFrame:
    if dataset_key == "talkshows":
        return df_talkshows
    return df_online_news


def apply_font(fig):
    fig.update_layout(
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
        title_font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
        legend_font=dict(family=FONT_FAMILY, color=TEXT_COLOR, size=14),
        xaxis_title_font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
        yaxis_title_font=dict(family=FONT_FAMILY, color=TEXT_COLOR)
    )
    return fig


def create_dash_app():
    app = Dash(__name__)

    # --- Layout ---
    app.layout = html.Div([

        # --- Header ---
        html.H1(
            "Political Party Coverage in German Media",
            style={**TEXT_STYLE, 'textAlign': 'center'}
        ),
        html.P(
            "The news we consume shapes how we think about politics and how we see the world. "
            "Coverage of political parties is no exception: when some parties dominate the headlines, "
            "this can influence public attention, perceptions, and ultimately voting behavior. "
            "This dashboard tracks how often political parties appear in German media, helping to make patterns of media visibility more transparent. ",
            style={**TEXT_STYLE, 'lineHeight': '1.5', 'textAlign': 'center', 'margin': '20px 0'}
        ),

        html.P(
            "Note: This dashboard is a work in progress. It currently includes online news coverage "
            "(since January 2026) and political talk shows (from 2017 to 2025). We are continuously expanding "
            "the project by adding more time periods, additional media outlets, and—looking ahead—social media coverage.",
            style={
                **TEXT_STYLE,
                'fontStyle': 'italic',
                'textAlign': 'center',
                'margin': '0 0 20px 0'
            }
        ),

        # --- Dataset selector (highlighted) ---
        html.Div(
            [
                html.Label(
                    "Select Type of Media:",
                    style={**TEXT_STYLE, "fontWeight": "bold", "fontSize": "16px"}
                ),
                dcc.RadioItems(
                    id="dataset-selector",
                    options=[
                        {"label": "Online News", "value": "news"},
                        {"label": "Talkshows", "value": "talkshows"}
                    ],
                    value="news",
                    inline=True,
                    inputStyle={"margin-right": "8px"},  # spacing between radio button and label
                    labelStyle={"margin-right": "15px"}  # spacing between options
                ),
            ],
            style={
                "textAlign": "center",
                "marginBottom": "30px",
                "padding": "15px 20px",
                "borderRadius": "12px",
                "backgroundColor": "#f3e6ff",  # soft purple
                "border": "2px solid #b19cd9",  # slightly darker border
                "display": "inline-block",  # makes the box fit content neatly
            },
        ),


        # --- Total Mentions Section ---
        html.Div([
            # Outer purple box
            html.Div([
                html.H3(id="total-title", style={**TEXT_STYLE, 'marginTop': '0'}),
                html.P(id="total-description", style={**TEXT_STYLE, 'lineHeight': '1.5'}),

                # Inner grey box
                html.Div([
                    html.Div([
                        html.Label("Select Graph:", style=TEXT_STYLE),
                        dcc.RadioItems(
                            id='graph-selector',
                            options=[
                                {'label': 'Total Mentions by Party', 'value': 'total'},
                                {'label': 'Percentage Distribution of Mentions', 'value': 'percentage'}
                            ],
                            value='total',
                            inline=True
                        )
                    ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '15px'}),

                    dcc.Graph(id='main-graph'),

                    html.Div([
                        html.Div([
                            html.Label("Select Publishers:", style=TEXT_STYLE),
                            dcc.Checklist(id='publisher-selector', inline=True)
                        ], style={'flex': '1'}),

                        html.Div([
                            html.Label("Select Parties:", style=TEXT_STYLE),
                            dcc.Checklist(
                                id='party-selector',
                                options=[{'label': p, 'value': p} for p in party_columns],
                                value=party_columns,
                                inline=True
                            )
                        ], style={'flex': '1'})
                    ], style={'display': 'flex', 'justifyContent': 'space-between'})
                ], style={
                    'border': '1px solid lightgrey',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'marginBottom': '40px',
                    'backgroundColor': '#f9f9f9'
                })

            ], style={
                'border': '2px solid purple',
                'padding': '20px',
                'borderRadius': '8px',
                'marginBottom': '40px'
            })
        ]),

        # --- Evolution Over Time Section ---
        html.Div([
            # Outer purple box
            html.Div([
                html.H3(id="evolution-title", style=TEXT_STYLE),
                html.P(id="evolution-description", style={**TEXT_STYLE, 'lineHeight': '1.5'}),

                # Inner grey box
                html.Div([
                    html.Div([
                        html.Label("Select Display Mode:", style=TEXT_STYLE),
                        dcc.RadioItems(
                            id='display-mode',
                            options=[
                                {'label': 'Absolute counts', 'value': 'absolute'},
                                {'label': 'Percentages', 'value': 'percent'}
                            ],
                            value='percent',
                            inline=True
                        )
                    ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '15px'}),

                    dcc.Graph(id='area-chart'),

                    html.Div([
                        html.Div([
                            html.Label("Select Publishers:", style=TEXT_STYLE),
                            dcc.Checklist(id='area-publisher-selector', inline=True)
                        ], style={'flex': '1'}),

                        html.Div([
                            html.Label("Select Parties:", style=TEXT_STYLE),
                            dcc.Checklist(
                                id='area-party-selector',
                                options=[{'label': p, 'value': p} for p in party_columns],
                                value=party_columns,
                                inline=True
                            )
                        ], style={'flex': '1'})
                    ], style={'display': 'flex', 'justifyContent': 'space-between'})
                ], style={
                    'border': '1px solid lightgrey',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'backgroundColor': '#f9f9f9'
                })

            ], style={
                'border': '2px solid purple',
                'padding': '20px',
                'borderRadius': '8px',
                'marginBottom': '40px'
            })
        ])
    ])

    # --- Callbacks ---
    @app.callback(
        Output('publisher-selector', 'options'),
        Output('publisher-selector', 'value'),
        Output('area-publisher-selector', 'options'),
        Output('area-publisher-selector', 'value'),
        Input('dataset-selector', 'value')
    )
    def update_publishers(dataset_key):
        df = get_active_df(dataset_key)
        pubs = sorted(df['publisher'].unique())
        options = [{'label': p, 'value': p} for p in pubs]
        return options, pubs, options, pubs

    @app.callback(
        Output('main-graph', 'figure'),
        [
            Input('dataset-selector', 'value'),
            Input('graph-selector', 'value'),
            Input('party-selector', 'value'),
            Input('publisher-selector', 'value')
        ]
    )
    def update_main_graph(dataset_key, selected_graph, selected_parties, selected_publishers):

        if not selected_parties or not selected_publishers:
            return px.bar(title="Select at least one party and one publisher")

        df_visibility = get_active_df(dataset_key)
        df_filtered = df_visibility[df_visibility['publisher'].isin(selected_publishers)]

        filtered_totals = df_filtered[[f"{p}_total" for p in selected_parties]].sum()
        parties = filtered_totals.index.str.replace("_total", "")

        if selected_graph == 'total':
            df_totals = pd.DataFrame({'party': parties, 'total': filtered_totals.values})
            fig = px.bar(df_totals, x='party', y='total', color='party',
                         color_discrete_map=color_coding)
        else:
            percentages = filtered_totals / filtered_totals.sum() * 100
            df_media = pd.DataFrame({'party': parties, 'percentage': percentages.values, 'type': 'Media Mentions'})
            df_elec_filtered = df_election[df_election['party'].isin(selected_parties)].assign(
                percentage=lambda x: x['bundestag_share'] * 100,
                type='Election Results'
            )
            fig = px.bar(pd.concat([df_media, df_elec_filtered[['party', 'percentage', 'type']]]),
                         x='party', y='percentage', color='type', barmode='group')

        return apply_font(fig)

    @app.callback(
        Output('total-title', 'children'),
        Output('total-description', 'children'),
        Output('evolution-title', 'children'),
        Output('evolution-description', 'children'),
        Input('dataset-selector', 'value')
        )
    def update_graph_text(dataset_key):
        cfg = TEXT_CONFIG[dataset_key]
        return (
            cfg['total_title'],
            cfg['total_description'],
            cfg['evolution_title'],
            cfg['evolution_description']
        )

    
    @app.callback(
        Output('area-chart', 'figure'),
        [
            Input('dataset-selector', 'value'),
            Input('area-publisher-selector', 'value'),
            Input('display-mode', 'value'),
            Input('area-party-selector', 'value')
        ]
    )
    def update_area_chart(dataset_key, selected_publishers, display_mode, selected_parties):

        if not selected_publishers or not selected_parties:
            return px.area(title="Select at least one party and one publisher")

        df_visibility = get_active_df(dataset_key)
        df_filtered = df_visibility[df_visibility['publisher'].isin(selected_publishers)]
        # Getting aggregating config
        agg_cfg = TIME_AGGREGATION[dataset_key]
        # Resample according to dataset
        df_resampled = (
            df_filtered
                .set_index("week_start")
                .resample(agg_cfg["freq"])[[f"{p}_total" for p in selected_parties]]
                .sum()
                .reset_index()
        )

        df_grouped = df_resampled

        # Rolling averages as specified in config
        window = agg_cfg["rolling_window"]

        for p in selected_parties:
            col = f"{p}_total"
            df_grouped[col] = (
                df_grouped[col]
                .rolling(window=window, min_periods=1)
                .mean()
            )



        if display_mode == 'percent':
            df_grouped['total'] = df_grouped[[f"{p}_total" for p in selected_parties]].sum(axis=1)
            for p in selected_parties:
                df_grouped[p] = df_grouped[f"{p}_total"] / df_grouped['total'] * 100
            df_long = df_grouped.melt('week_start', selected_parties, 'party', 'value')
        else:
            df_long = df_grouped.melt('week_start', [f"{p}_total" for p in selected_parties], 'party', 'value')
            df_long['party'] = df_long['party'].str.replace('_total', '')

        fig = px.area(df_long, x='week_start', y='value', color='party',
                      color_discrete_map=color_coding)

        fig.update_xaxes(
                tickformat=agg_cfg["date_format"],
                title_text=agg_cfg["label"],
                showgrid=False
        )

        if dataset_key == "news":
            fig.update_xaxes(dtick="M1")  # one tick per month, weekly data


        return apply_font(fig)

    return app
