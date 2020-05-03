import numpy as np


def recalculate(df):

    parties = [p[:-4] for p in [x for x in df.columns if '_raw' in x]]
    parties_dict = {i: parties[i] for i in range(len(parties))}

    df['Winner_forecast'] = np.argmax(df[[p + '_pct' for p in parties]].values, axis=1)
    df['Winner_forecast'] = df['Winner_forecast'].map(parties_dict)
    df['Winner_forecast_pct'] = np.max(df[[p + '_pct' for p in parties]].values, axis=1)
    for x in parties:
        df[x + '_swing_after_forecast_needed'] = (df['Winner_forecast_pct'] - df[x + '_pct']) / 2
    df['Swing_to_gain_after_forecast_pct'] = np.sort(df[[x + '_swing_after_forecast_needed' for x in parties]
                                                        ], axis=1)[:, 1]
    df['Majority_after_forecast_pct'] = df['Swing_to_gain_after_forecast_pct'] * 2
    df['Probability'] = 1 - (0.5 * 0.2 ** (df['Majority_after_forecast_pct'] / 6))
    df['In_danger'] = df[['Swing_to_gain_pct', 'Swing_to_gain_after_forecast_pct']].min(axis=1) < 5

    return df


def forecast(df, polling_list):
    """

    :param df: A Pandas DataFrame
    :param polling_list: List of tuples. Tuple element 1 is list of Area numbers to compare.
                            Tuple element 2 is list of Area numbers to apply in. Tuple element 3 is polling dict
    :return: An updated Pandas DataFrame
    """

    for t in polling_list:

        compare_regions = t[0]
        apply_regions = t[1]
        polling = t[2]

        raw_votes = df.loc[df.Area.isin(compare_regions), [x for x in df.columns if '_raw' in x]].copy()
        last_election = 100 * raw_votes.sum() / raw_votes.sum().sum()

        for p in polling.keys():
            df.loc[df.Area.isin(apply_regions), p+'_pct'] += (polling[p] - last_election[p+'_raw'])

    df = recalculate(df)

    return df
