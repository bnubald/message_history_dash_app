from flask import Flask
from dash import Dash
from layout import url_theme_light

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"
)

flask_server = Flask(__name__)
app = Dash(
    __name__,
    server=flask_server,
    suppress_callback_exceptions=True,
    external_stylesheets=[url_theme_light, dbc_css],
)

server = app.server
