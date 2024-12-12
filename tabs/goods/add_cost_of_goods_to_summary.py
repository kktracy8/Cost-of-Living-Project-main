from database.database import DB
import pandas as pd


def add_cost_of_goods(df, city, gas_status, family_size):
    if 'Fuel Price' in df.columns:
        df = df.drop(columns='Fuel Price')

    db = DB()
    df_gas = db.gas_rates()
    df_gas = df_gas.loc[df_gas['city'] == city]
    df_gas = df_gas.loc[df_gas[gas_status] > 0]
    df_gas = df_gas.rename(columns={'Zip code': 'Zip Code', gas_status: 'Fuel Price'})
    df_gas = df_gas[['Zip Code', 'Fuel Price']]
    df_gas['Zip Code'] = df_gas['Zip Code'].astype(str)
    df = df.merge(df_gas, on='Zip Code', how='left')

    df_food = db.food_invert()
    if isinstance(family_size, list):
        family_size1 = family_size[-1]
    else:
        family_size1 = family_size
    df_food = df_food.loc[df_food['value'] == family_size1, city].values[0]
    df['Annual Food'] = df_food * 12
    return df

def avg_fuel_price(gas_status):
    db = DB()
    df_gas = db.gas_rates()
    cities = ['Los Angeles, CA','Denver, CO','Chicago, IL','Boston, MA','Las Vegas, NV','New York City, NY','Dallas, TX']
    avg = []
    avg.append('Average Fuel Cost')
    for x in cities:
        df_gas2 = df_gas.loc[df_gas['city'] == x]
        price = df_gas2[gas_status].tolist()
        avg.append('$ ' + str(round((sum(price) / len(price)), 3)))
    df = pd.DataFrame([avg], columns=['Item','California','Colorado','Illinois','Massachusetts','Nevada','New York','Texas'])
    return df

def annual_food_cost(family_size):
    db = DB()
    df_invert = db.food_invert()
    cost = []
    cost.append('Annual Food Cost')
    if isinstance(family_size, list):
        family_size1 = family_size[-1]
    else:
        family_size1 = family_size
    invert = df_invert.loc[df_invert['value'] == family_size1].values.tolist()
    c = 0
    for x in invert:
        for y in x:
            if c != 0:
                # z = ('{:,}'.format(y * 12))
                # cost.append('$ ' + str(z))
                cost.append(y*12)
            c += 1
    myorder = [0, 3, 5, 4, 6, 2, 7, 1]
    cost = [cost[i] for i in myorder]
    df = pd.DataFrame([cost], columns=['Item','California','Colorado','Illinois','Massachusetts','Nevada','New York','Texas'])
    return df
