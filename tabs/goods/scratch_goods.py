import json

import numpy as np
import pandas as pd
import plotly.express as px

# import database.geo_json_data.zip_code_list as zc
from database.database import DB

# city = 'Los Angeles, CA'
# city = 'Las Vegas, NV'
value_options = ['regular', 'midgrade', 'premium', 'diesel']

#%%

# filter geojson for only relevant zip codes
# with open(f'database/geo_json_data/{city}.json') as f:
# # with open(f'database/geo_json_data/Los Angeles, CA.json') as f:
#     geo_json = json.load(f)


# zip_codes = zc.zip_codes_la
# features = [feature for feature in geo_json['features'] if feature['properties']['ZCTA5CE10'] in zip_codes]
# geo_json["features"] = features
#
# with open(f'database/geo_json_data/{city}.json', "w") as outfile:
#     outfile.write(json.dumps(geo_json))

def create_city_map_goods(city, db):
    df1 = db.gas_rates()
    with open(f'database/geo_json_data/{city}.json') as f:
        geo_json = json.load(f)

    match city:
        case 'Los Angeles, CA':
            zip_codes = zc.zip_codes_la

    # filter geojson for only relevant zip codes
    # features_la = [feature for feature in zip_codes['features'] if feature['properties']['ZCTA5CE10'] in zip_codes_la]
    # zip_codes['features'] = features_la\

    # ramdom dummy data:
    values = df1['regular']
    df = pd.DataFrame(index=zip_codes, columns=['value'], data=values)

    fig = px.choropleth_mapbox(df, geojson=geo_json, locations=df.index, color='value',
                               color_continuous_scale="Reds",
                               range_color=(0, 1),
                               featureidkey="properties.ZCTA5CE10",
                               mapbox_style="open-street-map",
                               )

    fig.update_layout(mapbox_zoom=7, mapbox_center={"lat": 34.0549, "lon": -118.2426})
    # fig.update_geos(fitbounds="locations", visible=True)
    # fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # fig.show()

    return fig

