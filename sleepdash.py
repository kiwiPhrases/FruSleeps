from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

import plotly
import plotly.express as px
from plotly.graph_objs import *
import pandas as pd
import json

from FruSleeps.auth import login_required
from FruSleeps.db import get_db

bp = Blueprint('sleepdash', __name__)

@bp.route("/sleepdash")
def sleepdash():
    # grab sleepTimes for the user
    munchkin = session.get('username')
    db = get_db()
    #data = db.execute("SELECT * FROM sleepTimes WHERE munchkin=?",(munchkin,))
    #df = pd.DataFrame(data,columns=data.keys())
    df = pd.read_sql("SELECT * FROM sleepTimes WHERE munchkin LIKE '%s'" %str(munchkin),con=db)

    # process data
    df.loc[:,'wholetime'] = pd.to_datetime(df.sleepdate+" "+df.sleeptime, format = '%Y-%m-%d %H:%M')

    df.loc[:,'hour'] = df.wholetime.dt.hour
    df.loc[:,'minutes'] = df.wholetime.dt.minute
    df.loc[:,'time'] = df.hour*60+df.minutes

    # summarize data
    summary = df.groupby('parent').time.mean().reset_index()
    summary.loc[:,'time'] = summary.time/60
    
    # generate graphs
    # for colors check out: https://plotly.com/python/builtin-colorscales/
    meanTime = px.bar(x=summary.parent, y=summary.time,
        labels={'x': 'Parent', 'y':'Time'},
        color_discrete_sequence= px.colors.sequential.Viridis)

    meanTime.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color':'rgba(255, 95, 31, .9)','size':14})

    longit = px.line(x=df.wholetime.dt.date, y=df.time/60,
        labels={'x': 'Date', 'y':'Time'})
        #color_discrete_sequence= px.colors.sequential.Viridis)

    longit.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color':'rgba(255, 95, 31, .9)','size':14},
        xaxis={
            "type": 'date',
            "tickformat": '%b %d, %y',
            "dtick": 86400000.0})
    longit.update_traces(line={'width':4,'color':'rgba(57, 255, 20,.9)'})

    bargraphJSON = json.dumps(meanTime, cls=plotly.utils.PlotlyJSONEncoder)
    timegraphJSON = json.dumps(longit, cls=plotly.utils.PlotlyJSONEncoder)


    #return(summary.to_json())
    graphspack = {"avgGraph":bargraphJSON,'timeGraph':timegraphJSON}
    return render_template('/sleepdash/sleepdash.html',graphs = graphspack)