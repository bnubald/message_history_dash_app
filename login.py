import dash
from dash.exceptions import PreventUpdate
from dash import dcc, html, Input, State, Output, callback
import dash_bootstrap_components as dbc

user_input = dbc.CardGroup(
    [
        dbc.Label("Username:", html_for="username"),
        dbc.Input(
            type="text",
            id="input-username",
            placeholder="Enter Username",
            debounce=True,
            autoFocus=True,
            style={
                "width": "100%",
            },
        ),
        dbc.FormFeedback(
            "Incorrect username",
            type="invalid",
        ),
    ]
)

pass_input = dbc.CardGroup(
    [
        dbc.Label("Password:", html_for="password"),
        dbc.Input(type="password", id="input-password", placeholder="Enter Password"),
        dbc.FormFeedback(
            "Incorrect password",
            type="invalid",
        ),
    ]
)

login_button = dbc.Button(
    "Log in",
    id="button-login",
    n_clicks=0,
    className="d-grid gap-2 col-6 mx-auto",
    style={"borderRadius": "25px", "margin": "10px"},
)

layout = html.Div(
    [
        dcc.Location(id="url_login", refresh=True),
        dbc.Modal(
            html.Main(
                [
                    html.H2("Log into SQL Server"),
                    html.Br(),
                    html.Div(
                        children=[
                            dbc.Card(
                                [
                                    dbc.CardGroup(
                                        [user_input, pass_input, login_button]
                                    ),
                                    dbc.CardFooter(
                                        [html.Center([html.Label("Welcome!")])],
                                        style={"backgroundColor": "transparent"},
                                    ),
                                ],
                                body=True,
                                style={
                                    "border": "1px solid rgb(0,28,100)",
                                    "borderRadius": "10px",
                                    "boxShadow": "0px 0px 30px 20px rgba(0,28,100,0.02)",
                                },
                            )
                        ],
                        style={
                            "position": "relative",
                            "width": "100%",
                            "maxWidth": "325px",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "flex": "0 0 100%",
                    "flexDirection": "column",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "padding": "48px 0px",
                    "marginTop": "10px",
                },
            ),
            id="modal-login",
            fullscreen=False,
            is_open=True,
            keyboard=False,
            backdrop="static",
            centered=True,
        ),
    ],
    id="login-screen",
)

import sql

# Callback for when login button is clicked
@callback(
    Output("modal-login", "is_open"),
    Output("input-username", "valid"),
    Output("input-username", "invalid"),
    Output("input-password", "valid"),
    Output("input-password", "invalid"),
    Input("button-login", "n_clicks"),
    Input("input-username", "n_submit"),
    Input("input-password", "n_submit"),
    State("input-username", "value"),
    State("input-password", "value"),
    prevent_initial_callback=False,
)
def login_check(n_clicks, s1, s2, username, password):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id != "":
        if password is None:
            return dash.no_update, True, False, False, True
        elif sql.SQLConnect(username, password).connectCheck() is not False:
            return False, True, False, True, False
        else:
            return dash.no_update, False, True, False, True
    else:
        raise PreventUpdate
