import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, Output, Input, dcc, Dash, dash_table, State
from dash.exceptions import PreventUpdate
from io import StringIO

from tabs.summary.input_layout_utils import generate_card_card

from database.database import DB

# df = pd.DataFrame()

hover_format = {
    'Occupation': None,
    'Annual Mean Income': ':.0f',
    'Location': ':.0f',
}


def input_div(label, element):
    return html.Div(
        className='row p-1',
        children=[
            html.Label(label, id=f'label-{label}', className='col-5'),
            html.Div(element, className='col-7')
        ]
    )


def render_layout_income():
    # global df
    # db = DB()
    # df = db.read_income_comparison()

    # Get list of unique occupations
    # occupations = sorted(df.src_occ_title.unique())

    # Adding similar format to Summary tab using cards
    graph_div = html.Div(
        className='p-4',
        children=[
            html.H5(
                'Note: this comparison is based on Bureau of Labor Statistics (BLS) average income for the occupation(s) selected above.'),
            html.Div(
                dcc.Graph(id='graph-income'),
                className='container border my-2'
            ),
            #html.Hr(),
            #dcc.Loading(children=html.Div(id='div-tax-graph')),
        ]
    )

    table_div = html.Div(
        className='p-4',
        children=[
            #html.Hr(),
            html.H5(
                'Note: this comparison is based on household income entered above, and shows the estimated adjusted income by city for the selected occupation(s).'),
            dcc.Loading(children=html.Div(id='div-income_table'))
        ]
    )

    layout = html.Div(
        className='',
        children=[
            # dcc.Store(id='df_income', data=df.to_json(date_format='iso', orient='split')),
            generate_card_card('Income Comparison by City & Occupation', 'fas fa-chart-bar', graph_div),
            generate_card_card('Custom Income Comparison Table', 'fa fa-table', table_div)
        ],
    )

    return layout


