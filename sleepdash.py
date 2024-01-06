from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

import plotly
import plotly.express as px
from plotly.graph_objs import *
import pandas as pd
import json

from .auth import login_required
from . import db

bp = Blueprint('sleepdash', __name__)

@bp.route("/sleepdash")
@login_required
def sleepdash():
    # grab sleepTimes for the user
    munchkin = session.get('username')

    #data = db.execute("SELECT * FROM sleepTimes WHERE munchkin=?",(munchkin,))
    #df = pd.DataFrame(data,columns=data.keys())
    df = pd.read_sql("SELECT * FROM sleep_times WHERE munchkin LIKE '%s'" %str(munchkin),con=db.engine)


    # generate a table of random times and all for test care
    #testdates = pd.date_range('2023-09-01', periods=100).strftime("%Y-%m-%d")
    #testtimes =  pd.to_datetime(np.random.choice(pd.date_range("18:00","22:00", freq='30min'), 100)).strftime("%H:%M")
    #df2 = pd.DataFrame({'id':np.arange(1,101,1),'munchkin':'testchild' ,'parent':np.random.choice(['jack', 'jill'],100), 'sleeptime': pd.to_datetime(testdates+" "+testtimes, format='%Y-%m-%d %H:%M')})
    #df2.to_sql('sleep_times',con=db.engine,if_exists='replace')
    #df = pd.read_sql("SELECT * FROM sleep_times where munchkin LIKE 'testchild'",con=db.engine)

    # process data
    df.loc[:,'sleeptime'] = pd.to_datetime(df.sleeptime, format = '%Y-%m-%d %H:%M')
    df.sort_values('sleeptime',inplace=True)

    #df.loc[:,'hour'] = df.sleeptime.dt.hour
    #df.loc[:,'minutes'] = df.sleeptime.dt.minute
    df.loc[:,'time'] = df.sleeptime.dt.hour*60+df.sleeptime.dt.minute

    # summarize data
    summary = df.groupby('parent').time.mean().reset_index()
    # convert back to hours
    summary.loc[:,'time'] = summary.time/60 # convert back to hours
    # keep hours and convert minutes to minutes for a rough time representation
    summary.loc[:,'time'] = summary.time//1+(summary.time%1*60).round(0)/100
    
    # generate graphs
    # for colors check out: https://plotly.com/python/builtin-colorscales/
    meanTime = px.bar(x=summary.parent, y=summary.time,
        labels={'x': 'Parent', 'y':'Time'},
        color_discrete_sequence= px.colors.sequential.Viridis)

    meanTime.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color':'rgba(255, 95, 31, .9)','size':14})

    longit = px.line(x=df.sleeptime.dt.date, y=df.time/60,
        labels={'x': 'Date', 'y':'Time'})
        #color_discrete_sequence= px.colors.sequential.Viridis)

    longit.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color':'rgba(255, 95, 31, .9)','size':14},
        xaxis={
            "type": 'date',
            #"tickformat": '%b/%d',
            #"dtick": 86400000.0})
        })
    longit.update_traces(line={'width':4,'color':'rgba(57, 255, 20,.9)'})

    bargraphJSON = json.dumps(meanTime, cls=plotly.utils.PlotlyJSONEncoder)
    timegraphJSON = json.dumps(longit, cls=plotly.utils.PlotlyJSONEncoder)


    #return(summary.to_json())
    graphspack = {"avgGraph":bargraphJSON,'timeGraph':timegraphJSON}
    return render_template('/sleepdash/sleepdash.html',graphs = graphspack)