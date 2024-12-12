import pandas as pd
import sqlite3
from typing import Any, List
# The csv file used for college tution data can be found here: https://collegescorecard.ed.gov/data/

# command to create table schema
# database = sqlite3.connect("../data.db")
# cursor = database.cursor()

# create_table = """
# CREATE TABLE tuition_college (
#     unitid INTEGER PRIMARY KEY NOT NULL,
#     instnm char(75),
#     city char(25),
#     state char(10),
#     zip_code char(10), 
#     latitude REAL,
#     longitude REAL,
#     costt4_a REAL
# )
# """
# cursor.execute(create_table)
# database.commit()

locations = ["Los Angeles, CA", "Dallas, TX", "Chicago, IL", "Boston, MA", "New York City, NY", "Denver, CO", "Las Vegas, NV"]

def clean_zipcode(row):
    if '-' in row: return row.split('-')[0]
    return row

def major_city(row):
    return row in locations
    
def insert_tuition_data_values(database, cursor, columns: List[str], values: List[List[Any]]) -> None:
    value_str = ",".join(["?"] * len(columns))
    insert_sql = f"""
    INSERT INTO tuition_college ({', '.join(columns)}) VALUES ({value_str})
    """
    cursor.executemany(insert_sql, values)
    database.commit()
    print(f"{len(values)} rows inserted")
    return

def main():
    col_names = ('UNITID', 'INSTNM', 'CITY', 'STABBR', 'ZIP', 'LATITUDE', 'LONGITUDE', 'COSTT4_A')
    college_tuition = pd.read_csv('Most-Recent-Cohorts-Institution.csv',
        header=0,
        usecols=col_names).reset_index()
    college_tuition = college_tuition[college_tuition.COSTT4_A.notnull()].drop('index', axis=1)
    college_tuition['ZIP'] = college_tuition['ZIP'].apply(clean_zipcode)

    # filter out only locations we are interested in
    college_tuition['location'] = college_tuition['CITY'] + ", " + college_tuition['STABBR']
    college_tuition['major_city'] = college_tuition.location.apply(major_city)
    college_tuition = college_tuition[college_tuition['major_city']].drop(['location', 'major_city'], axis=1)

    # get database connection and cursor
    database = sqlite3.connect("../data.db")
    cursor = database.cursor()

    columns = ('unitid', 'instnm', 'city', 'state', 'zip_code', 'latitude', 'longitude', 'costt4_a')
    insert_tuition_data_values(database, cursor, columns, college_tuition.values)

if __name__ == "__main__":
    main()
