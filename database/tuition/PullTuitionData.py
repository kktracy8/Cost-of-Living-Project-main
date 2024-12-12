from json import loads
import pandas as pd
import sqlite3
from typing import Any, Dict, List
import time
from urllib.request import urlopen

# command to create table schema
# database = sqlite3.connect("../data.db")
# cursor = database.cursor()

# create_table = """
# CREATE TABLE tuition_k12 (
#     leaid INTEGER PRIMARY KEY NOT NULL,
#     city char(25),
#     state char(10),
#     zip_code INTEGER, 
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

def major_city(row):
    return row in locations

def format_city(row):
    return row.lower().title()

def _get_district_data(school_districts: List[Dict[str, Any]]) -> List[List[Any]] | None:
    """
    Helper function to extract only relevant district data

    :param school_districts: school district data
    :return: list of lists containing school district data
    """
    keys = ('leaid', 'city_location', 'state_location', 'zip_location', 'latitude', 'longitude')
    if school_districts is None or len(school_districts) == 0:
        return
    district_data = []
    for district in school_districts:
        vals = [district[k] for k in keys]
        district_data.append(vals)
    return district_data

def pull_district_data() -> List[List[Any]]:
    """
    Pulls school district data from API for the year 2020

    :return: list of lists containing school district data
    """
    url = "https://educationdata.urban.org/api/v1/school-districts/ccd/directory/2020/"
    response = urlopen(url)
    data = loads(response.read())
    next_page = data['next']
    
    district_data = _get_district_data(data['results'])
    while next_page and len(next_page) > 0:
        response = urlopen(next_page)
        data = loads(response.read())
        new_data = _get_district_data(data['results'])
        if new_data is None: break
        district_data += new_data
        next_page = data['next']
        time.sleep(0.1)
        
    return district_data


def insert_tuition_data_values(database, cursor, columns: List[str], values: List[List[Any]]) -> None:
    """
    Inserts k-12 tuition data
    
    :param database: database connection
    :param cursor: database cursor
    :param columns: table columns
    :param values: table values
    
    :return: None
    """
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
    districts_df['leaid'] =  districts_df['leaid'].astype(int)
    
    # pull data from distract data cost dataset, pull only year 2020
    col_names =  ('leaid', 'district', 'ppcstot', 'predcost', 'year')
    district_cost = pd.read_excel('DistrictCostDatabase_2023.xlsx', sheet_name="Data", index_col=0, usecols=col_names).reset_index()
    district_cost = district_cost[district_cost.year == 2020]

    # merge district data with district cost data to get geospatial columns
    merged = districts_df.merge(district_cost, on="leaid", how="inner")
    
    merged['city'] = merged.city.apply(format_city)
    # filter out only locations we are interested in
    merged['location'] = merged['city'] + ", " + merged['state']
    merged['major_city'] = merged.location.apply(major_city)
    merged = merged[merged['major_city']].drop(['location', 'major_city'], axis=1)
    
    # get database connection and cursor
    database = sqlite3.connect("../data.db")
    cursor = database.cursor()
    
    insert_tuition_data_values(database, cursor, merged.columns.tolist(), merged.values)
        
if __name__ == "__main__":
    main()