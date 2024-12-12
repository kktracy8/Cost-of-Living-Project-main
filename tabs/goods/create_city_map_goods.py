import json

import numpy as np
import pandas as pd
import plotly.express as px

# import database.geo_json_data.zip_code_list as zc




# def create_city_map(city, value, df):
#     with open(f'database/geo_json_data/{city}.json') as f:
#         geo_json = json.load(f)
#
#
#     match city:
#         case 'Los Angeles, CA':
#             mapbox_center = {"lat": 34.0549, "lon": -118.2426}
#         case 'Las Vegas, NV':
#             mapbox_center = {"lat": 36.1716, "lon": -115.1391}
#         case 'Chicago, Il':
#             mapbox_center = {"lat": 41.8781, "lon": -87.6298}
#         case 'Dallas, TX':
#             mapbox_center = {"lat": 32.7767, "lon": -96.7970}
#         case 'Boston, MA':
#             mapbox_center = {"lat": 42.3601, "lon": -71.0589}
#         case 'New York City, NY':
#             mapbox_center = {"lat": 40.7128, "lon": -74.0060}
#         case 'Denver, CO':
#             mapbox_center = {"lat": 39.7392, "lon": -104.9903}
#         case _:
#             mapbox_center = {"lat": 34.0549, "lon": -118.2426}
#
#     fig = px.choropleth_mapbox(df, geojson=geo_json, locations='Zip Code', color=value,
#                                color_continuous_scale="Reds",
#                                range_color=(0, 1),
#                                featureidkey="properties.ZCTA5CE10",
#                                mapbox_style="open-street-map",
#                                )
#
#     fig.update_layout(mapbox_zoom=7, mapbox_center=mapbox_center)
#     # fig.show()
#
#     return fig
