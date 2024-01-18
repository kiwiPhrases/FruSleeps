from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from sqlalchemy import text, inspect, exc, func, or_, and_

from . import db
from .models import Munchkins, Parents, SleepTimes
from .auth import login_required
import re

bp = Blueprint('sleeplab', __name__)

# just check the db connection
@bp.route('/hello2')
def hello2():
    return "%d" %db.session.execute(text("SELECT 1")).fetchone()[0]


@bp.route('/')
@login_required
def index():
    munchkin = session.get('username')

    if munchkin is None:
        return redirect(url_for("auth.login"))
    if munchkin is not None:
        # grab the parent names
        # this assumes both parents are users in the app
        parents = Parents.query.filter(Parents.munchkin.like(session['username'])).all()
        db.session.close()

        return(render_template('sleeplab/index.html',parents=parents))

@bp.route("/confirm",methods=("GET",'POST'))
@login_required
def confirm():
    import datetime
    # grab data from the button submission
    munchkin = session.get('username')
    parent = request.form['parent']
    error = None

    # get and date and time of sleep
    #if request.method=="GET":        
    now = datetime.datetime.now()
    #    browsertime = request.args.get("brwtime")
    zzztime = now.time().strftime("%H:%M")
    zzzdate = now.date().strftime("%Y-%m-%d")
    #zzztime = browsertime.strftime("%H:%M")
    #zzzdate = browsertime.strftime("%Y-%m-%d")

    if SleepTimes.query.filter(and_(SleepTimes.munchkin==munchkin,func.DATE(SleepTimes.sleeptime)==zzzdate)).first():
        error="A time has already been entered for %s today.\nAre you sure you wish to enter another?" %munchkin

    formvals = {'parent':parent,'sleepdate':zzzdate,'sleeptime':zzztime}

    if error is not None:
        flash(error)
    return render_template('sleeplab/confirm.html',formvals = formvals)
        
@bp.route("/mkrecord",methods=("GET",'POST'))
@login_required        
def mkrecord():
    
    # grab the input entries
    parent = request.form['parent']
    zzzdate = request.form['date']
    zzztime = request.form['time']
    #sleeptype = request.form['sleepType']
    #sleeploc = request.form['home']
    sleeptype='Night Sleep' # place holder values
    sleeploc='Home' #place holder values
    # save into formvals in case confirmation fails on the backend
    formvals = {'parent':parent,'sleepdate':zzzdate,'sleeptime':zzztime}

    if request.method=='POST':
        # grab username from the session
        munchkin = session.get('username')
        #return "|".join(request.form.keys())
        error=None

        hour = int(re.search("(\d+)\:",zzztime).group(1))
        if (sleeptype=='Night Sleep') and (hour<18):
            suggestion = hour+12 if hour<=12 else 'nap'
            if suggestion=='nap':
                suggesttxt = 'Want to record as a nap instead?'
            if suggestion!='nap':
                suggesttxt = 'Did you intend to enter %dpm as %d?'%(hour, suggestion)
            error='The entry is for night sleep but time is before 6pm.\n%s'%suggesttxt
            flash(error)
            return render_template('sleeplab/confirm.html',formvals = formvals)

        # make model instance to be added into the db
        st = SleepTimes(munchkin=munchkin, parent=parent,sleeptime=" ".join([zzzdate, zzztime]))

        # try inserting. If success then redirect to sleep dashboard
        # if fail then rollback, display error, and return to confirmation page
        try:
            db.session.add(st)
            db.session.commit()
            db.session.close()
            return redirect("/sleepdash")
            #return("Committed time")
        except exc.IntegrityError:
            db.session.rollback()
            db.session.close()
            error='Error in recording sleep time'
            return render_template('sleeplab/confirm.html',formvals = formvals)

        flash(error)
    return render_template('sleeplab/confirm.html',formvals = formvals)


