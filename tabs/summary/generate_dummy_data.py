import json

import numpy as np
import pandas as pd

# import database.geo_json_data.zip_code_list as zc
from database.database import DB


def create_empty_df(city):
    db = DB()
    zip_codes = db.get_zip_codes(city)
    df = pd.DataFrame(index=zip_codes)
    df = df.reset_index(names='Zip Code')

    return df


def create_dummy_data(value_options, cities, db):  # only used for testing.

    df_list = []
    for i, city in enumerate(cities):
        df_city = create_empty_df(city, value_options)
        df_list.append(df_city)

    df = pd.concat(df_list)
    df_avg = df.groupby(['City', 'State Short']).mean().reset_index()

    df_avg['Zip Code'] = df_avg['City']
    df = df.reset_index(names='Zip Code')
    df = pd.concat([df_avg, df])

    # add in combined tax rates
    df_tax = db.tax_rates()
    df = df.merge(df_tax[['State Short', 'Combined Rate']], on='State Short', how='left')

    return df


# code to test
if __name__ == '__main__':
    cities = [
        'Los Angeles, CA',
        'Dallas, TX',
        'Chicago, IL',
        'Boston, MA',
        'New York City, NY',
        'Denver, CO',
        'Las Vegas, NV'
    ]

    value_options = ['Tax Estimate', 'State Tax Rate', 'Avg. Local Tax Rate', 'Income', 'Cost of Goods', 'Tuition',
                     'Commute Time']
    db = DB()
    df = create_dummy_data(value_options, cities, db)
