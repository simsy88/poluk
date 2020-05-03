import math

import matplotlib.pyplot as plt

from poluk import constants
from poluk.xy import xy

plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'


def battleground(df, parties, colour_by='Winner', shift=None, highlight=None, highlight_label=None, title=None):
    """
    Draws a three-way battleground diagram

    :param df: DataFrame of seat data
    :param parties: Parties to diagram
    :param colour_by: Column to use for colour of each point
    :param shift: A dictionary of polling use to show the shift
    :param highlight: List of seat names to highlight
    :param highlight_label: Column name to use for labelling highlighted seats. Usually 'Name' or 'MP'
    :return:
    """

    if type(parties) != list:
        raise TypeError('Parties list must be a list')

    if len(parties) != 3:
        raise AssertionError('Parties list must contain exactly 3 parties')

    battleground_data = xy(df, parties)

    limits = max(battleground_data.X.abs().max(), battleground_data.Y.abs().max())

    plt.figure(figsize=(8, 8))
    plt.scatter(x=battleground_data.X, y=battleground_data.Y,
                c=battleground_data[colour_by].map(constants.colours_dict))
    plt.xlim((-limits, limits))
    plt.ylim((-limits, limits))
    plt.plot([0, 0], [0, limits], color='black')
    plt.plot([0, limits], [0, -limits / math.sqrt(3)], color='black')
    plt.plot([0, -limits], [0, -limits / math.sqrt(3)], color='black')

    fig = plt.gcf()
    ax = fig.gca()

    x_poll = 0
    if shift is not None:

        raw_votes = df[[x for x in df.columns if '_raw' in x]]
        shift_previous = 100 * raw_votes.sum() / raw_votes.sum().sum()

        p0_change = shift[parties[0]] - shift_previous[parties[0]+'_raw']
        p1_change = shift[parties[1]] - shift_previous[parties[1]+'_raw']
        p2_change = shift[parties[2]] - shift_previous[parties[2]+'_raw']
        x_poll = (p0_change - p1_change) / 2
        y_poll = ((p2_change - p1_change) - (p0_change - p2_change)) / 2 / math.sqrt(3)

        plt.plot([0 + x_poll, 0 + x_poll], [0 + y_poll, 2 * limits + y_poll], color='lightgrey')
        plt.plot([0 + x_poll, 2 * limits + x_poll], [0 + y_poll, (-2 * limits / math.sqrt(3)) + y_poll],
                 color='lightgrey')
        plt.plot([0 + x_poll, -2 * limits + x_poll], [0 + y_poll, (-2 * limits / math.sqrt(3)) + y_poll],
                 color='lightgrey')

        plt.arrow(0, 0, x_poll, y_poll, head_width=1, overhang=0.5, length_includes_head=True, color='lightgrey')

    if highlight is not None:
        for seat in highlight:
            if seat not in list(battleground_data.Name):
                continue

            seat_x = battleground_data.loc[battleground_data.Name == seat, 'X']
            seat_y = battleground_data.loc[battleground_data.Name == seat, 'Y']

            circle = plt.Circle(xy=(seat_x, seat_y), radius=0.75, color='black', fill=False)
            ax.add_artist(circle)

            if highlight_label is not None:

                if seat_x.iloc[0] < x_poll:
                    align = 'right'
                else:
                    align = 'left'
                ax.annotate(battleground_data.loc[battleground_data.Name == seat, highlight_label].iloc[0],
                            xy=(seat_x, seat_y), xytext=(0.5*(seat_x-x_poll), -3),
                            textcoords='offset points', ha=align)

    plt.title(title)

    plt.show()
