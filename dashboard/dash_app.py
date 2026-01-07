# dashboard/dash_app.py
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pathlib import Path

# --- Load dataset ---
BASE_DIR = Path(__file__).resolve().parent.parent
dataset_path = BASE_DIR / "datasets" / "PARTIES_ANALYSIS.csv"
df_party_analysis = pd.read_csv(dataset_path)

# After reading df_party_analysis
df_visibility = df_party_analysis.copy()

# Example election dataframe — replace with real values if you have them
party_columns = [col.replace("_total", "") for col in df_visibility.columns if col.endswith("_total")]
df_election = pd.DataFrame({
    "party": party_columns,
    "bundestag_share": [0.25, 0.20, 0.15, 0.10, 0.15, 0.15]  # Replace with real election percentages
})



color_coding = {
    'CDU/CSU': 'black',
    'SPD': 'red',
    'Grüne': 'green',
    'FDP': 'yellow',
    'AfD': 'blue',
    'Die Linke': 'purple'
}

def create_dash_app():
    app = Dash(__name__)

    # --- Layout ---
    app.layout = html.Div([
        html.H1("Partisan Media Bias Dashboard", style={'textAlign': 'center'}),
        html.H3("Total Political Party Mentions in German Media"),
        html.P(
            "Explore how often political parties have been mentioned in Germany’s major online newspapers..."
        ),

        # --- Controls ---
        html.Div([
            html.Div([
                html.Label(html.B("Select Graph:")),
                dcc.RadioItems(
                    id='graph-selector',
                    options=[
                        {'label': 'Total Mentions by Party', 'value': 'total'},
                        {'label': 'Total Distribution of Mentions by Party (%)', 'value': 'percentage'}
                    ],
                    value='total',
                    inline=True
                ),
            ], style={'display': 'inline-block', 'verticalAlign': 'top'}),

            html.Div([
                html.Label(html.B("Select Publishers:")),
                dcc.Checklist(
                    id='publisher-selector',
                    options=[{'label': pub, 'value': pub} for pub in df_visibility['publisher'].unique()],
                    value=df_visibility['publisher'].unique().tolist(),
                    inline=True
                ),
            ], style={'display': 'inline-block', 'verticalAlign': 'top'}),

            html.Div([
                html.Label(html.B("Select Parties:")),
                dcc.Checklist(
                    id='party-selector',
                    options=[{'label': p, 'value': p} for p in party_columns],
                    value=party_columns,
                    inline=True
                ),
            ], style={'display': 'inline-block', 'verticalAlign': 'top'})
        ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}),

        dcc.Graph(id='main-graph'),

        # --- Area chart ---
        html.H3("Evolution of Political Party Coverage Over Time"),
        html.Div([
            html.Label(html.B("Select Display Mode:")),
            dcc.RadioItems(
                id='display-mode',
                options=[
                    {'label': 'Absolute counts', 'value': 'absolute'},
                    {'label': 'Percentages', 'value': 'percent'}
                ],
                value='percent',
                inline=True
            ),
            html.Label(html.B("Select Publishers:")),
            dcc.Checklist(
                id='area-publisher-selector',
                options=[{'label': pub, 'value': pub} for pub in df_visibility['publisher'].unique()],
                value=df_visibility['publisher'].unique().tolist(),
                inline=True
            ),
            html.Label(html.B("Select Parties:")),
            dcc.Checklist(
                id='area-party-selector',
                options=[{'label': p, 'value': p} for p in party_columns],
                value=party_columns,
                inline=True
            )
        ], style={'marginBottom': '20px'}),
        dcc.Graph(id='area-chart')
    ])

    # --- Callbacks ---

    @app.callback(
        Output('main-graph', 'figure'),
        [
            Input('graph-selector', 'value'),
            Input('party-selector', 'value'),
            Input('publisher-selector', 'value')
        ]
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
            fig.update_layout(template="plotly_white")
            return fig
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
            fig.update_layout(template="plotly_white", yaxis=dict(range=[0, 100]), legend_title_text="Source")
            return fig

    @app.callback(
        Output('area-chart', 'figure'),
        [
            Input('area-publisher-selector', 'value'),
            Input('display-mode', 'value'),
            Input('area-party-selector', 'value')
        ]
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
                          legend_title="Party", template="plotly_white", yaxis=dict(range=y_range))
        return fig

    return app
