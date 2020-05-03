import numpy as np
from poluk.forecast import recalculate


def alliance(df, col, attractiveness):

    members = [p for p in set(df[col]) if p is not None]

    for chosen in members:

        if type(attractiveness) == dict:
            adherence = attractiveness[chosen]
        else:
            adherence = attractiveness

        df[chosen+'_pct'] = np.where(df[col] == chosen,
                                     df[chosen+'_pct'] + df[[p+'_pct' for p in members if p != chosen]
                                                            ].sum(axis=1)*adherence,
                                     df[chosen+'_pct'])

    for chosen in members:
        df.loc[(df[col].notnull()) & (df[col] != chosen), chosen+'_pct'] = 0

    df = recalculate(df)

    return df
