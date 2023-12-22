from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from FruSleeps.auth import login_required
from FruSleeps.db import get_db

bp = Blueprint('sleeplab', __name__)

@bp.route('/')
def index():
    # connect to db
    db = get_db()

    # grab the parent names
    # this assumes both parents are users in the app
    query = """
    SELECT id, username
    FROM user ORDER BY username
    """
    parents = db.execute(query).fetchall()

    return render_template('sleeplab/index.html',parents=parents)

@bp.route("/confirm",methods=("GET",'POST'))
def confirm():
    import datetime
    db = get_db()

    #if request.method=='POST':
    # grab data from the button submission
    parent = request.form['parent']
    error = None

    if error is not None:
        flash(error)

    # get and date and time of sleep
    now = datetime.datetime.now()

    zzztime = now.time().strftime("%H:%M")
    zzzdate = now.date().strftime("%Y-%m-%d")

    # grab parent id
    sleeperid = db.execute('SELECT id FROM user WHERE username = ?', (parent,)).fetchone()

    # grab values to be inserted into the database]
    # and prefill the form to confirm by the user
    #query = """
    #INSERT INTO sleepTimes (parent, sleepdate, sleeptime)
    #VALUES ({0},{1},{2})
    #""".format(parent,zzzdate, zzztime)

    #formvals = {'parent':parent,'parentid':sleeperid,'sleepdate':zzzdate,'sleeptime':zzztime}
    formvals = {'parent':parent,'sleepdate':zzzdate,'sleeptime':zzztime}
    #if request.method == 'POST':
    #    return redirect(url_for('index'))
    return render_template('sleeplab/confirm.html',formvals = formvals)
        
@bp.route("/mkrecord",methods=("GET",'POST'))        
def mkrecord():
    db = get_db()
    
    if request.method=='POST':
        #return "|".join(request.form.keys())
        db.execute('INSERT INTO sleepTimes (parent, sleepdate, sleeptime)'
                   'VALUES (?,?,?)',
                   (request.form['parent'],request.form['date'],request.form['time']))
        db.commit()
    #return redirect(url_for("index"))
    return redirect("/sleepstats")

#@bp.route("/sleepstats")
#def sleepstats():

@bp.route("/sleepstats2")
def sleepstats2():
    import pandas as pd
    db = get_db()
    query = "SELECT * FROM sleepTimes slp"
    #df2 = db.execute(query)
    df = pd.read_sql(query,con=db)
    return(df.to_html())



