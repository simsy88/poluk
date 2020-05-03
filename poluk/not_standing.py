import numpy as np
from poluk.forecast import recalculate


def not_standing(df, party, col, standing_down_label=False):

    if standing_down_label:
        mask = df[col]
    else:
        mask = ~df[col]

    df.loc[mask, party+'_pct'] = 0

    df = recalculate(df)

    return df
