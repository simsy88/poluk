import matplotlib.pyplot as plt
import numpy as np
from poluk import constants

plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'


def constituency_map(df, centroids, by, highlight=None, highlight_label=None, title=None, **kwargs):

    map_data = df.merge(centroids, how='left', on='Name')

    if type(by) == str:
        by = [by]

    fig, ax = plt.subplots(1, len(by), figsize=(6*len(by), 8))
    
    if type(ax) != np.ndarray:
        ax = [ax]

    for i in range(len(by)):
        ax[i].axis('equal')
        ax[i].scatter(x=map_data.long * 85.39, y=map_data.lat * 111.03, c=map_data[by[i]].map(constants.colours_dict), **kwargs)
        ax[i].axis('off')

        xlim = ax[i].get_xlim()
        radius = (xlim[1]-xlim[0]) / 60.0
        
        if highlight is not None:
            for seat in highlight:
                if seat not in list(map_data.Name):
                    continue

                seat_x = map_data.loc[map_data.Name == seat, 'long'] * 85.39
                seat_y = map_data.loc[map_data.Name == seat, 'lat'] * 111.03

                circle = plt.Circle(xy=(seat_x, seat_y), radius=radius, color='black', fill=False)
                ax[i].add_artist(circle)

                if highlight_label is not None:
                    align = 'right'
                    ax.annotate(map_data.loc[map_data.Name == seat, highlight_label].iloc[0],
                                xy=(seat_x, seat_y), #xytext=(0.5*(seat_x-x_poll), -3),
                                textcoords='offset points', ha=align)
                    
        if title:
            ax[i].set_title(title[i])

    plt.plot()
