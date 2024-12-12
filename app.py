import dash_bootstrap_components as dbc
from dash import Dash, html, Output, Input, dcc

from tabs.commute.commute_tab import render_layout_commute, register_commute_callbacks
from tabs.goods.goods_tab import register_goods_callbacks, render_layout_goods
from tabs.housing.housing_tab import render_layout_housing, register_housing_callbacks
from tabs.income.income_tab import register_income_callbacks, render_layout_income
from tabs.summary.input_layout_utils import generate_card_card
from tabs.summary.inputs import input_card
from tabs.summary.summary_tab import register_summary_callbacks, render_layout_summary
from tabs.tax.tax_tab import register_tax_callbacks, render_layout_tax
from tabs.tuition.tuition_tab import render_layout_tuition, register_tuition_callbacks

# create the dash (Flask) app with bootstrap css stylesheet
font_awesome = {
    'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
    'crossorigin': 'anonymous'
}
meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

app = Dash(
    __name__,
    meta_tags=[meta_viewport],
    external_stylesheets=[dbc.themes.FLATLY, font_awesome],
    eager_loading=True,
    suppress_callback_exceptions=True,
)
server = app.server

show = {'display': 'block', 'visibility': 'visible'}
hide = {'display': 'none', 'visibility': 'hidden'}

city_table_div = html.Div(
    className='p-4',
    children=[
        dcc.Loading(children=html.Div(id='div-city-table'))
    ]
)

# define the main layout DOM (title + tabs + div for content)
app.layout = html.Div(
    className='container pt-3 px-0',
    children=[
        html.H1(children='Cost of Living Dashboard', style={'textAlign': 'center'}),
        # hidden button to trigger callbacks after layout is rendered
        html.Button(id='run_callbacks', children='', style=hide),
        dcc.Tabs(id="tabs", value='tab-summary', children=[
            dcc.Tab(label='Summary', value='tab-summary'),
            dcc.Tab(label='Housing', value='tab-housing'),
            dcc.Tab(label='Income', value='tab-income'),
            dcc.Tab(label='Tax Burden', value='tab-tax'),
            dcc.Tab(label='Cost of Goods', value='tab-goods'),
            dcc.Tab(label='Tuition', value='tab-tuition'),
            dcc.Tab(label='Commute Cost', value='tab-commute'),
        ]),
        dcc.Store(id='df', ),  # holds main df between callbacks
        dcc.Location(id='url', refresh=False),
        input_card,  # Inputs are common across all tabs
        dcc.Loading(html.Div(id='main', className='p-0 m-0'), id='loading_main'),
        generate_card_card('City Average - Comparison Table', 'fa fa-table', city_table_div, )

    ])

# Register separate callbacks for each tab
register_summary_callbacks(app)
register_tax_callbacks(app)
register_housing_callbacks(app)
register_tuition_callbacks(app)
register_goods_callbacks(app)
register_income_callbacks(app)
register_commute_callbacks(app)


# main call back to render main div content based on selected tab
@app.callback(
    Output('run_callbacks', component_property='n_clicks'),
    Output('main', 'children'),
    Output('run_button', 'n_clicks'),
    Output('run', 'style'),
    Output('location_card', 'style'),
    Output('income_card', 'style'),
    Output('tax estimate_card', 'style'),
    Output('housing_card', 'style'),
    Output('occupation_card', 'style'),
    Output('commute_card', 'style'),
    Output('cost of goods_card', 'style'),
    Output('city_average_-_comparison_table_card', 'style'),
    Input('tabs', 'value')
)
def render_content(tab):
    print(f'Rendering Tab - {tab}')

    match tab:

        case 'tab-summary':
            return 1, render_layout_summary(), 1, show, show, show, show, hide, show, show, show, show
        case 'tab-housing':
            return 1, render_layout_housing(), None, hide, show, hide, hide, show, hide, hide, hide, hide
        case 'tab-income':
            return 1, render_layout_income(), None, hide, show, show, hide, hide, show, hide, hide, hide
        case 'tab-tax':
            return 1, render_layout_tax(), None, hide, hide, show, show, hide, hide, hide, hide, hide
        case 'tab-goods':
            return 1, render_layout_goods(), None, hide, show, hide, hide, hide, hide, hide, show, hide
        case 'tab-tuition':
            return 1, render_layout_tuition(), None, hide, show, hide, hide, hide, hide, hide, hide, hide
        case 'tab-commute':
            return 1, render_layout_commute(), None, hide, show, hide, hide, hide, hide, show, hide, hide


if __name__ == '__main__':
    app.run(debug=True)
