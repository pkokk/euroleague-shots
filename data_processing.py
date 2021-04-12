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
p = c.draw_court()

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

 
totals_cols= ['2p','3p','ft','3pct','2pct','ftpct','2px','2py','3px','3py','2pTot','3pTot','ftTot','3pctTot','2pctTot','ftpctTot','player','season']

totals = Lib.create_empty_dataframe(totals_cols)

for season in seasons:
    for b in bins:
        #calculate every aggregated shot group for every player for every bin (court division)
        a = b.calc_shots(shots,season.season,players)
        #create a dataframe out of players dict
        df = pd.DataFrame.from_dict(a,orient='index')
        player_l = df.index.tolist()
        #transpose into columns the Total rows for every bin . Comparable to a case statement to create col in sql
        df['player'] = player_l
        df['2pTot'] = df['Total':]['2pTot'][0]
        df['3pTot'] = df['Total':]['3pTot'][0]
        df['ftTot'] = df['Total':]['ftTot'][0]
        df['3pctTot'] = df['Total':]['3pctTot'][0]
        df['2pctTot'] = df['Total':]['2pctTot'][0]
        df['ftpctTot'] = df['Total':]['ftpctTot'][0]
        df['season'] = season.season
        #Now drop rows with totals. We have them in cols
        df.drop(['Total'],inplace=True)
        #append every df to the totals one
        totals = totals.append(df,sort=False)

#attempted free throw data is not available, so not included in our analysis 
totals.drop(['ft', 'ftpct','ftTot','ftpctTot'], axis=1,inplace=True)
totals.reset_index(inplace=True)
#create df specific for 2 point shots
df_2p = totals.loc[totals['2px'].notnull(),['2p','2pct','2px','2py','2pctTot','player','season']]
#create df specific for 3 point shots
df_3p = totals.loc[totals['3px'].notnull(),['3p','3pct','3px','3py','3pctTot','player','season']]

#change column names to generic
df_2p.columns = ['nr_player_shots','pct_player','x_agg','y_agg','pct_total','playerid','season']
df_3p.columns = ['nr_player_shots','pct_player','x_agg','y_agg','pct_total','playerid','season']

#create pct_diff col, where the player fg pct in bin/season subtract the total pct for bin/season.
#we want to assess how good player is compared to competition
df_2p['pct_diff']=  df_2p['pct_player'] - df_2p['pct_total']
df_3p['pct_diff']=  df_3p['pct_player'] - df_3p['pct_total']

#create class for number of players shots in bin compared to players max shots in a bin
df_2p['max_player_shots_any_bin'] = df_2p.groupby(['playerid','season'])['nr_player_shots'].transform('max')
df_2p['class_nr_shots'] = 1
df_2p.loc[df_2p['nr_player_shots']/df_2p['max_player_shots_any_bin'] >= 1/3, 'class_nr_shots'] = 2
df_2p.loc[df_2p['nr_player_shots']/df_2p['max_player_shots_any_bin'] >= 2/3, 'class_nr_shots'] = 3
df_2p.drop('max_player_shots_any_bin',inplace=True,axis=1)

df_3p['max_player_shots_any_bin'] = df_3p.groupby(['playerid','season'])['nr_player_shots'].transform('max')
df_3p['class_nr_shots'] = 1
df_3p.loc[df_3p['nr_player_shots']/df_3p['max_player_shots_any_bin'] >= 1/3, 'class_nr_shots'] = 2
df_3p.loc[df_3p['nr_player_shots']/df_3p['max_player_shots_any_bin'] >= 2/3, 'class_nr_shots'] = 3
df_3p.drop('max_player_shots_any_bin',inplace=True,axis=1)


#Union 2p and 3p
final = df_2p.append(df_3p)

#Enrich final df with player name and team for every season
final = pd.merge(final,players_df[['team','playerid', 'name','season']], how='left', left_on=['playerid','season'], right_on = ['playerid','season'])

final['name'] = final['name'].str.replace(',','-')
final = final.astype({'nr_player_shots': 'int32','season': 'int32'})

#Bulk insert to Postgres
DATABASE = os.environ.get("DATABASE")
USER = os.environ.get("USER")
PASSWD = os.environ.get("PASSWD")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
con = Postgres(database=DATABASE, user=USER, passwd=PASSWD, host=HOST, port=PORT)
con.bulk_insert('shots_agg',final) 

con.close()














