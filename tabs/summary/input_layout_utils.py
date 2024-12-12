import dash_bootstrap_components as dbc
from dash import html, dcc


def form_input(label, placeholder=None, step=1.0, options=None, multi=False):
    _id = label.lower().replace(' ', '_')
    if options:
        input_html = dcc.Dropdown(options, placeholder, multi=multi, id=_id)
    else:
        input_html = dcc.Input(type="number", value=placeholder, step=step, id=_id, className='w-100')
    label_class = 'col-4 col-form-label text-right align-self-center py-0 pl-2'
    return dbc.Row(
        [
            dbc.Label(label, html_for=_id, className=label_class),
            html.Div(className='col-8 pl-2', children=input_html),
        ],
        className='mb-1',
        id=f'input_{_id}'
    )


def generate_card(label, children, class_name='', style=None):
    return html.Div(id=label.lower() + '_card', className='card border-dark mb-3 w-100', style=style, children=[
        html.Div(className=f'card-header py-1 text-center {class_name}', children=label),
        html.Div(className='card-body py-2', children=children)
    ])


def generate_card_card(name, fa_icon, children, color='dark'):
    _id = name.lower().replace(' ', '_')
    return dbc.Card(
        id = f'{_id}_card',
        className='container px-0',
        children=[
            dbc.CardHeader(
                className=f'text-center text-white bg-{color} p-0',
                id=f'{_id}_card_header',
                children=dbc.Button(html.I(f' {name}', className=f'{fa_icon} text-white'),
                                    id={'type': 'button', 'index': _id}, size='lg',
                                    className=f'btn-block bg-{color} border-{color} text-white p-0')),

            dbc.CardBody([
                html.Div(
                    className='mb-2 px-2',
                    id=f'{_id}_card_body',
                    children=[
                        children,
                    ]
                ),

            ], className='px-0')
        ]
    )


run_button = html.Div(
    id='run',
    className='d-flex justify-content-center',
    children=[
        dcc.Loading(html.A(html.I(' Update', className='fas fa-calculator text-white'),
                           id='run_button', href='#run-calculator', n_clicks=1,
                           className='btn btn-lg bg-success border-success text-white ml-3 px-sm-5 px-2'), )

    ]
)