def register_income_callbacks(app: Dash):
    @app.callback(
        Output('div-income_table', 'children'),
        # Output('df_income', 'data'),
        Input('run_callbacks', component_property='n_clicks'),
        # State('df_income', 'data'),
        State('tabs', 'value'),
        Input('income', 'value'),
        Input('current_occupation(s)', 'value'),
        Input('location', 'value'),
    )
    def update_df(_, tab, income ,occupation1, location):
        if tab != 'tab-income':
            PreventUpdate()
        if pd.isna(income):
            income = 0
        print('updating income df')
        db = DB()
        df = db.read_income_comparison()
        # df = pd.read_json(StringIO(json_df), orient='split')

        # Calculate custom income based on difference of relative occupation means
        df['Avg Income Dif'] = ((df['dest_a_mean'] - df['src_a_mean']) / df['src_a_mean'])
        df['Income Estimate'] = df['Avg Income Dif'].apply(lambda x: (1 + x) * income)
        df['Income Input'] = df['Avg Income Dif'].apply(lambda x: (x - x) + income)
        # return df.to_json(date_format='iso', orient='split')


        # added because changed to multi input
        # location = location[0]

        # df = pd.read_json(StringIO(json_df), orient='split')
        # Filter for occupations and leave out current location
        # df_filtered = df[(df.src_city == location) & (df.dest_occ_title.isin(list(occupation1))) & (
        #             df.src_city != df.dest_city)]

        # Added back current city for Summary tab
        df_filtered = df[(df.src_city == location) & (df.dest_occ_title.isin(list(occupation1))) & (
                df.src_city != df.dest_city)]
        # Select columns to view in the dash table
        df_filtered = df_filtered[
            ['src_city', 'dest_city', 'src_a_mean', 'dest_a_mean', 'a_mean_dif', 'Income Estimate',
             'Avg Income Dif', 'Income Input']].copy()

        # Aggregate results for selected occupations
        df_grouped = (df_filtered.groupby('dest_city')
                      .agg(Total_Mean_Current=('src_a_mean', 'sum'),
                           Total_Mean_Dest=('dest_a_mean', 'sum'),
                           Avg_Income_Dif=('Avg Income Dif', 'mean'),
                           Income_Input=('Income Input', 'mean'),
                           Total_Estimated_Income=('Income Estimate', 'sum'), )).reset_index()
        # Test adding new income calculation on grouped data table
        df_grouped['Total_Est_Income2'] = (df_grouped['Income_Input'] *
                                           (1 + ((df_grouped['Total_Mean_Dest'] -
                                                  df_grouped['Total_Mean_Current']) /
                                                 df_grouped['Total_Mean_Current'])))

        # Select final subset of columns needed for dash table
        df_grouped = df_grouped.rename(
            columns={'dest_city': 'Comparison City', 'Avg_Income_Dif': 'Avg. Income Difference (%)',
                     'Total_Est_Income2': 'Estimated Household Income'})
        df_grouped = df_grouped[
            ['Comparison City', 'Avg. Income Difference (%)', 'Estimated Household Income']].copy()

        # Column formatting
        df_grouped['Avg. Income Difference (%)'] = df_grouped['Avg. Income Difference (%)'].map('{:.2%}'.format)
        df_grouped['Estimated Household Income'] = df_grouped['Estimated Household Income'].map('${:,.2f}'.format)
        cols = [{"name": str(i), "id": str(i)}
                for i in df_grouped.columns]

        table = dash_table.DataTable(
            data=df_grouped.to_dict('records'),
            columns=cols
        )
        return table



    @app.callback(
        Output('graph-income', 'figure'),
        Input('run_callbacks', component_property='n_clicks'),
        State('tabs', 'value'),
        Input('location', 'value'),
        Input('current_occupation(s)', 'value'),
    )
    def update_graph(_,tab, location, occupation1):
        # print(tab)
        if tab != 'tab-income':
            PreventUpdate()

        # added because changed to multi input
        # location = location[0]

        # added to fix issue when enter tab from commute cost tab with missing data -chris
        db = DB()
        df = db.read_income_comparison()
        dff = df[(df.src_city == location) & (df.dest_occ_title.isin(occupation1))]
        fig = px.bar(dff, x='dest_a_mean',
                     y='dest_city',
                     orientation='h',
                     color='src_occ_title',
                     color_discrete_sequence=px.colors.qualitative.Safe,
                     # title='Annual Mean Income by Location',
                     text_auto=True,
                     labels={'dest_a_mean': 'Annual Mean Income',
                             'dest_city': 'City',
                             'src_occ_title': 'Occupation'})

        # Compute totals for household income based on selected occupations
        dfft = dff.groupby("dest_city").agg({'dest_a_mean': 'sum'})
        fig.add_trace(go.Scatter(
            x=dfft['dest_a_mean'],
            y=dfft.index,
            text=dfft['dest_a_mean'],
            mode='text',
            textposition='middle right',
            textfont=dict(size=12),
            fillcolor="#ff7f0e",
            texttemplate="%{x:$,.3s}",
            hovertext='Total Income',
            showlegend=False
        ))

        fig.update_layout(yaxis={'categoryorder': 'total ascending'},
                          scene_xaxis=dict(separatethousands=True),
                          xaxis_tickprefix='$',
                          xaxis_tickformat='.3s',
                          )
        return fig

    # Adding data table for custom income comparison
    # @app.callback(
    #     Output('div-income_table', 'children'),
    #
    #     Input('df_income', 'data'),
    #     State('tabs', 'value'),
    #     Input('current_occupation(s)', 'value'),
    #     Input('location', 'value'),
    #     prevent_initial_call=True,
    #
    # )
    # def update_table(json_df, tab, occupation1, location):
    #     if tab != 'tab-income':
    #         PreventUpdate()
    #
    #     print('updating income table')
    #     # added because changed to multi input
    #     # location = location[0]
    #
    #     df = pd.read_json(StringIO(json_df), orient='split')
    #     print(df)
    #     # Filter for occupations and leave out current location
    #     # df_filtered = df[(df.src_city == location) & (df.dest_occ_title.isin(list(occupation1))) & (
    #     #             df.src_city != df.dest_city)]
    #
    #     # Added back current city for Summary tab
    #     df_filtered = df[(df.src_city == location) & (df.dest_occ_title.isin(list(occupation1))) & (
    #             df.src_city != df.dest_city)]
    #     print(df_filtered)
    #     # Select columns to view in the dash table
    #     df_filtered = df_filtered[
    #         ['src_city', 'dest_city', 'src_a_mean', 'dest_a_mean', 'a_mean_dif', 'Income Estimate',
    #          'Avg Income Dif', 'Income Input']].copy()
    #
    #     # Aggregate results for selected occupations
    #     df_grouped = (df_filtered.groupby('dest_city')
    #                   .agg(Total_Mean_Current=('src_a_mean', 'sum'),
    #                        Total_Mean_Dest=('dest_a_mean', 'sum'),
    #                        Avg_Income_Dif=('Avg Income Dif', 'mean'),
    #                        Income_Input=('Income Input', 'mean'),
    #                        Total_Estimated_Income=('Income Estimate', 'sum'), )).reset_index()
    #     print(df_grouped)
    #     # Test adding new income calculation on grouped data table
    #     df_grouped['Total_Est_Income2'] = (df_grouped['Income_Input'] *
    #                                        (1 + ((df_grouped['Total_Mean_Dest'] -
    #                                               df_grouped['Total_Mean_Current']) /
    #                                              df_grouped['Total_Mean_Current'])))
    #
    #     # Select final subset of columns needed for dash table
    #     df_grouped = df_grouped.rename(
    #         columns={'dest_city': 'Comparison City', 'Avg_Income_Dif': 'Avg. Income Difference (%)',
    #                  'Total_Est_Income2': 'Estimated Household Income'})
    #     df_grouped = df_grouped[
    #         ['Comparison City', 'Avg. Income Difference (%)', 'Estimated Household Income']].copy()
    #
    #     # Column formatting
    #     df_grouped['Avg. Income Difference (%)'] = df_grouped['Avg. Income Difference (%)'].map('{:.2%}'.format)
    #     df_grouped['Estimated Household Income'] = df_grouped['Estimated Household Income'].map('${:,.2f}'.format)
    #     print(df_grouped)
    #     cols = [{"name": str(i), "id": str(i)}
    #             for i in df_grouped.columns]
    #
    #     table = dash_table.DataTable(
    #         data=df_grouped.to_dict('records'),
    #         columns=cols
    #     )
    #     return table
