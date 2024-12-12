from io import StringIO

import pandas as pd
from dash import html, Output, Input, dcc, Dash, State
from dash.exceptions import PreventUpdate

from tabs.commute.commute_api import get_commute_cost
from tabs.summary.create_city_map import create_city_map
from tabs.summary.input_layout_utils import form_input, generate_card_card

options = ['Annual Commute Cost', 'Annual Fuel Cost', 'Annual Commute Time Cost', 'Time (min)',
           'Distance (miles)']


def render_layout_commute():
    layout = generate_card_card(
        'City Map', 'far fa-map',
        html.Div(
            className='p-4',
            style={'height': 1000},
            children=[
                dcc.Store(id='df_commute'),
                html.H5(
                    'Note: the default workplace coordinates are the city center. Please input your actual workplace location.'),
                html.Hr(),
                html.Div(
                    form_input("Graphed Value", options[0], options=options),
                    className='w-50  mx-auto',
                ),
                html.Hr(),

                dcc.Loading(children=html.Div(id='commute_map'))
            ]
        ),
    )

    return layout


def register_commute_callbacks(app: Dash):
    @app.callback(
        Output('df_commute', 'data'),
        Input('tabs', 'value'),
        State('location', 'value'),
        Input('workplace_longitude', 'value'),
        Input('workplace_latitude', 'value'),
        Input('fuel_cost', 'value'),
        Input('time_cost_($/hr)', 'value'),
        Input('vehicle_mpg', 'value'),
    )
    def update_graph(tab, city, long, lat, fuel_cost, time_cost, mpg):
        if tab != 'tab-commute':
            PreventUpdate()

        try:
            df, _ = get_commute_cost(city, (long, lat), mpg, fuel_cost, time_cost)
        except Exception:
            return None
        return df.to_json(date_format='iso', orient='split')

    @app.callback(
        Output('commute_map', 'children'),
        State('tabs', 'value'),
        State('location', 'value'),
        Input('df_commute', 'data'),
        Input('graphed_value', 'value'),
        State('workplace_longitude', 'value'),
        State('workplace_latitude', 'value'),
    )
    def update_commute_map(tab, city, json_df, value, long, lat):
        if tab != 'tab-commute':
            PreventUpdate()
        if not json_df:
            return html.H3('Error! One of the required inputs is missing or invalid', className='pt-5')

        df = pd.read_json(StringIO(json_df), orient='split')
        hover_format = {
            'Time (min)': '{:,.1f} min',
            'Distance (miles)': ':,.1f',
            'Annual Fuel Cost': '${:,.0f}',
            'Annual Commute Time Cost': ':,.0f',
            'Annual Commute Cost': ':,.0f',
        }

        hovertemplate = '''
<b>Zip Code: %{customdata[0]} </b><br><br>
Time: %{customdata[1]:,.1f} min<br>
Distance: %{customdata[2]:,.1f} miles<br>
<br>
Annual Fuel Cost: $ %{customdata[3]:,.0f}<br>
Annual Time Cost: $ %{customdata[4]:,.0f}<br>
<br>
Annual Total Cost: $ %{customdata[5]:,.0f}<br>
        '''
        custom_data = ['Zip Code', 'Time (min)', 'Distance (miles)', 'Annual Fuel Cost', 'Annual Commute Time Cost',
                       'Annual Commute Cost']
        fig = create_city_map(city, value, df, hovertemplate, custom_data=custom_data, height=800)

        return dcc.Graph(figure=fig, style={'height': 800})
