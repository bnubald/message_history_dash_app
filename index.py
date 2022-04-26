import sys
import waitress
from dash import dcc, html

from app import app, server
import layout
import callbacks

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Location(id="url_refresh", refresh=True),
        layout.layout,
    ]
)

if __name__ == "__main__":
    if "debug" in sys.argv:
        app.run_server(host="0.0.0.0", debug=True)
    else:
        waitress.serve(server, listen="0.0.0.0:8050")
