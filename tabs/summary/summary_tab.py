from io import StringIO

import pandas as pd
from dash import html, Output, Input, dcc, Dash, State, dash_table
from dash.dash_table.Format import Format, Scheme, Group, Symbol
from dash.exceptions import PreventUpdate

from database.database import DB
from tabs.commute.commute_api import add_commute_cost
from tabs.goods.add_cost_of_goods_to_summary import add_cost_of_goods, annual_food_cost
from tabs.housing.utils import add_sale_price, add_rent_price, annual_rent_price_state
from tabs.income.add_income_to_summary import calc_est_income
from tabs.summary.create_city_map import create_city_map, get_city_center
from tabs.summary.generate_dummy_data import create_empty_df
from tabs.summary.input_layout_utils import generate_card_card, form_input
from tabs.tax.calc_tax_rates import add_tax_rate, average_tax_rate

cities = [
    'Dallas, TX',
    'Los Angeles, CA',
    'Chicago, IL',
    'Boston, MA',
    'New York City, NY',
    'Denver, CO',
    'Las Vegas, NV',
]

#
# value_options = ['Annual Rent', 'Income', 'Tax Estimate', 'State Tax Rate', 'Avg. Local Tax Rate', 'Fuel Price',
#                  'Food Cost', 'Tuition', 'Commute Time']
# value_options = ['Net Income', 'Income', 'Tax Estimate', 'Annual Rent', 'Annual Fuel Cost', 'Annual Commute Time Cost',
#                  'Annual Food']  # 'Fuel Price', 'Annual Rent',
value_options = [
    'Zip Code',
    'Income',
    'Annual Rent',
    'Annual Food',
    'Annual Fuel Cost',
    'Annual Commute Time Cost',
    'Federal Taxes',
    'Child Tax Credit',
    'State Taxes',
    'Property Taxes',
    'Total Taxes',
    'Net Income'
]


def render_layout_summary():
    # value_dropdown = dcc.Dropdown(value_options, value_options[0], id='dropdown-value')
    # city_dropdown = dcc.Dropdown(cities, id='dropdown-zipcode', multi=True)

    map_div = html.Div(
        className='p-4',
        children=[
            html.Div(
                form_input('Graphed Value', value_options[-1], options=value_options[1:]),
                className='w-50  mx-auto',
            ),
            html.Hr(),
            dcc.Loading(children=html.Div(id='div-graph')),
        ]
    )

    table_div = html.Div(
        className='p-4',
        children=[
            html.Div(
                form_input('Zip Codes', '', options=[''], multi=True),
                className='w-75  mx-auto',
            ),
            html.Hr(),
            html.H4('Annual Income and Expenses by Zip Code'),
            dcc.Loading(children=html.Div(id='div-table'))
        ]
    )

    layout = html.Div(
        className='',
        children=[
            generate_card_card('City Map', 'far fa-map', map_div),
            generate_card_card('Zip Code - Comparison Table', 'fa fa-table', table_div),
        ],
    )
    return layout


