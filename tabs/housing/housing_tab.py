import plotly.express as px
from dash import html, Output, Input, dcc, Dash, State
from dash.exceptions import PreventUpdate

from database.database import DB
from tabs.housing.utils import (
    sale_prices_by_city,
    sale_prices_by_zipcode,
    rent_prices_by_city,
    rent_prices_by_zipcode
)
from tabs.map_utils import get_mapbox_center


def input_div(label, element):
    return html.Div(
        className='row p-1',
        children=[
            html.Label(label, id=f'label-{label}', className='col-5'),
            html.Div(element, className='col-7')
        ]
    )


def render_layout_housing():
    return html.Div(
        dcc.Loading(
            [
                html.Div(
                    className='row',
                    children=[

                        html.H4('Housing Cost'),
                        html.Div(
                            dcc.Graph(id='housing-map', style={'height': '600px', 'width': '700px'}, ),
                            className='container border my-2 mx-auto d-flex justify-content-center',
                        ),
                        html.Div(
                            dcc.Graph(id='housing-bar-chart', style={'width': '700px'}, ),
                            className='container border my-2 mx-auto d-flex justify-content-center',
                        )
                    ]
                ),
            ],
            style={'height': '700px'},
        )
    )


def register_housing_callbacks(app: Dash):
    @app.callback(
        Output('housing-map', 'figure'),
        Output('housing-bar-chart', 'figure'),
        Input('run_callbacks', component_property='n_clicks'),
        State('tabs', 'value'),
        Input('location', 'value'),
        Input('property_type', 'value'),
        Input('rent_or_buy', 'value'),
    )
    def update_graph(_, tab, location, property_type, rent_or_buy):
        if tab != 'tab-housing':
            PreventUpdate()
        print('Updating housing graph')

        mapbox_center = get_mapbox_center(location)
        loc_toks = location.split(",")
        city = loc_toks[0].strip()
        state = loc_toks[1].strip()

        db = DB()
        geo_json = db.get_geo_json(location)

        if rent_or_buy == "RENT":
            prices_by_zip_df = rent_prices_by_zipcode(property_type, city, state)
            prices_by_city_df = rent_prices_by_city()
        else:
            prices_by_zip_df = sale_prices_by_zipcode(property_type, city, state)
            # print(f"geo-json: {geo_json['features']}")
            prices_by_city_df = sale_prices_by_city()

        min_val_zip = prices_by_zip_df['mean_price'].min()
        max_val_zip = prices_by_zip_df['mean_price'].max()

        title_tag = "Monthly Rent" if rent_or_buy == "RENT" else "Sale"

        fig1 = px.choropleth_mapbox(
            prices_by_zip_df,
            geojson=geo_json,
            locations='zip_code',
            color='mean_price',
            color_continuous_scale='Turbo',
            range_color=(min_val_zip, max_val_zip),
            featureidkey="properties.ZCTA5CE10",
            mapbox_style="open-street-map",
            title=f"Mean {title_tag} Price (USD) by Zip Code"
        )

        fig1.update_layout(mapbox_zoom=9, mapbox_center=mapbox_center)

        fig2 = px.bar(prices_by_city_df,
                      x="mean_price",
                      y="location",
                      orientation='h',
                      height=400,
                      title=f'Mean {title_tag} Price (USD) for Property Type: {property_type}'
                      )
        return fig1, fig2
