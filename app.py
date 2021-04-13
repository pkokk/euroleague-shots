from flask import Flask, render_template
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Select,LinearColorMapper,ColorBar
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models.callbacks import CustomJS
import psycopg2
import random
from modules.court import *
from bokeh.palettes import Turbo256
from bokeh.transform import linear_cmap
from dotenv import load_dotenv, find_dotenv
import os

app = Flask(__name__)
DATABASE = os.environ.get("DATABASE")
USER = os.environ.get("USER")
PASSWD = os.environ.get("PASSWD")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

@app.route('/')
def index():


    def selecteddata():
        con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWD, host=HOST, port=PORT)
        # print("Database opened successfully")
        cur = con.cursor()
        statement = """ 
        select 

        classnrshots,
        xagg,
        nr_player_shots,
        yagg,
        pcttotal,
        pctplayer,
        season,
        pctdiff,
        playername,
        playerid,
        team

        from shots_agg 
        """
        cur.execute(statement)
        rows = cur.fetchall()

        res = []
        for row in rows:
            record_dict = {
                "classnrshots" : row[0],
                "xagg" : row[1],
                "nr_player_shots" : row[2],
                "yagg" : row[3],
                "pcttotal" : row[4],
                "pctplayer" : row[5],
                "season" : row[6],
                "pctdiff" : row[7],
                "playername" : str(row[8]),
                "playerid" : str(row[9]),
                "team" : str(row[10])
            }
            res.append(record_dict)



        print("Data loaded")
        con.close()
        return res

    src = selecteddata()

    seasons_list = sorted(list(set([str(item['season']) for item in src])))
    players_list = sorted(list(set([item['playername'] for item in src])))

    controls = {
        "playername": Select(title="Player", value="ALL", options=players_list),
        "season": Select(title="Season", value="2017", options=seasons_list)
    }

    controls_array = controls.values()
    source = ColumnDataSource()

    callback = CustomJS(args=dict(source=source, controls=controls), code="""
        if (!window.full_data_save) {
            window.full_data_save = JSON.parse(JSON.stringify(source.data));
        }
        var full_data = window.full_data_save;
        var full_data_length = full_data.x.length;
        var new_data = { x: [], y: [], color : [], size : [], nr_player_shots : [], pctplayer : [], playername : []}
        for (var i = 0; i < full_data_length; i++) {
            if (full_data.x[i] === null || full_data.y[i] === null || full_data.playername[i] === null)
                continue;
            if (
                ( full_data['playername'][i] == controls.playername.value) &&
                ( full_data['season'][i] == controls.season.value)
                
            ) { 
                Object.keys(new_data).forEach(key => new_data[key].push(full_data[key][i]));
            }
        }
        
        source.data = new_data;
        source.change.emit();
    """)

    color_mapper = LinearColorMapper(palette=Turbo256,low=min([float(d['pctdiff']) for d in src]),high=max([float(d['pctdiff']) for d in src]))

    c = Court(tooltips=[("Nr FG", "@nr_player_shots"), ("Pct", "@pctplayer")])
    fig = c.draw_court()
    fig.circle(x="x", y="y", source=source, size="size",  line_color=None, color={'field': 'color', 'transform': color_mapper})
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12)
    fig.add_layout(color_bar, 'right')

    source.data = dict(
        x = [float(d['xagg']) for d in src],
        y = [float(d['yagg']) for d in src],
        color = [float(d['pctdiff']) for d in src],
        size = [int(d['classnrshots'])*3 for d in src],
        nr_player_shots = [float(d['nr_player_shots']) for d in src],
        pctplayer = [float(d['pctplayer'])*100.0 for d in src],
        playername = [d['playername'] for d in src],
        season = [int(d['season']) for d in src]

    )
    

    for single_control in controls_array:
        single_control.js_on_change('value', callback)

    inputs_column = column(*controls_array, width=220, height=300)
    layout_row = column ([ inputs_column, fig ])

    script, div = components(layout_row)
    return render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    )


if __name__ == "__main__":
    app.run(debug=True)

