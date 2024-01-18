from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

import plotly
import plotly.express as px
from plotly.graph_objs import *
import pandas as pd
import json
import numpy as np
#from matplotlib import colormaps as cms

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
    db.session.close()

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
    #https://plotly.com/python/bar-charts/
    # for colors check out: https://plotly.com/python/builtin-colorscales/
    meanTime = px.bar(x=summary.parent, y=summary.time, text_auto=True,
        labels={'x': 'Parent', 'y':'Mean Sleep Time (24h)'},
        color_discrete_sequence= px.colors.sequential.Viridis,
        title='Average Sleep Start by Parent')
    #meanTime.update_traces(base=3)
    #, text="nation" add text - add custom text
    #, text_auto=True # autotext inside bars (usually the data value)
    #fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) # more barchart customization

    meanTime.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color':'rgba(255, 95, 31, .9)','size':14},
        title_x = .5)

    longit = px.line(x=df.sleeptime.dt.date, y=(df.time/60)//1+((df.time/60)%1*60).round(0)/100,
        labels={'x': 'Date', 'y':'Time of Day (24h)'}, title='Time of Sleep')
        #color_discrete_sequence= px.colors.sequential.Viridis)

    longit.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color':'rgba(255, 95, 31, .9)','size':14},
        #title={'xanchor':'center'},
        title_x = .5,
        xaxis={
            "type": 'date',
            #"tickformat": '%b/%d',
            #"dtick": 86400000.0})
        })
    # add parent name to individual line elements
    # fix time to be in minutes so that it is more intuitive
    longit.update_traces(line={'width':4,'color':'rgba(57, 255, 20,.9)'})

    # parent pie
    pieVals = df.groupby('parent').time.count().reset_index().rename(columns = {'time':'Count'})
    pieVals.loc[:,'share'] = pieVals.Count/df.shape[0]

    # grab colors
    # the issue is that plotly grabs the first n values in its sequence
    # whereas we want something more like linspace where for n values, we take n equal steps from min to max
    cols = px.colors.sequential.Cividis_r
    cmp = [cols[int(i)] for i in np.linspace(0,len(cols)-1,2)]

    # plot
    parentPie = px.pie(pieVals, values='share', names='parent', title='Sleep Duty Distribution',hole=.4,
                       color_discrete_sequence=cmp, labels='parent')
                       #color_continuous_midpoint=0.0)
                        #color_continuous_scale= px.colors.sequential.Cividis_r
    parentPie.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_x = .5,
        font={'color':'rgba(255, 95, 31, .9)','size':14})

    # dump to JSON
    bargraphJSON = json.dumps(meanTime, cls=plotly.utils.PlotlyJSONEncoder)
    timegraphJSON = json.dumps(longit, cls=plotly.utils.PlotlyJSONEncoder)
    piegraphJSON = json.dumps(parentPie, cls=plotly.utils.PlotlyJSONEncoder)


    #return(summary.to_json())
    graphspack = {"avgGraph":bargraphJSON,'timeGraph':timegraphJSON, 'pieGraph':piegraphJSON}
    return render_template('/sleepdash/sleepdash.html',graphs = graphspack)