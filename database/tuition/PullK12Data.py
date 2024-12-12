from json import loads
import pandas as pd
import sqlite3
from typing import Any, Dict, List
import time
from urllib.request import urlopen
from geopy.distance import geodesic
# Excel file pulled K-12 spending data can be found here: https://www.schoolfinancedata.org/download-data/

# command to create table schema
# database = sqlite3.connect("../data.db")
# cursor = database.cursor()

# create_table = """
# CREATE TABLE tuition_k12 (
#     leaid INTEGER PRIMARY KEY NOT NULL,
#     city char(25),
#     state char(10),
#     zip_code char(10), 
#     latitude REAL,
#     longitude REAL,
#     year INTEGER,
#     district CHAR(30),
#     ppcstot REAL,
#     predcost REAL
# )
# """
# cursor.execute(create_table)
# database.commit()

locations = ["Los Angeles, CA", "Dallas, TX", "Chicago, IL", "Boston, MA", "New York City, NY", "Denver, CO", "Las Vegas, NV"]
states = ["CA", "TX", "IL", "MA", "NY", "CO", "NV"]


def get_mapbox_center(location: str) -> Dict[str, float]:
    match location:
        case 'Los Angeles, CA':
            mapbox_center = {"lat": 34.0549, "lon": -118.2426}
        case 'Las Vegas, NV':
            mapbox_center = {"lat": 36.1716, "lon": -115.1391}
        case 'Chicago, IL':
            mapbox_center = {"lat": 41.8781, "lon": -87.6298}
        case 'Dallas, TX':
            mapbox_center = {"lat": 32.7767, "lon": -96.7970}
        case 'Boston, MA':
            mapbox_center = {"lat": 42.3601, "lon": -71.0589}
        case 'New York City, NY':
            mapbox_center = {"lat": 40.7128, "lon": -74.0060}
        case 'Denver, CO':
            mapbox_center = {"lat": 39.7392, "lon": -104.9903}
        case _:
            mapbox_center = {"lat": 34.0549, "lon": -118.2426}
    return mapbox_center

def mark_state(row):
    states = ["CA", "TX", "IL", "MA", "NY", "CO", "NV"]
    return row in states

def get_district_data(school_districts: List[Dict[str, Any]]) -> List[List[Any]] | None:
    keys = ('leaid', 'city_location', 'state_location', 'zip_location', 'latitude', 'longitude')
    if school_districts is None or len(school_districts) == 0:
        return
    district_data = []
    for district in school_districts:
        vals = [district[k] for k in keys]
        district_data.append(vals)
    return district_data

def pull_district_data() -> List[List[Any]]:
    url = "https://educationdata.urban.org/api/v1/school-districts/ccd/directory/2020/"
    response = urlopen(url)
    data = loads(response.read())
    next_page = data['next']
    
    district_data = get_district_data(data['results'])
    while next_page and len(next_page) > 0:
        response = urlopen(next_page)
        data = loads(response.read())
        new_data = get_district_data(data['results'])
        if new_data is None: break
        district_data += new_data
        next_page = data['next']
        time.sleep(0.1)
        
    return district_data


def get_districts_near_cities(districts_df: pd.DataFrame) -> List[str]:
    # Code to only get school districts with 25 miles of city center
    lats = districts_df.latitude.tolist()
    lons = districts_df.longitude.tolist()
    
    nearby_cities = []
    for lat, lon in zip(lats, lons):
        nearby_city = None
        for loc in locations:
            loc_dict = get_mapbox_center(loc)
            dist_miles = geodesic((lat, lon), (loc_dict['lat'], loc_dict['lon'])).miles
            if dist_miles < 25:
                nearby_city = loc.split(',')[0].strip()
        nearby_cities.append(nearby_city)
    return nearby_cities


def insert_tuition_data_values(database, cursor, columns: List[str], values: List[List[Any]]) -> None:
    value_str = ",".join(["?"] * len(columns))
    insert_sql = f"""
    INSERT INTO tuition_k12 ({', '.join(columns)}) VALUES ({value_str})
    """
    cursor.executemany(insert_sql, values)
    database.commit()
    print(f"{len(values)} rows inserted")
    return


def main():

    district_data = pull_district_data()
    # create dataframe from pulled districts data
    columns = ('leaid', 'city', 'state', 'zip_code', 'latitude', 'longitude')
    districts_df = pd.DataFrame(data=district_data, columns=columns)
    districts_df['leaid'] = districts_df['leaid'].astype(int)
    
    districts_df['state_flag'] = districts_df.state.apply(mark_state)
    districts_df = districts_df[districts_df.state_flag].drop("state_flag", axis=1)   
    
    # Code to only get school districts with 25 miles of city center
    nearby_cities = get_districts_near_cities(districts_df)
    
    districts_df['nearby_city'] = nearby_cities
    filtered_districts_df = districts_df[districts_df.nearby_city.notna()].drop('city', axis=1)
    filtered_districts_df = filtered_districts_df.rename(columns={'nearby_city':'city'})
    
    # pull data from distract data cost dataset, pull only year 2020
    col_names =  ('leaid', 'district', 'ppcstot', 'predcost', 'year')
    district_cost = pd.read_excel('DistrictCostDatabase_2023.xlsx', sheet_name="Data", index_col=0, usecols=col_names).reset_index()
    district_cost = district_cost[district_cost.year == 2020]
    # merge district data with district cost data to get geospatial columns
    merged = filtered_districts_df.merge(district_cost, on="leaid", how="inner")
    # reorg columns
    merged = merged[['leaid', 'city', 'state', 'zip_code', 'latitude', 'longitude', 'year',
           'district', 'ppcstot', 'predcost']]

    # get database connection and cursor
    database = sqlite3.connect("../data.db")
    cursor = database.cursor()
    
    insert_tuition_data_values(database, cursor, merged.columns.tolist(), merged.values)
        
if __name__ == "__main__":
    main()