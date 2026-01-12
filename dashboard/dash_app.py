import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pathlib import Path

# Load Config Parameters
from dashboard.dash_config import (
    COLOR_CODING,
    VIS_START_DATE,
    DF_ELECTION,
    FONT_FAMILY,
    TEXT_COLOR
)

# --- Config Objects Assigning ---
color_coding = COLOR_CODING
df_election = DF_ELECTION
vis_start_date = VIS_START_DATE

# Global text style for HTML elements
TEXT_STYLE = {"fontFamily": FONT_FAMILY, "color": TEXT_COLOR}

# --- Load dataset ---
BASE_DIR = Path(__file__).resolve().parent.parent
dataset_path = BASE_DIR / "datasets" / "PARTIES_ANALYSIS.csv"
df_party_analysis = pd.read_csv(dataset_path)

# --- Define analysis start date ---
df_party_analysis["week_start"] = pd.to_datetime(
    df_party_analysis["week_start"], format="%Y-%m-%d", errors="coerce"
)

df_party_analysis = df_party_analysis[
    df_party_analysis["week_start"] >= VIS_START_DATE
].reset_index(drop=True)

# After reading df_party_analysis
df_visibility = df_party_analysis.copy()
party_columns = [col.replace("_total", "") for col in df_visibility.columns if col.endswith("_total")]


