import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import Munchkins, Parents, SleepTimes
from sqlalchemy import exc

bp = Blueprint('auth', __name__, url_prefix='/auth')

# function for registering users
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
        email = request.form['email']
        #db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        elif password!=repassword:
            error = 'Passwords do not match'

        if error is None:
            newuser = Munchkins(username=username, email=email, password=password)
            try:
                db.session.add(newuser)

                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    return render_template('auth/register.html')
    

def chkparents():
    # check if there are parents registered for this child

    # fetch current user
    username = session.get('username')
    # fetch existing records for parents
    parents = Parents.query.filter_by(munchkin=username).all()
    
    # if there's at least 1 parent then redirect to index page
    if parents:
        return('index')
    # if there are no parents then add parents
    if not parents:
        return('auth.addparents')
    
# function for login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    # clear out existing login if going to login
    user_id = session.get('username')
    if user_id is not None:
        session.clear()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        user = Munchkins.query.filter_by(username = username).first()

        if user is None:
            error = 'Incorrect username.'
        #elif not check_password_hash(user.password, password):
        elif not user.password==password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()

            session['username'] = user.username 

            gonext = chkparents()
            #return gonext
            return redirect(url_for(gonext))

        flash(error)

    return render_template('auth/login.html')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view    

# function for adding the parents
# make this accept up to, say, 5 fields
# make number of parents being entered dynamic though 
# 2 is a minimum
# set default
# write down directions for this form
# redirect to this form on /addparents click
@bp.route('/addparents', methods=('GET', 'POST'))
@login_required
def addparents():
    #return("%d" %len(parres))
    username = session.get('username')

    if request.method=='POST':
        error = None
        formparents = []
        for i in range(2):
            if not request.form['parent%d' %(i+1)]:
                error = "Caregiver %d is required" %(i+1)
            elif request.form['parent%d' %(i+1)]:
                formparents.append(request.form['parent%d' %(i+1)])

        if error is None:
            for i,par in enumerate(formparents):
                    newparent = Parents(munchkin=username, parent=par)
                    try:
                        db.session.add(newparent)
                        db.session.commit()
                    except exc.IntegrityError:
                        db.session.rollback()
                        error='Issue in adding parents'

            return redirect(url_for("index"))                  
        # save error messages to display in the template
        flash(error)

    return render_template('auth/addparents.html')        

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('username')

    if user_id is None:
        g.user = None
    else:
        g.user = Munchkins.query.filter_by(username = user_id).first()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))            

