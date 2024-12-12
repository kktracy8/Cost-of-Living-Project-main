import plotly.express as px
from dash import html, Output, Input, dcc, Dash, State
from dash.exceptions import PreventUpdate

from database.database import DB
from tabs.map_utils import get_mapbox_center
from tabs.tuition.utils import (k12_spending_by_city,
                                k12_spending_by_zipcode,
                                college_tuition_by_city,
                                college_tuition_by_zipcode)

WIDTH = "800px"


def input_div(label, element):
    return html.Div(
        className='row p-1',
        children=[
            html.Label(label, id=f'label-{label}', className='col-5'),
            html.Div(element, className='col-7')
        ]
    )


def render_layout_tuition():
    return html.Div(
        [
            html.Div(
                className='row',
                children=[
                    html.H4('K12 Education Spending'),
                    dcc.Loading(html.Div(
                        dcc.Graph(id='k12-spending-map', style={'height': '600px', 'width': WIDTH}, ),
                        className='container border my-2 mx-auto d-flex justify-content-center'),
                    ),
                    html.Div(
                        dcc.Graph(id='k12-spending-bar-chart', style={'width': WIDTH}, ),
                        className='container border my-2 mx-auto d-flex justify-content-center'),
                    html.H4('College Tuition'),
                    html.Div(
                        dcc.Graph(id='college-tuition-map', style={'height': '600px', 'width': WIDTH}),
                        className='container border my-2 mx-auto d-flex justify-content-center'
                    ),
                    html.Div(
                        dcc.Graph(id='college-tuition-bar-chart', style={'width': WIDTH}, ),
                        className='container border my-2 mx-auto d-flex justify-content-center')
                ]
            ),
        ],
        className='container',
        style={'height': '700px'},
    )


def register_tuition_callbacks(app: Dash):
    @app.callback(
        Output('k12-spending-map', 'figure'),
        Output('k12-spending-bar-chart', 'figure'),
        Output('college-tuition-map', 'figure'),
        Output('college-tuition-bar-chart', 'figure'),
        Input('run_callbacks', component_property='n_clicks'),
        State('tabs', 'value'),
        Input('location', 'value')
    )
    def update_graph(_, tab, location):
        if tab != 'tab-tuition':
            PreventUpdate()

        # added because turned to multi input
        # location = location[0]

        mapbox_center = get_mapbox_center(location)
        loc_toks = location.split(",")
        city = loc_toks[0].strip()
        state = loc_toks[1].strip()

        db = DB()
        geo_json = db.get_geo_json(location)
        # =================== K12 Spending =====================
        k12_spending_by_zip_df = k12_spending_by_zipcode(city, state)
        min_val_zip = k12_spending_by_zip_df['total_spending_per_pupil'].min()
        max_val_zip = k12_spending_by_zip_df['total_spending_per_pupil'].max()

        fig1 = px.choropleth_mapbox(
            k12_spending_by_zip_df,
            geojson=geo_json,
            locations='zip_code',
            color='total_spending_per_pupil',
            color_continuous_scale='Greens',
            range_color=(min_val_zip, max_val_zip),
            featureidkey="properties.ZCTA5CE10",
            mapbox_style="open-street-map",
            title="Total Spending Per Pupil (USD) by Zip Code"
        )

        fig1.update_layout(mapbox_zoom=9, mapbox_center=mapbox_center)

        k12_spending_by_city_df = k12_spending_by_city()

        fig2 = px.bar(k12_spending_by_city_df,
                      x="mean_total_spending_per_pupil",
                      y="location",
                      orientation='h',
                      height=400,
                      title=f'Mean Total Spending Per Pupil (USD) by City'
                      )
        # =================== College Tuition =====================

        college_tuition_by_zip_df = college_tuition_by_zipcode(city, state)
        min_val_zip = college_tuition_by_zip_df['avg_cost_of_attendance'].min()
        max_val_zip = college_tuition_by_zip_df['avg_cost_of_attendance'].max()

        fig3 = px.choropleth_mapbox(
            college_tuition_by_zip_df,
            geojson=geo_json,
            locations='zip_code',
            color='avg_cost_of_attendance',
            color_continuous_scale='Turbo',
            range_color=(min_val_zip, max_val_zip),
            featureidkey="properties.ZCTA5CE10",
            mapbox_style="open-street-map",
            title="Mean Cost of College (USD) Attendance by Zip Code"
        )

        fig3.update_layout(mapbox_zoom=7, mapbox_center=mapbox_center)

        college_tuition_by_city_df = college_tuition_by_city()

        fig4 = px.bar(college_tuition_by_city_df,
                      x='avg_cost_of_attendance',
                      y="location",
                      orientation='h',
                      height=400,
                      title=f'Mean Cost of College (USD) Attendance by City'
                      )

        return fig1, fig2, fig3, fig4
