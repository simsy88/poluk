import matplotlib.pyplot as plt
import numpy as np

from poluk import constants
from poluk.xy import xy

plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'


def swingometer(df, parties, colour_by='Winner', shift=None, highlight=None, highlight_label=None, title=None):

    if type(parties) != list:
        raise TypeError('Parties list must be a list')

    if len(parties) != 2:
        raise AssertionError('Parties list must contain exactly 2 parties')

    top = 10
    step = 1

    swingometer_data = xy(df, parties)
    swingometer_data = swingometer_data[swingometer_data['X'].abs() < top]

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='polar')
    ax.set_ylim(0, 13)
    ax.set_yticklabels([])
    ax.set_thetamin(-90)
    ax.set_thetamax(90)
    ax.set_theta_zero_location('S')
    ax.set_xticks(np.pi / 90 / 2 * np.linspace(90, -90, round(2 * top / step) + 1, endpoint=True))
    ax.set_xticklabels([abs(x) for x in range(-top, top + 1, step)])
    ax.scatter(np.pi * swingometer_data['X'] / top / 2, swingometer_data.Area,
               c=swingometer_data[colour_by].map(constants.colours_dict), cmap='hsv', alpha=0.75)

    if shift is not None:

        raw_votes = df[[x for x in df.columns if '_raw' in x]]
        shift_previous = 100 * raw_votes.sum() / raw_votes.sum().sum()

        swing = ((shift[parties[0]] - shift_previous[parties[0]+'_raw']) -
                 (shift[parties[1]] - shift_previous[parties[1]+'_raw'])) / 2

        plt.plot([0, np.pi * swing / top / 2], [0, 15], color='black')

    if highlight is not None:
        for seat in highlight:
            if seat not in list(swingometer_data.Name):
                continue
            seat_x_deg = swingometer_data.loc[swingometer_data.Name == seat, 'X']
            seat_x_rad = np.pi * seat_x_deg / top / 2
            seat_y = swingometer_data.loc[swingometer_data.Name == seat, 'Area']
            circle_x = seat_y * np.sin(seat_x_rad)
            circle_y = seat_y * np.cos(seat_x_rad)
            circle = plt.Circle(xy=(circle_x, -circle_y), radius=0.25, color='black', fill=False, transform=ax.transData._b)
            ax.add_artist(circle)

            if highlight_label is not None:
                if seat_x_deg.iloc[0] >= 0:
                    rot = -90 * (1 - seat_x_deg.iloc[0] / top)
                else:
                    rot = 90 * (1 + seat_x_deg.iloc[0] / top)
                ax.annotate(swingometer_data.loc[swingometer_data.Name == seat, highlight_label].iloc[0],
                            xy=(seat_x_rad, seat_y), rotation=rot, rotation_mode='anchor')

    if title:
        ax.set_title(title)
    
    plt.show()
