import pandas as pd

from database.database import DB

tax_options = [
    'Federal Taxes',
    'Child Tax Credit',
    'State Taxes',
    'Property Taxes',
    'Total Taxes',
]


def add_tax_rate(df, city, income, kids, filing_status, property_value):
    tax_rates = calc_tax_data(income, kids, filing_status, property_value)

    tax_rates = tax_rates.loc[tax_rates['State Short'] == city.split(", ")[1], :]
    tax_rates = tax_rates[tax_options]


    for col in tax_rates.columns:
        df[col] = tax_rates[col].values[0]

    return df


def average_tax_rate(income, kids, filing_status, property_value):
    tax_rates = calc_tax_data(income, kids, filing_status, property_value)
    cities = ['CA','TX','IL','MA','NY','CO','NV']
    tax_rates = tax_rates.loc[tax_rates['State Short'].isin(cities), :]
    tax_rates = tax_rates[['State',*tax_options]]
    tax_rates = tax_rates.set_index('State')
    # tax_rates = tax_rates.map(lambda x: f'$ {x:,.0f}')
    tax_rates = tax_rates.T
    tax_rates = tax_rates.reset_index(names='Item')
    return tax_rates

def calc_tax_data(income, kids, filing_status, property_value):
    df = load_state_tax_rates()
    fed_taxes = calc_fed_taxes(filing_status, income)
    child_tax_credit = calc_child_tax_credit(filing_status, income, kids)

    df['Federal Taxes'] = fed_taxes
    df['Child Tax Credit'] = - child_tax_credit
    df['State Taxes'] = df['Combined Rate'].apply(lambda x: x * income)
    df['Property Taxes'] = df['Effective Tax Rate'].apply(lambda x: x * property_value)
    df['Total Taxes'] = df['Federal Taxes'] + df['Child Tax Credit'] + df['State Taxes'] + df['Property Taxes']
    return df


def load_state_tax_rates():
    db = DB()
    df = db.tax_rates()
    return df


def calc_child_tax_credit(status, income, num_child):
    income_threshold = 400_000 if status == 'Married filling jointly' else 200_000
    if income < income_threshold:
        return num_child * 2000
    return 0


def calc_fed_taxes(status, income):
    if not income:
        return 0
    db = DB()
    df = db.tax_brackets()
    df = df.set_index('Tax Rate')
    tax_bracket = df[status]

    taxes = 0
    lower_limit = 0
    for rate, limit in tax_bracket.items():
        if pd.isna(limit):  # last bracket has no limit. calc amount over previous max
            if income > lower_limit:
                amt = (income - lower_limit) * rate
            else:
                amt = 0
        else:
            if income > limit:  # fills up entire tax bracket
                amt = (limit - lower_limit) * rate
            elif (income > lower_limit) and (income <= limit):  # in bracket
                amt = (income - lower_limit) * rate
            else:
                amt = 0
            # print(f'lower = {lower_limit}, upper = {limit}, rate = {rate}, , amt = {amt}')

        taxes += amt
        lower_limit = limit
    return taxes


if __name__ == '__main__':
    for i in [40000, 41000, 70000, 71000, 95000, 96000]:
        print(i, calc_fed_taxes('Single', i))