def apply_font(fig):
    """Helper function to apply consistent font to Plotly figures."""
    fig.update_layout(
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
        title_font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
        legend_font=dict(
            family=FONT_FAMILY,
            color=TEXT_COLOR,
            size=14
        ),
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
            "Political Party Coverage in German Online News",
            style={**TEXT_STYLE, 'textAlign': 'center'}
        ),
        html.P(
            "The news we consume shapes what we think about and how we see the world. "
            "Coverage of political parties is no exception. When some parties dominate the headlines, "
            "this can influence public perception, opinions, and ultimately voting behavior. "
            "This dashboard tracks how often political parties appear in major German online news, helping you see media bias.",
            style={**TEXT_STYLE, 'lineHeight': '1.5', 'textAlign': 'center', 'margin': '20px 0'}
        ),

        # --- Total Mentions Section ---
        html.H3(
            "Total Political Party Mentions in German Media",
            style={**TEXT_STYLE, 'marginTop': '30px'}
        ),
        html.P(
            "Explore how often political parties have been mentioned in Germany’s major online newspapers since August 2025 "
            "(Der Spiegel, Die Zeit, Die FAZ, Süddeutsche Zeitung, and Die Bild). "
            "Use the controls to select which parties and publishers to include, and switch between viewing the Total Mentions by Party "
            "or the percentage Distribution of Mentions by Party. See at a glance which parties dominate the media conversation!",
            style={**TEXT_STYLE, 'lineHeight': '1.5'}
        ),
        html.Div([
            # Graph Selection
            html.Div([
                html.Label("Select Graph:", style=TEXT_STYLE),
                dcc.RadioItems(
                    id='graph-selector',
                    options=[
                        {'label': 'Total Mentions by Party', 'value': 'total'},
                        {'label': 'Percentage Distribution of Mentions', 'value': 'percentage'}
                    ],
                    value='total',
                    inline=True,
                    labelStyle={'margin-right': '15px'}
                )
            ], style={'display': 'flex', 'justifyContent': 'center', 'lineHeight': '1.5', 'margin-bottom': '15px'}),

            # Main Graph
            dcc.Graph(id='main-graph'),

            # Publishers & Parties Filters side-by-side
            html.Div([
                html.Div([
                    html.Label("Select Publishers:", style=TEXT_STYLE),
                    dcc.Checklist(
                        id='publisher-selector',
                        options=[{'label': pub, 'value': pub} for pub in df_visibility['publisher'].unique()],
                        value=df_visibility['publisher'].unique().tolist(),
                        inline=True,
                        labelStyle={'margin-right': '15px'}
                    )
                ], style={'flex': '1'}),

                html.Div([
                    html.Label("Select Parties:", style=TEXT_STYLE),
                    dcc.Checklist(
                        id='party-selector',
                        options=[{'label': p, 'value': p} for p in party_columns],
                        value=party_columns,
                        inline=True,
                        labelStyle={'margin-right': '15px'}
                    )
                ], style={'flex': '1'})
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'lineHeight': '1.5'})
        ], style={
            'border': '1px solid lightgrey',
            'padding': '20px',
            'borderRadius': '8px',
            'margin-bottom': '40px',
            'backgroundColor': '#f9f9f9'
        }),

        # --- Evolution Over Time Section ---
        html.H3("Evolution of Political Party Coverage in Online Media Over Time", style=TEXT_STYLE),
        html.P(
            "Track how media coverage of political parties has evolved over time. "
            "Choose whether to view absolute mentions or percentages, and filter by specific parties and publishers "
            "to see trends and shifts in the media conversation.",
            style={**TEXT_STYLE, 'lineHeight': '1.5'}
        ),
        html.Div([
            # Display Mode Selection
            html.Div([
                html.Label("Select Display Mode:", style=TEXT_STYLE),
                dcc.RadioItems(
                    id='display-mode',
                    options=[
                        {'label': 'Absolute counts', 'value': 'absolute'},
                        {'label': 'Percentages', 'value': 'percent'}
                    ],
                    value='percent',
                    inline=True,
                    labelStyle={'margin-right': '15px'}
                )
            ], style={'display': 'flex', 'justifyContent': 'center', 'margin-bottom': '15px'}),

            # Area Chart
            dcc.Graph(id='area-chart'),

            # Filters
            html.Div([
                html.Div([
                    html.Label("Select Publishers:", style=TEXT_STYLE),
                    dcc.Checklist(
                        id='area-publisher-selector',
                        options=[{'label': pub, 'value': pub} for pub in df_visibility['publisher'].unique()],
                        value=df_visibility['publisher'].unique().tolist(),
                        inline=True,
                        labelStyle={'margin-right': '15px'}
                    )
                ], style={'flex': '1'}),

                html.Div([
                    html.Label("Select Parties:", style=TEXT_STYLE),
                    dcc.Checklist(
                        id='area-party-selector',
                        options=[{'label': p, 'value': p} for p in party_columns],
                        value=party_columns,
                        inline=True,
                        labelStyle={'margin-right': '15px'}
                    )
                ], style={'flex': '1'})
            ], style={'display': 'flex', 'justifyContent': 'space-between'})
        ], style={
            'border': '1px solid lightgrey',
            'padding': '20px',
            'borderRadius': '8px',
            'margin-bottom': '40px',
            'backgroundColor': '#f9f9f9'
        })
    ])  # End of outer html.Div

    # --- Callbacks ---
    @app.callback(
        Output('main-graph', 'figure'),
        [Input('graph-selector', 'value'),
         Input('party-selector', 'value'),
         Input('publisher-selector', 'value')]
    )
    def update_main_graph(selected_graph, selected_parties, selected_publishers):
        if not selected_parties or not selected_publishers:
            return px.bar(title="Select at least one party and one publisher")

        df_filtered = df_visibility[df_visibility['publisher'].isin(selected_publishers)]
        filtered_totals = df_filtered[[f"{p}_total" for p in selected_parties]].sum()
        parties = filtered_totals.index.str.replace("_total", "")

        if selected_graph == 'total':
            df_totals = pd.DataFrame({'party': parties, 'total': filtered_totals.values})
            fig = px.bar(df_totals, x='party', y='total', color='party', color_discrete_map=color_coding,
                         labels={'party': 'Party', 'total': 'Total Mentions'}, title="Total Mentions by Party")
        else:
            sum_all = filtered_totals.sum()
            percentages = (filtered_totals / sum_all * 100) if sum_all > 0 else filtered_totals * 0
            df_media = pd.DataFrame({'party': parties, 'percentage': percentages.values, 'type': 'Media Mentions'})

            df_elec_filtered = df_election[df_election['party'].isin(selected_parties)]
            df_elec_filtered = df_elec_filtered.assign(
                percentage=df_elec_filtered['bundestag_share'] * 100,
                type='Election Results'
            )

            df_combined = pd.concat([df_media, df_elec_filtered[['party', 'percentage', 'type']]])

            fig = px.bar(df_combined, x='party', y='percentage', color='type', barmode='group',
                         color_discrete_map={'Media Mentions': '#636EFA', 'Election Results': '#EF553B'},
                         category_orders={'type': ['Media Mentions', 'Election Results']},
                         labels={'percentage': 'Percentage (%)', 'party': 'Party', 'type': 'Source'},
                         title="Comparison: Media Mentions vs. Election Results (%)")
            fig.update_layout(yaxis=dict(range=[0, 60]), legend_title_text="Source")

        return apply_font(fig)

    @app.callback(
        Output('area-chart', 'figure'),
        [Input('area-publisher-selector', 'value'),
         Input('display-mode', 'value'),
         Input('area-party-selector', 'value')]
    )
    def update_area_chart(selected_publishers, display_mode, selected_parties):
        if not selected_publishers or not selected_parties:
            return px.area(title="Select at least one party and one publisher")

        df_filtered = df_visibility[df_visibility['publisher'].isin(selected_publishers)]
        df_grouped = df_filtered.groupby('week_start')[[f"{p}_total" for p in selected_parties]].sum().reset_index()

        if display_mode == 'percent':
            df_grouped['total_mentions'] = df_grouped[[f"{p}_total" for p in selected_parties]].sum(axis=1)
            for p in selected_parties:
                df_grouped[f"{p}_share"] = (df_grouped[f"{p}_total"] / df_grouped['total_mentions']) * 100
            df_long = df_grouped.melt(
                id_vars='week_start',
                value_vars=[f"{p}_share" for p in selected_parties],
                var_name='party',
                value_name='value'
            )
            df_long['party'] = df_long['party'].str.replace('_share', '', regex=False)
            yaxis_label = "Share of Mentions (%)"
            y_range = [0, 100]
        else:
            df_long = df_grouped.melt(
                id_vars='week_start',
                value_vars=[f"{p}_total" for p in selected_parties],
                var_name='party',
                value_name='value'
            )
            df_long['party'] = df_long['party'].str.replace('_total', '', regex=False)
            yaxis_label = "Total Mentions"
            y_range = None

        fig = px.area(df_long, x='week_start', y='value', color='party', color_discrete_map=color_coding,
                      labels={'week_start': 'Week Start', 'value': yaxis_label, 'party': 'Party'},
                      title=f"Party Mentions Over Time ({'Percentages' if display_mode == 'percent' else 'Absolute'})")
        fig.update_layout(xaxis_title="Week Start", yaxis_title=yaxis_label,
                          legend_title="Party", yaxis=dict(range=y_range))

        return apply_font(fig)

    return app
