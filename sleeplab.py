from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from sqlalchemy import text, inspect, exc

from . import db
from .models import Munchkins, Parents, SleepTimes
from .auth import login_required

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

        return(render_template('sleeplab/index.html',parents=parents))

@bp.route("/confirm",methods=("GET",'POST'))
@login_required
def confirm():
    import datetime
    # grab data from the button submission
    parent = request.form['parent']
    error = None

    if error is not None:
        flash(error)

    # get and date and time of sleep
    now = datetime.datetime.now()

    zzztime = now.time().strftime("%H:%M")
    zzzdate = now.date().strftime("%Y-%m-%d")

    formvals = {'parent':parent,'sleepdate':zzzdate,'sleeptime':zzztime}

    return render_template('sleeplab/confirm.html',formvals = formvals)
        
@bp.route("/mkrecord",methods=("GET",'POST'))
@login_required        
def mkrecord():
    parent = request.form['parent']
    zzzdate = request.form['date']
    zzztime = request.form['time']
    formvals = {'parent':parent,'sleepdate':zzzdate,'sleeptime':zzztime}
    if request.method=='POST':
        munchkin = session.get('username')
        #return "|".join(request.form.keys())
        error=None
        st = SleepTimes(munchkin=munchkin, parent=parent,sleeptime=" ".join([zzzdate, zzztime]))
        try:
            db.session.add(st)
            db.session.commit()
            return redirect("/sleepdash")
            #return("Committed time")
        except exc.IntegrityError:
            db.session.rollback()
            error='Error in recording sleep time'
            return render_template('sleeplab/confirm.html',formvals = formvals)

        flash(error)
    return render_template('sleeplab/confirm.html',formvals = formvals)


