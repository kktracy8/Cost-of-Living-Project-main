import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///database/goods/Goodsdata.db', echo=False)

# load sales tax data
df1 = pd.read_excel('database/goods/goods_data/gas.xlsx')
for row in df1:
    df1['city'] = df1['Cities'] + ", " + df1['state']
df1.to_sql('gas_rates', con=engine, if_exists='replace', index=False)

df2 = pd.read_excel('database/goods/goods_data/food.xlsx')
df2.to_sql('food_rates', con=engine, if_exists='replace', index=False)

df3 = pd.read_excel('database/goods/goods_data/invert.xlsx')
df3.to_sql('food_invert', con=engine, if_exists='replace', index=False)
