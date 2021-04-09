import os
from modules.utils import *
from modules.court import *
from modules.shot import *
from modules.player import *
from modules.bin import *
from modules.season import *
from dotenv import load_dotenv, find_dotenv
import numpy as np
# import pandas as pd

#Load .env file with parameters and get root folder
load_dotenv(find_dotenv())
ROOT_PATH = os.environ.get("ROOT_FOLDER")


#Initialize dataframes
points_cols= ['NUM_ANOT', 'TEAM', 'ID_PLAYER', 'PLAYER', 'ID_ACTION', 'ACTION',
       'POINTS', 'COORD_X', 'COORD_Y', 'ZONE', 'FASTBREAK', 'SECOND_CHANCE',
       'POINTS_OFF_TURNOVER', 'MINUTE', 'CONSOLE', 'POINTS_A', 'POINTS_B',
       'UTC']

players_cols= ['c','ac','na','nu','st','sl','nn','p','im']

#Create empty dataframes for points and players
points_df = Lib.create_empty_dataframe(points_cols)
players_df = Lib.create_empty_dataframe(players_cols)


root = Folder(ROOT_PATH)

#Loop over source data and create 2 dataframes: point data and players
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
            
            

        

points_df['ID_ACTION'] = points_df['ID_ACTION'].apply(lambda x: x.strip())
points_df['ID_PLAYER'] = points_df['ID_PLAYER'].apply(lambda x: x.strip())


players_df.rename(columns={"c":"team","ac":"playerid","na":"name","SEASON":"season"},inplace=True)
players_df['playerid'] = players_df['playerid'].apply(lambda x: x.strip())

#Instantiate all players 
players = [ Player(player[0],player[1]) for player in players_df.groupby(["playerid","name"])["playerid","name"].apply(list).to_dict()]

#Instantiate all seasons
seasons = [Season(season) for season in players_df.season.unique()]

#Construct team - player dict for every season
for season in seasons:
    season.construct_team_player_dict(players_df)


#one bin example
# b1 = Bin(1,{"y_bound_down":-1500,"y_bound_up":1500,"x_bound_down":-1500,"x_bound_up":1500})

##Instantiate all shots
#A unique Id for shot would be playerID + Timestamp of shot
shots = [Shot(shot['ID_PLAYER']+str(shot['UTC']),shot['ID_PLAYER'],shot['COORD_X'],shot['COORD_Y'],shot['ID_ACTION'],shot['SEASON']) for shot in points_df.to_dict('records')]

#Create court
c = Court()
# p = c.draw_court()

#Choose binning dimensions of court
bins_l_dim = 10
bins_h_dim = 10

court_bounds = c.get_bound_coords()
xstep = (-court_bounds['x_low'] + court_bounds['x_up'])/bins_l_dim
ystep = (-court_bounds['y_low'] + court_bounds['y_up'])/bins_h_dim

binid=1
bins = []

#We instantiate all bins of the court. We divide the court in bins_l_dim * bins_h_dim boxes and below are the boundary dims / as well as the binid
for i in np.arange(court_bounds['x_low'],court_bounds['x_up'], xstep):
    for j in np.arange(court_bounds['y_low'],court_bounds['y_up'], ystep):
        bin_def = { "x_bound_up": i+xstep
                    ,"y_bound_up": j+ystep
                    ,"x_bound_down" : i
                    ,"y_bound_down" : j
                    }
        bins.append(Bin(binid,bin_def))
        # print(i,j,j,i+xstep)
        binid+=1
print(bins[0].x_bound_up)
print(bins[0].y_bound_up)
print(bins[0].x_bound_down)
print(bins[0].y_bound_down)

tot = {}
for season in seasons:
    tot[season.get_int()] = {  b.binid :b.calc_shots(shots,season.get_int(),players)  for b in bins }

print(tot[2017][66])

# for item in tot:
#     print(item)
        



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

show(p)
'''











