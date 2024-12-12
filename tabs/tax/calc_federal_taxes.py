import pandas as pd


def calc_fed_taxes(db, status, income):
    if not income:
        return 0
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
                amt = (limit - income) * rate
            else:
                amt = 0
        taxes += amt
        lower_limit = limit
    return taxes
