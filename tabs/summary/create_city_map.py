import plotly.express as px

from database.database import DB


def get_city_center(city):
    match city:
        case 'Los Angeles, CA':
            return 34.0549, -118.2426
        case 'Las Vegas, NV':
            return 36.1716, -115.1391
        case 'Chicago, IL':
            return 41.8781, -87.6298
        case 'Dallas, TX':
            return 32.7767, -96.7970
        case 'Boston, MA':
            return 42.3601, -71.0589
        case 'New York City, NY':
            return 40.7128, -74.0060
        case 'Denver, CO':
            return 39.7392, -104.9903
        case _:
            return 34.0549, -118.2426


def create_city_map(city, value, df, hover_format, custom_data = None,height=500):
    # with open(f'database/geo_json_data/{city}.json') as f:
    #     geo_json = json.load(f)
    db = DB()
    geo_json = db.get_geo_json(city)
    zip_codes = db.get_zip_codes(city)
    df['Zip Code'] = df['Zip Code'].astype(str)
    lat, lon = get_city_center(city)
    mapbox_center = {"lat": lat, "lon": lon}
    # print(df[value].min(), df[value].max())
    # print(df.sort_values(value, ascending=False))
    # print(df)
    # print(zip_codes)

    color_scheme = {
        'Net Income': 'RdBu',
    }


    df = df[df['Zip Code'].isin(zip_codes)]
    # print(df)
    fig = px.choropleth_mapbox(df, geojson=geo_json, locations='Zip Code', color=value,
                               color_continuous_scale=color_scheme.get(value, 'Turbo'), opacity=0.8,
                               # range_color=(df[value].min(), df[value].max()),c
                               custom_data=custom_data,
                               featureidkey="properties.ZCTA5CE10",
                               mapbox_style="open-street-map",
                               # hover_data=hover_format,

                               height=500
                               )
    fig.update_traces(hovertemplate=hover_format)

    fig.update_layout(mapbox_zoom=8, mapbox_center=mapbox_center, margin={'l': 5, 'r': 5, 't': 5, 'b': 5})
    # fig.show()

    return fig
