import numpy as np
from poluk import constants


def process(df, keep_ni=False, new=None):
    """ Tidies up a raw Electoral Calculus data set

    :param df: Pandas DataFrame from reading a raw Electoral Calculus data set
    :param keep_ni: Boolean to indicate whether Northern Ireland seats should be kept in the output
    :param new: Dict of new parties. Keys are party abbreviation. Values are the votes per seat
    :return: Pandas DataFrame that's been nicely tidied up
    """

    # Gather party codes 
    parties = list(df.columns[5:])
    
    # Name Northern Irish parties
    if len(parties) == 6:
        ni_parties = ['UUP', 'SDLP', 'DUP', 'SF', 'MIN', 'OTH']
    elif len(parties) == 8:
        ni_parties = ['UUP', 'SDLP', 'DUP', 'APNI', 'Green', 'SF', 'MIN', 'OTH']
    else:
        raise AssertionError('Wrong number of parties in raw Electoral Calculus file')
    ni_conv_dict = {parties[i]:ni_parties[i] for i in range(len(parties))}

    # Rename raw vote columns
    df.columns = list(df.columns[:5]) + [p+'_raw' for p in parties]

    # Add new parties
    if new:
        for p in new.keys():
            parties.append(p)
            df[p+'_raw'] = new[p]
            df[p+'_raw'].fillna(0, inplace=True)
            df['OTH_raw'] = (df['OTH_raw'] - new[p]).fillna(df['OTH_raw'])
    
    # Process Northern Ireland
    if keep_ni:
        for gbp in ni_conv_dict.keys():
            nip = ni_conv_dict[gbp]
            if nip not in parties:
                df[nip+'_raw'] = np.where(df['Area'] == 1, df[gbp+'_raw'], 0)
                df[gbp+'_raw'] = np.where(df['Area'] != 1, df[gbp+'_raw'], 0)
                parties.append(nip)
    else:
        df = df[df['Area'] != 1].reset_index(drop=True).copy()
        
    # Process NAT into SNP and Plaid
    for t in [('SNP',2),('Plaid',6)]:
        df[t[0]+'_raw'] = np.where(df['Area'] == t[1], df['NAT_raw'], 0)
        parties.append(t[0])
    df.drop('NAT_raw', axis=1, inplace=True)
    parties.remove('NAT')

    # Further processing
    df['Region'] = df['Area'].map(constants.region_dict)

    parties_dict = {i: parties[i] for i in range(len(parties))}
    parties_raw = [p+'_raw' for p in parties]

    df['Total_votes'] = df[parties_raw].sum(axis=1)
    df['Winner'] = np.argmax(df[parties_raw].values, axis=1)
    df['Winner'] = df['Winner'].map(parties_dict)
    df['Winner_votes'] = df[parties_raw].max(axis=1)
    df['Winner_pct'] = 100.00 * df['Winner_votes'] / df['Total_votes']

    for p in parties:
        df[p+'_pct'] = 100.00 * df[p+'_raw'] / df['Total_votes']
        df[p+'_swing_needed'] = (df['Winner_pct'] - df[p+'_pct']) / 2.00

    df['Swing_to_gain_pct'] = np.sort(df[[p+'_swing_needed' for p in parties]], axis=1)[:, 1]
    df['Majority_pct'] = df['Swing_to_gain_pct'] * 2.00

    return df