def register_summary_callbacks(app: Dash):
    @app.callback(
        Output('workplace_longitude', 'value'),
        Output('workplace_latitude', 'value'),
        Input('location', 'value'),
    )
    def update_lat_and_lon(location):
        lat, lon = get_city_center(location)
        return lat, lon

    @app.callback(
        Output('df', 'data'),
        Output('div-city-table', 'children'),
        Output('loading_main', 'type'),  # trigger loading indicator
        Input('run_callbacks', component_property='n_clicks'),
        Input('run_button', 'n_clicks'),
        State('tabs', 'value'),
        State('location', 'value'),
        State('filing_status', 'value'),
        State('income', 'value'),
        State('property_type', 'value'),
        State('current_occupation(s)', 'value'),
        State('fuel_type', 'value'),
        State('family_size', 'value'),
        State('number_of_kids', 'value'),
        State('property_value', 'value'),
        State('workplace_longitude', 'value'),
        State('workplace_latitude', 'value'),
        State('fuel_cost', 'value'),
        State('time_cost_($/hr)', 'value'),
        State('vehicle_mpg', 'value'),
        State('rent_or_buy', 'value'),
        prevent_initial_call=True,
    )
    def update_df(_, run, tab, location, tax_status, income, property_type, occupations, gas_status, family_size, kids,
                  property_value, long, lat, fuel_cost, time_cost, mpg, rent_or_buy):
        if tab != 'tab-summary':
            PreventUpdate()
            raise PreventUpdate
        if pd.isna(income):
            income = 0
        print('updating summary data')

        # hard code to single family for summary tab
        property_type = 'SINGLE_FAMILY'

        # data for selected city
        df = create_empty_df(location)
        # df = add_income(df, occupations, location)
        df['Income'] = (income)
        df = add_tax_rate(df, location, income, kids, tax_status, property_value)
        if rent_or_buy == "RENT":
            df = add_rent_price(df, location, property_type)
        else:
            df = add_sale_price(df, location, property_type)
        df = add_cost_of_goods(df, location, gas_status, family_size)
        df = add_commute_cost(df, location, (long, lat), mpg, fuel_cost, time_cost)
        # print(df.columns)

        df['Net Income'] = (df['Income'] - df['Total Taxes'] - df['Annual Food'] - df['Annual Fuel Cost'] -
                            df['Annual Commute Time Cost'] - df['Annual Rent'])

        # city average data
        df_city = average_tax_rate(income, kids, tax_status, property_value)

        # add annual fuel price for city
        # df_state_gas = avg_fuel_price(gas_status)
        # df_city = pd.concat([df_state_gas, df_city],ignore_index=True)

        # add avg food costs
        df_state_food = annual_food_cost(family_size)
        df_city = pd.concat([df_state_food, df_city], ignore_index=True)

        # add estimated income by city
        df_cityincome = calc_est_income(income, occupations, location)
        df_city = pd.concat([df_cityincome, df_city], ignore_index=True)

        df_state_rent = annual_rent_price_state(rent_or_buy)
        df_city = pd.concat([df_state_rent, df_city], ignore_index=True)
        df_city = df_city.set_index('Item')

        # apply sum and format table
        df_city.loc['Adjusted Income'] = -1 * df_city.loc['Adjusted Income']
        df_city = df_city.map(lambda x: -1 * x)
        df_city = df_city.loc[['Adjusted Income', 'Annual Rent', 'Annual Food Cost', 'Federal Taxes',
                               'Child Tax Credit', 'State Taxes', 'Property Taxes']]
        df_city.loc['Net Income'] = df_city.sum()
        df_city = df_city.reset_index()

        df_city = df_city.rename(columns={
            'California': 'Los Angeles, CA',
            'Texas': 'Dallas, TX',
            'Illinois': 'Chicago, IL',
            'Massachusetts': 'Boston, MA',
            'New York': 'New York City, NY',
            'Colorado': 'Denver, CO',
            'Nevada': 'Las Vegas, NV',
        })

        num_format = Format(precision=0, scheme=Scheme.fixed, group=Group.yes, symbol=Symbol.yes)
        cols = [{"name": str(i), "id": str(i)} if i in ['Item']
                else {"name": str(i), "id": str(i), 'type': 'numeric', 'format': num_format}
                for i in df_city.columns]

        # create city average table
        table = dash_table.DataTable(
            data=df_city.to_dict('records'),
            columns=cols  # [{"name": str(i), "id": str(i)} for i in df_city.columns]
        )

        return df.to_json(date_format='iso', orient='split'), table, 'default'

    @app.callback(
        Output('div-graph', 'children'),
        Output('zip_codes', 'options'),
        Output('zip_codes', 'value'),
        Input('df', 'data'),
        State('tabs', 'value'),
        State('location', 'value'),
        Input('graphed_value', 'value'),
        prevent_initial_call=True,

    )
    def update_graph(json_df, tab, city, value):
        if tab != 'tab-summary':
            PreventUpdate()
        print('updating summary graph')
        if not city:
            return 'Please select a city'

        hovertemplate = '''
<b>Annual Costs: Zip Code %{customdata[0]} </b><br><br>
Adjusted Income:  $ %{customdata[1]:,.1f} <br>
Rent:             $ %{customdata[2]:,.0f} <br>
Food:             $ %{customdata[3]:,.0f} <br>
Fuel Cost:        $ %{customdata[4]:,.0f} <br>
Commute Time Cost: $ %{customdata[5]:,.0f} <br>
Federal Taxes:    $ %{customdata[6]:,.0f} <br>
Child Tax Credit: $ %{customdata[7]:,.0f} <br>
State Taxes:      $ %{customdata[8]:,.0f} <br>
Property Taxes:   $ %{customdata[9]:,.0f} <br>
Total Taxes:      $ %{customdata[10]:,.0f} <br><br>
Net Income:       $ %{customdata[11]:,.0f} <br>
                '''  # : $ %{customdata[]:,.0f} <br>

        df = pd.read_json(StringIO(json_df), orient='split')

        map = create_city_map(city, value, df, hovertemplate, custom_data=value_options)
        zip_code_options = DB().get_zip_codes(city)

        return dcc.Graph(figure=map), [f'{city} Avg.', *zip_code_options], [f'{city} Avg.', zip_code_options[10],
                                                                            zip_code_options[20]]

    @app.callback(
        Output('div-table', 'children'),
        Input('df', 'data'),
        State('tabs', 'value'),
        Input('zip_codes', 'value'),
        State('location', 'value'),
        prevent_initial_call=True,
    )
    def update_table(json_df, tab, zipcodes, city):
        if tab != 'tab-summary':
            # PreventUpdate()
            PreventUpdate()
        if not zipcodes:
            return 'Please Select a Zip Code'
        print('updating summary table')

        df = pd.read_json(StringIO(json_df), orient='split')

        if 'House Price' in list(df.columns):
            df = df.drop('House Price', axis=1)

        if 'Rent Price' in list(df.columns):
            df = df.drop('Rent Price', axis=1)

        df = df.drop(columns=['Fuel Price', 'Distance (miles)', 'Time (min)', 'Annual Commute Cost'])
        df = df.set_index('Zip Code')
        # apply negative signs where appropriate
        df['Income'] = -1 * df['Income']
        df = df.map(lambda x: -1 * x)
        df.loc[f'{city} Avg.'] = df.mean()
        df.index = df.index.astype(str)
        df = df[
            ['Income', 'Annual Rent', 'Annual Food', 'Annual Fuel Cost', 'Annual Commute Time Cost', 'Federal Taxes',
             'Child Tax Credit', 'State Taxes', 'Property Taxes', 'Net Income']]  # order columns

        df_filtered = df[df.index.isin([city, *zipcodes])]
        df_filtered = df_filtered.T
        df_filtered = df_filtered[[*zipcodes]]
        df_filtered = df_filtered.reset_index(names='Value')

        num_format = Format(precision=0, scheme=Scheme.fixed, group=Group.yes, symbol=Symbol.yes)
        cols = [{"name": str(i), "id": str(i)} if i not in zipcodes
                else {"name": str(i), "id": str(i), 'type': 'numeric', 'format': num_format}
                for i in df_filtered.columns]

        table = dash_table.DataTable(
            data=df_filtered.to_dict('records'),
            columns=cols
        )

        return table
