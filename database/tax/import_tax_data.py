import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///database/data.db', echo=False)

# load sales tax data
df1 = pd.read_excel('database/tax/data/2024 Sales Tax Rates State  Local Sales Tax by State.xlsx')
state_short = pd.read_excel('database/tax/data/State Abbreviation.xlsx')
df1 = df1.merge(state_short, left_on="State", right_on="State Full")
df1.to_sql('tax_rates', con=engine, if_exists='replace', index=False)
# %%
# load property tax data
df2 = pd.read_excel("database/tax/data/propety taxes 2024.xlsx")
df2 = df2.merge(state_short, left_on="State", right_on="State Full")
df2.to_sql('tax_property', con=engine, if_exists='replace', index=False)

# %%
# load sales tax data
df2 = pd.read_excel("database/tax/data/sales tax by state.xlsx")
df2 = df2.rename(columns={'State:': 'State'})
df2 = df2.merge(state_short, left_on="State", right_on="State Full")
df2.to_sql('tax_sales', con=engine, if_exists='replace', index=False)

# %%
df2 = pd.read_excel("database/tax/data/fed_tax_brackets.xlsx")
df2.to_sql('tax_brackets', con=engine, if_exists='replace', index=False)
