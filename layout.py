from dash import dcc, html
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash import dash_table
from datetime import datetime, timedelta
import login

# Define light and dark themes.
theme_light = "yeti"  # yeti, cosmo, lumen
theme_dark = "darkly"
url_theme_light = dbc.themes.YETI
url_theme_dark = dbc.themes.DARKLY
this_year = datetime.now().year

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            ThemeSwitchAIO(
                aio_id="theme",
                themes=[url_theme_light, url_theme_dark],
            ),
        )
    ],
    brand="Message History Stats",
    brand_href="#",
    color="primary",
    dark=True,
    style={"margin": "0px", "filter": "drop-shadow(0 0 0.25rem black)"},
)

card_filter = dbc.Row(
    [
        dbc.Col(
            [
                dmc.DateRangePicker(
                    id="datepicker",
                    maxDate=datetime.utcnow() - timedelta(days=1),
                    value=None,
                ),
            ],
            width=3,
        ),
        dbc.Col([], width=9),
    ],
    className="g-0",
    align="center",
    style={"marginBottom": "10px"},
)

card_graph = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(
                id="graph",
                style={"height": "100%"},
            ),
            dcc.Store(id="graphUpdate"),
        ],
        style={"height": "calc(100vh - 150px)"},
    ),
)

table = html.Div(
    [
        dash_table.DataTable(
            id="datatable-interactivity",
            filter_action="native",
            sort_action="native",
            sort_mode="single",
            page_action="none",
            style_filter_conditional=[
                {"if": {"column_id": "counts"}, "pointer-events": "None"}
            ],
        ),
        dcc.Store(id="tableUpdate"),
        dcc.Store(id="memory-dataframe", storage_type="memory"),
    ],
    id="table",
    style={"height": "inherit", "overflowY": "auto"},
)

card_table = dbc.Card(
    table,
    style={"height": "calc(100vh - 150px)"},
)

cards = dbc.CardBody(
    [
        card_filter,
        dbc.Row(
            [
                dbc.Col(card_graph, width=8),
                dbc.Col(card_table, width=4),
            ]
        ),
    ]
)

layout = dmc.LoadingOverlay(
    dbc.Container(
        [
            login.layout,
            dbc.Row(navbar),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            cards,
                        ],
                    )
                ],
            ),
        ],
        className="dbc",
        fluid=True,
        id="main-container",
        style={"height": "100vh"},
    ),
    overlayOpacity=0,
)
