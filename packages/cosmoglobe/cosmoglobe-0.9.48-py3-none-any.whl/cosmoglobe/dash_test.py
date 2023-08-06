from cosmoglobe.plot.plottools import standalone_colorbar, seds_from_model
from cosmoglobe.plot import plot, gnom, trace, spec
from cosmoglobe.h5.chain import Chain
from cosmoglobe import get_test_chain
from astropy import constants as const
import numpy as np
import healpy as hp
import astropy.units as u
import matplotlib.pyplot as plt
import os
from pathlib import Path
import data as data_dir

paperfigs = "/Users/svalheim/work/BP/papers/09_leakage/figs/"
path = "/Users/svalheim/work/cosmoglobe-workdir/"
# chain='bla.h5'
dust = "dust_c0001_k000200.fits"


import dash
from dash import html, dcc
import pandas as pd

data = pd.read_csv("/Users/svalheim/projects/avocado.csv")
data = data.query("type == 'conventional' and region == 'Albany'")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

app = dash.Dash(__name__)

HEADER_STYLE = {
    "backgroundColor": "#222222",
    "height": "256px",
    "display": "flex",
    "flexDirection": "column",
    "justifyContent": "center",
}
EMOJI_STYLE = {"fontSize": "48px", "margin": "0 auto", "textAlign": "center"}
TITLE_STYLE = {
    "fontSize": "48px",
    "color": " #FFFFFF",
    "font-weight": "bold",
    "textAlign": "center",
    "margin": "0 auto",
}
DESC_STYLE = {
    "color": "#CFCFCF",
    "margin": "4px auto",
    "textAlign": "center",
    "maxWidth": "384px",
}
WRAPPER_STYLE = {
    "marginRight": "auto",
    "marginLeft": "auto",
    "maxWidth": "1024px",
    "paddingRight": "10px",
    "paddingLeft": "10px",
    "marginTop": "32px",
}
CARD_STYLE = {
    "marginBottom": "24px",
    "boxShadow": "0 4px 6px 0 rgba(0, 0, 0, 0.18)",
    "maxWidth": "1000px",
    "justifyContent": "center",
}
BODY_STYLE = {
    "fontFamily": "Lato, sans-serif",
    "margin": 0,
    "backgroundColor": "#F7F7F7",
}

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🥑", style=EMOJI_STYLE),
                html.H1(
                    children="Avocado Analytics",
                    style=TITLE_STYLE,
                ),
                html.P(
                    children="Analyze the behavior of avocado prices"
                    " and the number of avocados sold in the US"
                    " between 2015 and 2018",
                    style=DESC_STYLE,
                ),
            ],
            style=HEADER_STYLE,
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data["Date"],
                                    "y": data["AveragePrice"],
                                    "type": "lines",
                                    "hovertemplate": "$%{y:.2f}" "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Average Price of Avocados",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {
                                    "tickprefix": "$",
                                    "fixedrange": True,
                                },
                                "colorway": ["#17B897"],
                            },
                        },
                    ),
                    style=CARD_STYLE,
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data["Date"],
                                    "y": data["Total Volume"],
                                    "type": "lines",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Avocados Sold",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {"fixedrange": True},
                                "colorway": ["#E12D39"],
                            },
                        },
                    ),
                    style=CARD_STYLE,
                ),
            ],
            style=WRAPPER_STYLE,
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children="Region",
                            style={
                                "marginBottom": "6px",
                                "fontWeight": "bold",
                                "color": "#079A82",
                            },
                        ),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in np.sort(data.region.unique())
                            ],
                            value="Albany",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Type",
                            style={
                                "marginBottom": "6px",
                                "fontWeight": "bold",
                                "color": "#079A82",
                            },
                        ),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {"label": avocado_type, "value": avocado_type}
                                for avocado_type in data.type.unique()
                            ],
                            value="organic",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            style={
                                "marginBottom": "6px",
                                "fontWeight": "bold",
                                "color": "#079A82",
                            },
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
            ],
            style={
                "height": "112px",
                "width": "912px",
                "display": "flex",
                "justifyContent": "spaceEvenly",
                "paddingTop": "24px",
                "margin": "-80px auto 0 auto",
                "backgroundColor": "#FFFFFF",
                "boxShadow": "0 4px 6px 0 rgba(0, 0, 0, 0.18)",
            },
        ),
    ],
    style=BODY_STYLE,
)

if __name__ == "__main__":
    app.run_server(debug=True)

"""

.Select-control {
    width: 256px;
    height: 48px;
}

.Select--single > .Select-control .Select-value, .Select-placeholder {
    line-height: 48px;
}

.Select--multi .Select-value-label {
    line-height: 32px;
}

.menu-title {
    margin-bottom: 6px;
    font-weight: bold;
    color: #079A82;
}

"marginBottom": "6px",
    "fontWeight": "bold",
    "color": "#079A82",
"""
