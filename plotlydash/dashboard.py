from dash import Dash
from dash import dash_table
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from bs4 import BeautifulSoup


from FruSleeps.db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

def init_dashboard(server):

    #dbi = db.get_db()
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=server,
        url_base_pathname = "/sleepstats/",
        #routes_pathname_prefix='/sleepstats/',
        external_stylesheets=[
            '/static/styles.css',
        ]
    )

    # grab data
    #df2 = db.execute("SELECT * FROM sleepTimes")
    #db = get_db()
    with server.app_context():
        #https://flask.palletsprojects.com/en/2.3.x/appcontext/
        db = get_db()
        df = pd.read_sql("SELECT * FROM sleepTimes",con=db)

    # process data
    df.loc[:,'wholetime'] = pd.to_datetime(df.sleepdate+" "+df.sleeptime, format = '%Y-%m-%d %H:%M')

    df.loc[:,'hour'] = df.wholetime.dt.hour
    df.loc[:,'minutes'] = df.wholetime.dt.minute
    df.loc[:,'time'] = df.hour*60+df.minutes/60
    #df.loc[:,'sleeptime'] = pd.to_datetime(df.sleeptime, format = "%H:%M")
    #df.loc[:,'hour'] = df.sleeptime.dt.hour
    #df.loc[:,'minutes'] = df.sleeptime.dt.minutes

    # summarize data
    summary = df.groupby('parent').time.mean().reset_index()
    summary.loc[:,'time'] = summary.time/60
    #df.loc[:,'sleeptime'] = df.loc[:,'sleeptime'] - df.loc[:,'sleeptime'].dt.normalize()
    #print(df2)
    #df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

    # Create Dash Layout
    dash_app.layout = html.Div([
            html.Div(children="Freya's Sleeping Stats"),
            #dash_table.DataTable(data=df.to_dict('records'), page_size=10),
            dcc.Graph(figure=px.bar(summary,x='parent',y='time')),
            dcc.Graph(figure=px.line(x=df.wholetime.dt.date, y=df.time/60,labels={'x': 'Date', 'y':'Time'}))
        ],
        id='dash-container')
    meanTime = dcc.Graph(figure=px.bar(summary,x='parent',y='time'))
    longit = dcc.Graph(figure=px.line(x=df.wholetime.dt.date, y=df.time/60,labels={'x': 'Date', 'y':'Time'}))
    
    #soup = BeautifulSoup(dash_app.index(), 'html.parser')
    #footer = soup.footer
    #return render_template('sleepstats.html', footer=footer)

    return("Hello world!")
    #return dash_app.server
    #with server.app_context():
    #    outtempl =  render_template('sleeplab/sleepstats.html',charts={"meanTime":meanTime,'Longitude':longit})

    #return outtempl