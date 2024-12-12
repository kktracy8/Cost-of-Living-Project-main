import json

import pandas as pd
import plotly.express as px
import requests


url = 'https://api.traveltimeapp.com/v4/time-filter'


def build_api_data(home_coords: tuple, dest_coords: dict[str:tuple]) -> dict:
    arrival_location_ids = ['Home']
    locations = [{
        "id": "Home",
        "coords": {
            "lat": home_coords[0],
            "lng": home_coords[1]
        }
    }]
    for zip, coord in dest_coords.items():
        arrival_location_ids.append(zip)
        locations.append({
            "id": zip,
            "coords": {
                "lat": coord[0],
                "lng": coord[1]
            }
        })

    data = {
        "locations": locations,
        "departure_searches": [
            {
                "id": "One-to-many Matrix",
                "departure_location_id": "Home",
                "arrival_location_ids": arrival_location_ids,
                "departure_time": "2021-09-21T08:00:00Z",
                "travel_time": 2*60*60,  # max travel time in sec
                "properties": [
                    "travel_time",
                    "distance"
                ],
                "transportation": {
                    "type": "driving"
                }
            }
        ]
    }
    return data


home = (34.02126979156505, -118.2135967031257)
destinations = {
    '91768': (34.05963311807834, -117.82023113265431),
    '92821': (33.91582607791368, -117.88628578156626),
}

data = build_api_data(home, destinations)
r = requests.request("POST", url, headers=headers, json=data)

# %%
city = 'Los Angeles, CA'

with open(f'database/geo_json_data/{city}.json') as f:
    geo_json = json.load(f)

# %%

df = geo_json['features']
destinations = {}
for row in df:
    zip_code = row['properties']['ZCTA5CE10']
    coord = row["geometry"]['coordinates'][0]
    while type(coord[0]) == list:
        coord = coord[0]
    destinations[zip_code] = (coord[1], coord[0])

data = build_api_data(home, destinations)
r = requests.request("POST", url, headers=headers, json=data)
r = json.loads(r.content)
# %%
df = []
for location in r['results'][0]['locations']:
    df.append(pd.Series({
        'Zip Code': location['id'],
        'distance': location['properties'][0]['distance'] * 0.000621371, # convert meters to miles
        'time': int(location['properties'][0]['travel_time']/60) # convert seconds to minues
    }))

df = pd.concat(df, axis=1).T
df['time'] = df['time'].astype(int)
#%%
value = 'time'

mapbox_center = {"lat": 34.0549, "lon": -118.2426}
fig = px.choropleth_mapbox(df, geojson=geo_json, locations='Zip Code', color=value,
                           color_continuous_scale="Viridis",
                           range_color=(0, 60),
                           # color_continuous_scale="Reds",
                           # range_color=(0, df['time'].max()),
                           featureidkey="properties.ZCTA5CE10",
                           mapbox_style="open-street-map",
                           opacity=0.5,
                           )

fig.update_layout(mapbox_zoom=7, mapbox_center=mapbox_center)

fig.show()

#%%