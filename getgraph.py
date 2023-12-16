##########################
# Import necessary modules#
##########################
import io

import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import mpld3
from io import BytesIO
import base64

def create_scatter_for_team(team,df_1,df_2):
    team_data = df_1[df_1['Name'] == team]

    color_dict = {
        1: 'limegreen',
        2: 'lime',
        3: 'lime',
        4: 'chartreuse',
        5: 'palegreen',
        6: 'lightgreen',
        7: 'aquamarine',
        8: 'aquamarine',
        9: 'turquoise',
        10: 'salmon',
        11: 'salmon',
        12: 'tomato',
        13: 'tomato',
        14: 'orangered',
        15: 'orangered',
        16: 'red'
    }

    years = team_data['Year']
    rankings = team_data['Ranking']
    ratios = team_data['FW/Total goals']
    total_goals = team_data['Total Goals Scored']
    strikers_goals = team_data['Strikers Goals Scored']

    plt.figure(figsize=(20, 6))

    plt.plot(df_2['Year'], df_2['FW/Total goals'], color='blue', linestyle='--')

    # Scatter plot and annotations setup
    scatter = plt.scatter(years, ratios, c=[color_dict.get(rank, 'lightgrey') for rank in rankings], s=100, label='Rank')
    for i, txt in enumerate(rankings):
        if txt != -1:
            plt.text(years.iloc[i], ratios.iloc[i], str(txt), fontsize=7, ha='center', va='center', fontweight='bold')


    # Function to display annotations on click
    def on_plot_hover(sel):
        if sel is None:
            plt.gca().texts[-1].set_visible(False)
        else:
            ind = sel.index
            rank = rankings.iloc[ind]
            goal = int(total_goals.iloc[ind])
            striker = int(strikers_goals.iloc[ind])
            if rank != -1:
                sel.annotation.set_text(f'{goal} goals. Strikers: {striker} goals.')
                sel.annotation.set_visible(True)
            else:
                sel.annotation.set_visible(False)


    mplcursors.cursor(hover=True).connect("add", on_plot_hover)



    plt.xlabel('Years')
    plt.ylabel('FW/Total goals')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return img

