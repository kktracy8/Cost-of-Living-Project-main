import json

import pandas as pd
from sqlalchemy import create_engine, Engine, text


class DB:

    def __init__(self):
        self.engine: Engine = create_engine('sqlite:///database/data.db', echo=False)

    # ***********************    Common Helper Functions     #####################################
    def read_table_to_df(self, table_name):
        with self.engine.connect() as con:
            df = pd.read_sql_table(table_name, con)
        return df

    def read_sql_to_df(self, sql):
        with self.engine.connect() as con:
            df = pd.read_sql(sql, con)
        return df

    def get_geo_json(self, city):
        with self.engine.connect() as con:
            cur = con.execute(text(f"SELECT geo_json FROM geo_json WHERE city = '{city}'"))
            geo_json = cur.fetchone()._data[0]
        return json.loads(geo_json)

    def get_zip_codes(self, city):
        with self.engine.connect() as con:
            cur = con.execute(text(f"SELECT zip_codes FROM geo_json WHERE city = '{city}'"))
            zip_codes = cur.fetchone()._data[0]
        return zip_codes.split(',')

    # ***********************    Tax Tab     **********************************************
    def tax_rates(self):
        df = self.read_table_to_df('tax_rates')
        df = df[['State', 'Avg. Local Tax Rate', 'State Tax Rate','Combined Rate', 'State Short']]
        df_property_tax = self.read_table_to_df('tax_property')
        df = df.merge(df_property_tax[['State Short','Effective Tax Rate']], on='State Short')
        return df

    def tax_brackets(self):
        return self.read_table_to_df('tax_brackets')

    def property_tax(self):
        sql = "SELECT * FROM tax_property"
        return self.read_sql_to_df(sql)

    # ***********************    Income Tab     **********************************************
    def read_income_comparison(self):
        return self.read_table_to_df('income_comparison')

    def read_income(self, city, occupations):
        query = f"""
        SELECT a_mean FROM income
        WHERE occ_title in ({', '.join([f"'{x}'" for x in occupations])}) AND city = '{city}'
        """
        return self.read_sql_to_df(query)

    # *********************** Housing Prices Tab *********************************************

    def get_housing_data(self, property_type: str, city: str, state: str):
        query = f"""
        SELECT * FROM prop_data
        WHERE property_type = '{property_type}' AND city = '{city}' AND state = '{state}'
        """
        return self.read_sql_to_df(query)

    def get_all_housing_data(self):
        query = f"""
        SELECT * FROM prop_data
        """
        return self.read_sql_to_df(query)

    def get_property_types(self):
        query = f"""
        SELECT DISTINCT property_type FROM prop_data
        """
        return self.read_sql_to_df(query)

    # ***********************     Tuition Tab     **********************************************
    def get_k12_spending_data(self, city: str, state: str):
        query = f"""
        SELECT * FROM tuition_k12
        WHERE city = '{city}' AND state = '{state}'
        """
        return self.read_sql_to_df(query)

    def get_all_k12_spending_data(self):
        query = f"""
        SELECT * FROM tuition_k12
        """
        return self.read_sql_to_df(query)

    def get_college_tuition_data(self, city: str, state: str):
        query = f"""
        SELECT * FROM tuition_college
        WHERE city = '{city}' AND state = '{state}'
        """
        return self.read_sql_to_df(query)

    def get_all_college_tuition_data(self):
        query = f"""
        SELECT * FROM tuition_college
        """
        return self.read_sql_to_df(query)

    # ***********************     Goods Tab     **********************************************
    def gas_rates(self):
        return self.read_table_to_df('gas_rates')

    def food_rates(self):
        return self.read_table_to_df('food_rates')

    def food_invert(self):
        return self.read_table_to_df('food_invert')


# test class methods by running file directly
if __name__ == '__main__':
    db = DB()
    df = db.property_tax()
    # geo_json = db.get_geo_json('Los Angeles, CA')
