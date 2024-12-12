from io import StringIO

import pandas as pd
import plotly.express as px
from dash import html, Output, Input, dcc, Dash, dash_table, State
from dash.dash_table.Format import Format, Scheme, Group, Symbol
from dash.exceptions import PreventUpdate

from database.database import DB
from tabs.summary.input_layout_utils import form_input, generate_card_card

from tabs.tax.calc_tax_rates import calc_tax_data

df = pd.DataFrame()
hover_format = {
    'Federal Taxes': ':,.0f',
    'Child Tax Credit': ':,.0f',
    'State Taxes': ':,.0f',
    'Property Taxes': ':,.0f',
    'Total Taxes': ':,.0f',
}
tax_value_options = list(hover_format.keys())


def render_layout_tax():
    db = DB()
    df = db.tax_rates()
    states = df['State'].tolist()

    map_div = html.Div(
        className='p-4',
        children=[
            html.Div(
                form_input('Graphed Value', tax_value_options[-1], options=tax_value_options),
                className='w-50  mx-auto',
            ),
            html.Hr(),
            dcc.Loading(children=html.Div(id='div-tax-graph')),
        ]
    )
    default_states = ['California', 'Texas', 'Illinois', 'Massachusetts', 'New York', 'Colorado', 'Nevada']

    table_div = html.Div(
        className='p-4',
        children=[
            html.Div(
                form_input('States', default_states, options=states, multi=True),
                className='w-75  mx-auto',
            ),
            html.Hr(),
            dcc.Loading(children=html.Div(id='div-tax-table'))
        ]
    )

    layout = html.Div(
        className='',
        children=[
            dcc.Store(id='tax_data'),
            generate_card_card('United States Map', 'far fa-map', map_div),
            generate_card_card('State Comparison Table', 'fa fa-table', table_div)
        ],
    )

    return layout


def register_tax_callbacks(app: Dash):
    @app.callback(
        Output('tax_data', 'data'),
        Input('run_callbacks', component_property='n_clicks'),
        State('tabs', 'value'),
        Input('filing_status', 'value'),
        Input('income', 'value'),
        Input('number_of_kids', 'value'),
        Input('property_value', 'value'),
    )
    def load_tax_data(_, tab, filing_status, income, kids, property_value):
        if tab != 'tab-tax':
            PreventUpdate()
        if pd.isna(income):
            income = 0
        if kids is None:
            kids = 0
        if property_value is None:
            property_value = 0

        df = calc_tax_data(income, kids, filing_status, property_value)

        return df.to_json(date_format='iso', orient='split')

    @app.callback(
        Output('div-tax-graph', 'children'),
        Input('run_callbacks', component_property='n_clicks'),
        State('tabs', 'value'),
        Input('tax_data', 'data'),
        Input('graphed_value', 'value'),
        prevent_initial_call=True,
    )
    def update_tax_map(_, tab, json_df, graphed_value):
        if tab != 'tab-tax':
            PreventUpdate()

        df = pd.read_json(StringIO(json_df), orient='split')
        fig = px.choropleth(
            df,
            locations="State Short",
            color=graphed_value,
            color_continuous_scale='Reds',
            scope="usa",
            locationmode="USA-states",
            hover_data=hover_format
        )

        return dcc.Graph(figure=fig)

    @app.callback(
        Output('div-tax-table', 'children'),
        Input('run_callbacks', component_property='n_clicks'),
        Input('tax_data', 'data'),
        State('tabs', 'value'),
        Input('states', 'value'),
        prevent_initial_call=True,
    )
    def update_tax_table(_, json_df, tab, states):
        if tab != 'tab-summary':
            PreventUpdate()

        df = pd.read_json(StringIO(json_df), orient='split')
        df = df.set_index('State')
        df = df[tax_value_options]

        df.loc[f'US Avg.'] = df.mean()

        df_filtered = df[df.index.isin(['US Avg.', *states])]
        df_filtered = df_filtered.T
        df_filtered = df_filtered.reset_index(names='Value')

        num_format = Format(precision=0, scheme=Scheme.fixed, group=Group.yes, symbol=Symbol.yes)
        cols = [{"name": str(i), "id": str(i)} if i not in ['US Avg.', *states]
                else {"name": str(i), "id": str(i), 'type': 'numeric', 'format': num_format}
                for i in df_filtered.columns]

        table = dash_table.DataTable(
            data=df_filtered.to_dict('records'),
            columns=cols  # [{"name": str(i), "id": str(i)} for i in df.columns]
        )

        return table

