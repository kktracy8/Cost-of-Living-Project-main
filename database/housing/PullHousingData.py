import requests
import logging
from pydantic import BaseModel
import sqlite3
from typing import Any, Dict, List
import time

url = 'https://zillow69.p.rapidapi.com/search'



logger = logging.getLogger()

# Create statement for prop_data table
# create_table = """
# CREATE TABLE prop_data (
#     zpid TEXT PRIMARY KEY NOT NULL,
#     latitude REAL,
#     longitude REAL,
#     price REAL, 
#     living_area REAL,
#     address CHAR(50),
#     for_rent TINYINT,
#     property_type CHAR(30),
#     zip_code CHAR(10), 
#     city char(25),
#     state char(10)
# )
# """

# Pydantic class for holding housing data
class HousingData(BaseModel):
    zpid: str
    latitude: float
    longitude: float
    price: float
    living_area: float
    address: str
    property_type: str
    for_rent: int
    zip_code: str
    city: str
    state: str


def _extract_housing_data(props: Dict[str, Any], location: str, for_rent: bool) -> HousingData | None:
    try:
        zpid = props['zpid']
        latitude = float(props['latitude'])
        longitude = float(props['longitude'])
        price = float(props['price'])
        living_area = float(props['livingArea'])
        address = props['address']
        property_type = props['propertyType']
        # parse zip code
        try:
            zip_code = address.split()[-1]
        except Exception as e:
            # dont want houses without associated zip codes
            return
        loc_toks = location.split(",")
        city = loc_toks[0].strip()
        state = loc_toks[1].strip()

        housing_data = HousingData(
            zpid=zpid,
            latitude=latitude,
            longitude=longitude,
            price=price,
            living_area=living_area,
            address=address,
            for_rent = int(for_rent),
            property_type=property_type,
            zip_code=zip_code,
            city=city,
            state=state
        )
        return housing_data
    except Exception as e:
        logger.warning(f"Issue parsing price data from property: {zpid}, Exception: {e}")
    return


def extract_housing_data(data_props: List[Dict[str, Any]], location: str, for_rent: bool) -> List[HousingData]:
    housing_datas = []
    for props in data_props:
        house_data = _extract_housing_data(props, location, for_rent)
        if house_data: housing_datas.append(house_data)
    return housing_datas


def pull_housing_data(location: str, home_type: str, for_rent: bool) -> List[HousingData]:
    housing_data: List[HousingData] = []
    params = {
        'location': location,
        'home_type': home_type,
        'status_type': "ForRent" if for_rent else "ForSale"
    }
    
    data = requests.get(url, headers=headers, params=params).json()
    # Pull data necessary for pagination
    total_result_count = data['totalResultCount']
    total_pages = data['totalPages']
    cur_page = data['currentPage']
    
    if total_result_count == 0: return []
    # extract initial housing data and append to result list
    housing_data += extract_housing_data(data['props'], location, for_rent)
    
    while cur_page <= total_pages:
        cur_page += 1
        # update page number in param calls
        params['page'] = cur_page
        data = requests.get(url, headers=headers, params=params).json()
        if 'props' not in data:
            print(f"No prop data on page: {cur_page}, for location: {location}")
            break
        housing_data += extract_housing_data(data['props'], location, for_rent)
        time.sleep(.5)

    return housing_data


def pull_all_housing_data(location) -> List[HousingData]:
    home_types = ['Multi-Family', 'Apartments', 'Houses', 'Manufactured', 'Condos', 'Townhomes']
    housing_data = []
    
    # Pull all houses for sale in each location
    for home_type in home_types:
        housing_data += pull_housing_data(location, home_type, False)
    
    # Pull all rentals in each location
    for home_type in home_types:
        housing_data += pull_housing_data(location, home_type, True)
    
    
    print(f"Total properties pulled for {location} -> {len(housing_data)}")
    return housing_data


def insert_house_data_values(database, cursor, house_data: List[Dict[str, Any]]):
    # create list of tuples for row values
    values = []
    keys = None
    existing_zpids = []
    # column names
    for data in house_data:
        if data["zpid"] in existing_zpids:
            continue
        
        if keys is None:
            keys = [*data.keys()]
        values.append(tuple([*data.values()]))
        existing_zpids.append(data["zpid"])

    value_str = ",".join(["?"] * len(keys))
    insert_sql = f"""
    INSERT INTO prop_data ({', '.join(keys)}) VALUES ({value_str})
    """
    cursor.executemany(insert_sql, values)
    database.commit()
    print(f"{len(values)} rows inserted")
    return

def main():
    # database file
    database = sqlite3.connect("../data.db")
    cursor = database.cursor()

    locations = ["Los Angeles, CA", "Dallas, TX", "Chicago, IL", "Boston, MA", "New York City, NY", "Denver, CO", "Las Vegas, NV"]
    for location in locations:
        results = pull_all_housing_data(location)
        result_dicts = [res.model_dump() for res in results]
        insert_house_data_values(database, cursor, result_dicts)
    return

if __name__ == "__main__":
    main()