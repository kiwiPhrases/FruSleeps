from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

import plotly
import plotly.express as px
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
    df.loc[:,'time'] = df.hour*60+df.minutes/60

    # summarize data
    summary = df.groupby('parent').time.mean().reset_index()
    summary.loc[:,'time'] = summary.time/60

    # Create Dash Layout
    #figure=px.bar(summary,x='parent',y='time')),
    #figure=px.line(x=df.wholetime.dt.date, y=df.time/60,labels={'x': 'Date', 'y':'Time'}))
    meanTime = px.bar(summary,x='parent',y='time')
    longit = px.line(x=df.wholetime.dt.date, y=df.time/60,labels={'x': 'Date', 'y':'Time'})
    
    bargraphJSON = json.dumps(meanTime, cls=plotly.utils.PlotlyJSONEncoder)
    timegraphJSON = json.dumps(longit, cls=plotly.utils.PlotlyJSONEncoder)


    #return(summary.to_json())
    graphspack = {"avgGraph":bargraphJSON,'timeGraph':timegraphJSON}
    return render_template('/sleepdash/sleepdash.html',graphs = graphspack)