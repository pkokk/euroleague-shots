from bokeh.plotting import figure, output_file, show
import pandas as pd
import json
# from bokeh.io import curdoc, show
# from bokeh.models import ColumnDataSource, Grid, HexTile, LinearAxis, Plot,Range1d
# from bokeh.util.hex import hexbin
import os
from modules.utils import *
from modules.court import *

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

ROOT_PATH = os.environ.get("ROOT_FOLDER")
#initialize dataframe 
df = Lib.create_empty_dataframe()

root = Folder(ROOT_PATH)
for sub in root.get_subdirs():
    if os.path.isfile(sub+'\\points.json'):
        f = File(sub+'\\points.json')
        df_cur = f.get_content_df()
        df_cur["SEASON"]=f.get_season()
        df = df.append(df_cur,sort=False)

        break
# print(df.head())
# print(df.columns)
# print(df.loc[df['SEASON']=='2017'])
# f = File('C:\\Users\\pkokkinakos\\Documents\\python_scripts\\euro\\data\\euroleague\\E2017\\FINAL FOUR\\Final\\259\\points.json')
# data = f.get_content_df()
# print(data)



# DATABASE = os.environ.get("DATABASE")
# USER = os.environ.get("USER")
# PASSWD = os.environ.get("PASSWD")
# HOST = os.environ.get("HOST")
# PORT = os.environ.get("PORT")
# con = Postgres(database=DATABASE, user=USER, passwd=PASSWD, host=HOST, port=PORT)
# rows = con.get_records(statement)

# res = []
# for row in rows:
#     record_dict = {
#         "imdbrating" : str(row[0]),
#         "numericrating" : str(row[1]),
#         "title" : str(row[2]),
#         "title_year" : row[3],
#         "imdbvotes" : row[4],
#         "genre" : str(row[5])
#     }
#     res.append(record_dict)

# # print("Operation done successfully")
# con.close()

# print(res)


# #print(df.columns)
# x= df['COORD_X']
# y= df['COORD_Y']
# print(x.max())
# print(x.min())
# print(y.max())
# print(y.min())

# from modules.court import *
# from bokeh.plotting import show

# c = Court()
# show(c.draw_court())
# print(c.get_bound_coords())

# print(df.ACTION.unique())

# print(df.loc[df['ZONE']==' '])






