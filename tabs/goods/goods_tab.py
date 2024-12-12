import pandas as pd
import json
import plotly.express as px
from dash.dash_table.Format import Format, Scheme
from dash import html, Output, Input, dcc, Dash, State
from dash.exceptions import PreventUpdate
from tabs.map_utils import get_mapbox_center
# import database.geo_json_data.zip_code_list as zc
from database.database import DB
from tabs.summary.input_layout_utils import generate_card_card

cities = [
    'Los Angeles, CA',
    'Dallas, TX',
    'Chicago, IL',
    'Boston, MA',
    'New York City, NY',
    'Denver, CO',
    'Las Vegas, NV',
]
gas = ['regular', 'midgrade', 'premium', 'diesel']

df = pd.DataFrame()
hover_format = {
    'regular': ':.0f',
    'midgrade': ':.0f',
    'premium': ':.0f',
    'diesel': ':.0f',
}
gas_options = list(hover_format.keys())
gas_status = ['regular', 'midgrade', 'premium', 'diesel']


def input_div(label, element):
    return html.Div(
        className='row p-1',
        children=[
            html.Label(label, id=f'label-{label}', className='col-5'),
            html.Div(element, className='col-7')
        ]
    )

def render_layout_goods():
    global df
    db = DB()
    df = db.gas_rates()

    graph_div = html.Div(
        className='r-1',
        children=[
            html.Div(
                dcc.Graph(id='gas-map', style={'height':'600px','width': '800px', 'transform': 'translate(30%, 0%)'}),
                className='col-8'
            ),
        ]
    )

    heatmap_div = html.Div(
        className='r-1',
        children=[
            html.Div(
                dcc.Graph(id='goods-bar-chart', style={'width': '700px', 'left': '70%', 'transform': 'translate(50%, 0%)'}),
                className='row py-2'
            ),
        ]
    )

    layout = html.Div(
        className='',
        children=[
            dcc.Store(id='df_goods', data=df.to_json(date_format='iso', orient='split')),
            generate_card_card('Fuel Price by Zip Code', 'fas fa-gas', graph_div),
            generate_card_card('Food Cost by City and Family Size', 'fa fa-heatmap', heatmap_div)
        ],
    )
    return layout

def register_goods_callbacks(app: Dash):

    db = DB()

    @app.callback(
        Output('gas-map', 'figure'),
        Output('goods-bar-chart', 'figure'),
        Input('run_callbacks', component_property='n_clicks'),
        State('tabs', 'value'),
        Input('location', 'value'),
        Input('fuel_type', 'value'),
        Input("family_size", "value")
    )
    def update_graph(_,tab, location, fuel_type, family_size):
        if tab != 'tab-goods':
            PreventUpdate()
            
        df1 = db.gas_rates()
        df2 = df1.loc[df1['city'] == location]
        
        geo_json = db.get_geo_json(location)
        mapbox_center = get_mapbox_center(location)
        if location == 'Boston, MA':
            df2['Zip code'] =  df2['Zip code'].astype(str).str.zfill(5)

        fig = px.choropleth_mapbox(df2, geojson=geo_json, locations='Zip code', color=df2[fuel_type],
                               color_continuous_scale="Turbo",
                               range_color=(min(df2[fuel_type]), max(df2[fuel_type])),
                               featureidkey="properties.ZCTA5CE10",
                               mapbox_style="carto-positron",
                               hover_data='Zip code',
                               title=f"Average {fuel_type} Price (USD) per Gallon by Zip Code"
                               )
        fig.update_layout(mapbox_zoom=8, mapbox_center=mapbox_center)
        df = db.food_rates()
        names = []
        a = []
        if isinstance(family_size, list):
            for x in family_size:
                a.append(df[x].tolist())
                names.append(x)
        else:
            a.append(df[family_size].tolist())
            names.append(family_size)
        fig2 = px.imshow(a, text_auto=True, labels=dict(x="City", y="Family Size", color="Monthly Cost", title=f"Food Cost (USD) by Family Size"),
                x=['Los Angeles, CA', 'Dallas, TX', 'Chicago, IL', 'Boston, MA', 'New York City, NY', 'Denver, CO', 'Las Vegas, NV'],
                y=names)
        return fig, fig2
