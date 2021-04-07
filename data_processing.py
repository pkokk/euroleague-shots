import os
from modules.utils import *
from modules.court import *
from modules.shot import *
from modules.player import *
from modules.bin import *
from dotenv import load_dotenv, find_dotenv
# import pandas as pd

#Load .env file with parameters and get root folder
load_dotenv(find_dotenv())
ROOT_PATH = os.environ.get("ROOT_FOLDER")


#Initialize dataframe which holds all points data
points_cols= ['NUM_ANOT', 'TEAM', 'ID_PLAYER', 'PLAYER', 'ID_ACTION', 'ACTION',
       'POINTS', 'COORD_X', 'COORD_Y', 'ZONE', 'FASTBREAK', 'SECOND_CHANCE',
       'POINTS_OFF_TURNOVER', 'MINUTE', 'CONSOLE', 'POINTS_A', 'POINTS_B',
       'UTC']

players_cols= ['c','ac','na','nu','st','sl','nn','p','im']

points_df = Lib.create_empty_dataframe(points_cols)
players_df = Lib.create_empty_dataframe(players_cols)


root = Folder(ROOT_PATH)
for sub in root.get_subdirs():
    for name in sub[2]:
        if 'points.json' in name:
            points_f = File(os.path.join(sub[0],name))
            points_df_cur =  pd.DataFrame(points_f.get_content()['Rows']) 
            points_df_cur["SEASON"]=points_f.get_season()
            points_df = points_df.append(points_df_cur,sort=False)
        elif 'players' in name:
            players_f = File(os.path.join(sub[0],name))
            players_df_cur = pd.DataFrame(players_f.get_content())
            players_df_cur["SEASON"]=players_f.get_season()
            players_df = players_df.append(players_df_cur,sort=False)

players_df_agg = players_df[["c","ac","na","SEASON"]].groupby([ "c","ac","na","SEASON"])

    #break  ## to be removed for complete data

points_df['ID_ACTION'] = points_df['ID_ACTION'].apply(lambda x: x.strip())

# #one bin example
# b1 = Bin(1,{"y_bound_down":-1500,"y_bound_up":1500,"x_bound_down":-1500,"x_bound_up":1500})

# #shots list example
# shots = [Shot(shot['NUM_ANOT'],shot['ID_PLAYER'],shot['COORD_X'],shot['COORD_Y'],shot['ID_ACTION'],shot['SEASON']) for shot in df.to_dict('records')]

# avg = b1.calc_tot_avg(shots,2017)
# print(avg)
'''
# from bokeh.io import curdoc, show
# from bokeh.models import ColumnDataSource, Grid, HexTile, LinearAxis, Plot,Range1d
# from bokeh.util.hex import hexbin


# import numpy as np

# from bokeh.io import output_file, show
# from bokeh.plotting import figure
# from bokeh.transform import linear_cmap
# from bokeh.util.hex import hexbin


# xcord = [shot.x for shot in shots]
# ycord = [shot.y for shot in shots]
# x = np.array(xcord)
# y = np.array(ycord)

# bins = hexbin(x, y, 10)
# print(bins)


# c = Court()
# p = c.draw_court()

# p.hex_tile(q="q", r="r", size=10, line_color=None, source=bins)

# output_file("hex_tile.html")

# show(p)
'''











