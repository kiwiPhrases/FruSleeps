from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from FruSleeps.auth import login_required
from FruSleeps.db import get_db

bp = Blueprint('sleeplab', __name__)

@bp.route('/')
def index():
    munchkin = session.get('username')

    if munchkin is None:
        return redirect(url_for("auth.login"))
    if munchkin is not None:
        # connect to db
        db = get_db()

        # grab the parent names
        # this assumes both parents are users in the app
        query = """
        SELECT parent
        FROM parents 
        WHERE munchkin=?
        ORDER BY parent
        """
        parents = db.execute(query,(session['username'],)).fetchall()

        #eturn("|".join(parents[0]))#
        return(render_template('sleeplab/index.html',parents=parents))

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
        munchkin = session.get('username')
        #return "|".join(request.form.keys())
        db.execute('INSERT INTO sleepTimes (munchkin,parent, sleepdate, sleeptime)'
                   'VALUES (?,?,?,?)',
                   (munchkin,request.form['parent'],request.form['date'],request.form['time']))
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



