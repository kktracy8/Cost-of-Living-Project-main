import json

import pandas as pd
import plotly.express as px
import requests

from database.database import DB


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
                "travel_time": 2 * 60 * 60,  # max travel time in sec
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


def add_commute_cost(df, city: str, home: tuple[str, str], mpg, fuel_cost, time_cost):
    try:
        df_commute, _ = get_commute_cost(city, home, mpg, fuel_cost, time_cost)
        df_commute['Zip Code'] = df_commute['Zip Code'].astype(str)
        df = df.merge(df_commute, on='Zip Code', how='left')
    except Exception:
        df['Annual Fuel Cost'] = 0
        df['Annual Commute Time Cost'] = 0
        df['Distance (miles)'] = 0
        df['Time (min)'] = 0
        df['Annual Commute Cost'] = 0
    return df


def get_commute_cost(city: str, home: tuple[str, str], mpg, fuel_cost, time_cost):
    # city = 'Los Angeles, CA'
    # print(city, home, mpg, fuel_cost, time_cost)
    # with open(f'database/geo_json_data/{city}.json') as f:
    #     geo_json = json.load(f)
    db = DB()
    geo_json = db.get_geo_json(city)

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
    print(f'api status = {r.status_code}')
    if r.status_code != 200:
        print(r.content)
        print(r.reason)
    r = json.loads(r.content)

    df = []
    for location in r['results'][0]['locations']:
        df.append(pd.Series({
            'Zip Code': location['id'],
            'distance': float(location['properties'][0]['distance'] * 0.000621371),  # convert meters to miles
            'time': float(location['properties'][0]['travel_time'] / 60)  # convert seconds to minues
        }))

    df = pd.concat(df, axis=1).T

    df['Annual Fuel Cost'] = df['distance'] * fuel_cost / mpg * 2 * 251
    df['Annual Commute Time Cost'] = df['time'] / 60 * time_cost * 2 * 251  # 251 = working days
    df['Annual Commute Cost'] = df['Annual Fuel Cost'] + df['Annual Commute Time Cost']
    df['Annual Commute Time Cost'] = df['Annual Commute Time Cost'].astype(float)
    df['Annual Fuel Cost'] = df['Annual Fuel Cost'].astype(float)
    df['Annual Commute Cost'] = df['Annual Commute Cost'].astype(float)
    df['time'] = df['time'].astype(float)
    df['distance'] = df['distance'].astype(float)
    df = df.rename(columns={
        'time': 'Time (min)',
        'distance': 'Distance (miles)',
    })
    return df, geo_json


if __name__ == '__main__':
    df, geo_json = get_commute_cost('Los Angeles, CA', home, 25, 3.5, 25)
    value = 'Commute Cost'
    mapbox_center = {"lat": 34.0549, "lon": -118.2426}
    fig = px.choropleth_mapbox(df, geojson=geo_json, locations='Zip Code', color=value,
                               color_continuous_scale="Viridis",
                               # color_continuous_scale="Reds",
                               # range_color=(0, df['time'].max()),
                               featureidkey="properties.ZCTA5CE10",
                               mapbox_style="open-street-map",
                               opacity=0.5,
                               )

    fig.update_layout(mapbox_zoom=7, mapbox_center=mapbox_center)

    fig.show()

# %%
