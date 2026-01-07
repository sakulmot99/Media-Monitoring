import os
from dashboard.dash_app import app

# Gunicorn needs this
server = app.server

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8050)),
        debug=False
    )
