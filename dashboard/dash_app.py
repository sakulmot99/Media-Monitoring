from dash import Dash, html

def create_dash_app():
    app = Dash(__name__)
    app.layout = html.Div("Dashboard coming soon 🚧")
    return app
