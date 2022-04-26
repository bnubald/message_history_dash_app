import dash
import plotly.express as px
import pandas as pd
from dash import Input, State, Output, callback
from dash_bootstrap_templates import ThemeSwitchAIO
from dash.exceptions import PreventUpdate
import sql
from app import app
from layout import theme_light, theme_dark
from functions import countMessages


@app.callback(
    Output("memory-dataframe", "data"),
    Output("main-container", "children"),
    Input("button-login", "n_clicks"),
    State("input-username", "value"),
    State("input-password", "value"),
    prevent_initial_call=False,
)
def store_data(login, username, password):
    if (username != None) and (password != None):
        sqlConn = sql.SQLConnect(username, password)
        df = sqlConn.loadData()

        dump = df.to_dict("records")
        return dump, dash.no_update
    else:
        raise PreventUpdate


@callback(
    Output("datatable-interactivity", "data"),
    Output("datatable-interactivity", "columns"),
    Output("graph", "figure"),
    Output("datepicker", "value"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
    Input("datatable-interactivity", "derived_virtual_data"),
    Input("datatable-interactivity", "derived_virtual_selected_rows"),
    Input("datepicker", "value"),
    Input("memory-dataframe", "data"),
    prevent_initial_call=False,
)
def update_table(toggle, rows, derived_virtual_selected_rows, dates, data):
    template = theme_light if toggle else theme_dark
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    df = pd.DataFrame(data)
    if not len(df) > 0:
        raise PreventUpdate
    df["message_timestamp"] = pd.to_datetime(df["message_timestamp"], errors="coerce")

    df_count = countMessages(
        df, group="category", date_col="message_timestamp", period="day"
    )

    if dates is not None:
        dates[0] = pd.to_datetime(dates[0])
        dates[1] = pd.to_datetime(dates[1])

        df_timestamp = pd.to_datetime(df_count["message_timestamp"])
        df_count = df_count[(df_timestamp >= dates[0]) & (df_timestamp <= dates[1])]

    dateRange = dash.no_update
    if dates is None:
        df_timestamp = pd.to_datetime(df_count["message_timestamp"])
        if len(df_timestamp) > 0:
            dateRange = [min(df_timestamp), max(df_timestamp)]

    data = df_count.to_dict("records")
    columns = [{"name": i, "id": i} for i in df_count.columns]

    if (rows is not None) and (rows != []):
        fig = px.line(
            pd.DataFrame(rows),
            x="message_timestamp",
            y="counts",
            color="category",
            template=template,
            # markers=True,
            # line_shape='spline',
            labels={
                "month": "Day",
                "counts": "Counts",
            },
        )
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(
            {
                # "title": 'Message history count ',
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "Total Messages"},
                "showlegend": True,
                "margin": dict(l=5, r=5, t=5, b=5),
            }
        )
    else:
        fig = {}

    return data, columns, fig, dateRange
