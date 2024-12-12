from database.database import DB
import pandas as pd

def _is_numeric(row: str):
    return row.isnumeric()

def sale_prices_by_zipcode(property_type: str, city: str, state: str) -> pd.DataFrame:
    """
    Gets mean house price by zip code

    :param property_type: property type, ex (SFH, MFH, etc)
    :param city: city 
    :param state: state
    :return: pandas dataframe containing mean house price by zip code
    """
    db = DB()
    df = db.get_housing_data(property_type, city, state)
    df = df[df['for_rent'] == 0]
    df = df[df['zip_code'].apply(_is_numeric)]
    result_df = df.groupby('zip_code').price.agg('mean').to_frame().reset_index().rename(
        columns={"price": "mean_price"})
    
    
    return result_df


def sale_prices_by_city() -> pd.DataFrame:
    """
    Gets mean house price by each location (city, state)

    :return: pandas dataframe containing mean house price by each location
    """
    db = DB()
    df = db.get_all_housing_data()
    df = df[df['for_rent'] == 0]
    df = df.astype({'city': str, 'state': str})
    df['location'] = df['city'] + ", " + df['state']
    result_df = df.groupby('location').price.agg('mean').to_frame().reset_index().rename(
        columns={"price": "mean_price"})
    return result_df

def rent_prices_by_zipcode(property_type: str, city: str, state: str) -> pd.DataFrame:
    """
    Gets mean house price by zip code

    :param property_type: property type, ex (SFH, MFH, etc)
    :param city: city 
    :param state: state
    :return: pandas dataframe containing mean house price by zip code
    """
    db = DB()
    df = db.get_housing_data(property_type, city, state)
    df = df[df['for_rent'] == 1]
    df = df[df['zip_code'].apply(_is_numeric)]
    result_df = df.groupby('zip_code').price.agg('mean').to_frame().reset_index().rename(
        columns={"price": "mean_price"})
    return result_df

def rent_prices_by_city() -> pd.DataFrame:
    """
    Gets mean house price by each location (city, state)

    :return: pandas dataframe containing mean house price by each location
    """
    db = DB()
    df = db.get_all_housing_data()
    df = df[df['for_rent'] == 1]
    df = df.astype({'city': str, 'state': str})
    df['location'] = df['city'] + ", " + df['state']
    result_df = df.groupby('location').price.agg('mean').to_frame().reset_index().rename(
        columns={"price": "mean_price"})
    return result_df

def add_rent_price(df: pd.DataFrame, location, property_type) -> pd.DataFrame:
    if 'Rent Price' in df.columns:
        df = df.drop(columns='Rent Price')
    # location = location[0]
    loc_toks = location.split(",")
    city = loc_toks[0].strip()
    state = loc_toks[1].strip()
    rent_prices = rent_prices_by_zipcode(property_type, city, state)
    rent_prices = rent_prices.rename(columns={'zip_code': 'Zip Code', 'mean_price': 'Rent Price'})

    rent_prices['Zip Code'] = rent_prices['Zip Code'].astype(str)
    df = df.merge(rent_prices, on='Zip Code', how='left')

    # fill NA with average house price for city
    df['Rent Price'] = df['Rent Price'].fillna(rent_prices['Rent Price'].mean())

    df['Annual Rent'] = df['Rent Price'] * 12  # rough estimate based on monthly rent

    return df


def add_sale_price(df: pd.DataFrame, location, property_type) -> pd.DataFrame:
    if 'House Price' in df.columns:
        df = df.drop(columns='House Price')
    # location = location[0]
    loc_toks = location.split(",")
    city = loc_toks[0].strip()
    state = loc_toks[1].strip()
    sale_prices = sale_prices_by_zipcode(property_type, city, state)
    sale_prices = sale_prices.rename(columns={'zip_code': 'Zip Code', 'mean_price': 'House Price'})

    sale_prices['Zip Code'] = sale_prices['Zip Code'].astype(str)
    df = df.merge(sale_prices, on='Zip Code', how='left')

    # fill NA with average house price for city
    df['House Price'] = df['House Price'].fillna(sale_prices['House Price'].mean())

    df['Annual Rent'] = df['House Price'] * 0.005 * 12  # rough estimate based on house price

    return df

def annual_rent_price_city(rent_or_buy: str):
    
    rent_flag = rent_or_buy == "RENT"
    db = DB()
    df = db.get_all_housing_data()
    df = df[df['for_rent'] == rent_flag]
    result_df = df.groupby('city').price.agg('mean').to_frame().reset_index().rename(
        columns={"price": "mean_price"})
    
    if rent_flag:
        result_df['Annual Rent'] = result_df['mean_price'] * 12
    else:
        result_df['Annual Rent'] = result_df['mean_price'] * 0.005 * 12
    
    result_df = result_df[['city','Annual Rent']]
    result_df = result_df.T
    result_df.columns = result_df.iloc[0]
    result_df = result_df.drop(result_df.index[0])
    return result_df

def annual_rent_price_state(rent_or_buy: str):
    
    rent_flag = rent_or_buy == "RENT"
    db = DB()
    df = db.get_all_housing_data()
    df = df[df['for_rent'] == rent_flag]
    
    states = {'CA': 'California',
              'TX': 'Texas',
              'CO': 'Colorado',
              'NV': 'Nevada',
              'NY': 'New York',
              'MA': 'Massachusetts',
              'IL': 'Illinois'}
    
    df['state'] = df['state'].apply(lambda x: states[x])
    
    result_df = df.groupby('state').price.agg('mean').to_frame().reset_index().rename(
        columns={"price": "mean_price"})
    
    if rent_flag:
        result_df['Annual Rent'] = result_df['mean_price'] * 12
    else:
        result_df['Annual Rent'] = result_df['mean_price'] * 0.005 * 12
    
    # result_df['Annual Rent'] = result_df['Annual Rent'].map('${:,.0f}'.format)
    result_df = result_df.rename(columns={'state': 'Item'})
    result_df = result_df[['Item', 'Annual Rent']]
    result_df = result_df.T
    result_df = result_df.reset_index(names='Item')
    result_df.columns = result_df.iloc[0]
    result_df = result_df.drop(result_df.index[0])
    result_df = result_df[['Item', 'California', 'Colorado', 'Illinois', 'Massachusetts', 'Nevada', 'New York', 'Texas']]
    result_df['Item'] = 'Annual Rent'
    return result_df

