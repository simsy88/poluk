import math
import numpy as np


def xy(df, parties):

    if type(parties) != list:
        raise TypeError('Parties list must be a list')

    if (len(parties) < 2) | (len(parties) > 3):
        raise AssertionError('Parties list contain either 2 or 3 parties')

    df['X'] = np.NaN
    df['Y'] = np.NaN

    df.loc[df['Winner'] == parties[0], 'X'] = -df[parties[1] + '_swing_needed']
    df.loc[df['Winner'] == parties[1], 'X'] = df[parties[0] + '_swing_needed']

    if len(parties) == 2:
        df.loc[df['Winner'].isin(parties), 'Y'] = 0
    else:
        df.loc[df['Winner'] == parties[2], 'X'] = df[parties[0] + '_swing_needed'] - df[parties[1] + '_swing_needed']
        df.loc[df['Winner'] == parties[0], 'Y'] = (df[parties[1] + '_swing_needed'] - (2 * df[parties[2] + '_swing_needed'])) / -math.sqrt(3)
        df.loc[df['Winner'] == parties[1], 'Y'] = (-df[parties[0] + '_swing_needed'] + (2 * df[parties[2] + '_swing_needed'])) / math.sqrt(3)
        df.loc[df['Winner'] == parties[2], 'Y'] = (-df[parties[0] + '_swing_needed'] - df[parties[1] + '_swing_needed']) / math.sqrt(3)

    return df
