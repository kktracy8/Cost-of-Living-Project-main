import pandas as pd
import plotly.express as px

from database.database import DB




# %%
def load_data():
    df = pd.read_excel('tabs/tax/data/2024 Sales Tax Rates State  Local Sales Tax by State.xlsx')
    state_short = pd.read_excel("tabs/tax/data/State Abbreviation.xlsx")
    df = df.merge(state_short, left_on="State", right_on="State Full")
    return df


df = load_data()
# %%


fig = px.choropleth(
    df,
    locations="State Short",
    color="Avg. Local Tax Rate",
    color_continuous_scale='Reds',
    scope="usa",
    locationmode="USA-states",
)
fig.show()

# %%
