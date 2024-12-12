from dash import html, dcc

from tabs.tax.tax_tab import input_div

filing_status = ['Single', 'Married filing jointly', 'Married filing separately', 'Head of household']
occupation = ['Engineer', 'Doctor', 'Mechanic', 'Teacher']

layout_inputs = [
    html.Div(
        className='row',
        children=[
            html.Div(
                [
                    input_div(
                        'Filing Status: ',
                        dcc.Dropdown(filing_status, filing_status[0], id='dropdown-filing-status'),
                    ),
                    input_div(
                        'Income: ',
                        dcc.Input(id='input_income', type="number", className='w-100',
                                  placeholder='Total Income', value=70000),
                    ),
                    input_div(
                        'Property Value: ',
                        dcc.Input(id='input_property', type="number", className='w-100',
                                  placeholder='If renting leave empty', ),
                    ),
                    input_div(
                        'Number of Kids: ',
                        dcc.Input(id='input_kids', type="number", className='w-100',
                                  placeholder='0', ),
                    ),
                ],
                className='col-4'
            ),
            html.Div(
                [
                    input_div(
                        'Occupation: ',
                        dcc.Dropdown(occupation, occupation[0], id='dropdown-tbd1'),
                    ),
                    input_div(
                        'TBD 2: ',
                        dcc.Input(id='input_tbd2', type="number", className='w-100'),
                    ),
                    input_div(
                        'TBD 3: ',
                        dcc.Input(id='input_tbd3', type="number", className='w-100'),
                    ),
                ],
                className='col-4'
            ),
            html.Div(
                [
                    input_div(
                        'TBD 4: ',
                        dcc.Dropdown(filing_status, filing_status[0], id='dropdown-tbd4'),
                    ),
                    input_div(
                        'TBD 5: ',
                        dcc.Input(id='input_tbd5', type="number", className='w-100'),
                    ),
                    input_div(
                        'TBD 6: ',
                        dcc.Input(id='input_tbd6', type="number", className='w-100'),
                    ),
                ],
                className='col-4'
            ),
        ]
    )
]
