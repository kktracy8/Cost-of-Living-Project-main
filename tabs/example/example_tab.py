import pandas as pd
import plotly.express as px
from dash import html, Output, Input, dcc, Dash, State
from dash.exceptions import PreventUpdate


# this is the dash tutorial app as a demo
# https://dash.plotly.com/minimal-app
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')


def render_layout_example():
    return html.Div(
        [
            dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
            dcc.Graph(id='graph-content')
        ]
    )


def register_example_callbacks(app: Dash):
    @app.callback(
        Output('graph-content', 'figure'),
        Input('tabs', 'value'),
        Input('dropdown-selection', 'value'),
    )
    def update_graph(tab, value):
        # print(tab)
        if tab != 'tab-example':
            PreventUpdate()
        dff = df[df.country == value]
        return px.line(dff, x='year', y='pop')
