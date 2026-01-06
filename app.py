from dashboard.dash_app import create_dash_app

app = create_dash_app()
server = app.server  # Required for deployment
