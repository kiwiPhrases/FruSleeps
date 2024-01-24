import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

#from . import db
#from .models import Munchkins, Parents, SleepTimes
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
            from . import db
            from .models import Munchkins
            newuser = Munchkins(username=username, email=email, password=password)
            try:
                db.session.add(newuser)

                db.session.commit()
                db.session.close()
            except exc.IntegrityError:
                db.session.rollback()
                db.session.close()
                error = f"User {username} is already registered or {email} email is already used."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    return render_template('auth/register.html')
    

def chkparents():
    # check if there are parents registered for this child
    from . import db
    from .models import Parents
    # fetch current user
    username = session.get('username')
    # fetch existing records for parents
    parents = Parents.query.filter_by(munchkin=username).all()
    db.session.close()
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
        from . import db
        from .models import Munchkins
        username = request.form['username']
        password = request.form['password']

        error = None

        user = Munchkins.query.filter_by(username = username).first()
        db.session.close()
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
    # declare whether fields are optional or required
    ph = ['Required']*2 + ['Optional']*3

    #return("%d" %len(parres))
    username = session.get('username')

    # check if there are any parents already registered
    parents = Parents.query.filter_by(munchkin=username).all()
    if len(parents)>0:
        formparents = [p.parent for p in parents]
        #return render_template('auth/addparents.html', ph=ph)
    else:
        formparents = []
    
    # process the form
    if request.method=='POST':
        error = None
        formparents = []
        for i in range(5):
            # require name for parent 1
            if i<2:
                if not request.form['parent%d' %(i+1)]:
                    error = "Caregiver %d is required" %(i+1)
                elif request.form['parent%d' %(i+1)]:
                    formparents.append(request.form['parent%d' %(i+1)])
            # if 2nd parent is not named and Other is already not a parent then enter 'Other'
            else:
                #if (not request.form['parent%d' %(i+1)]) and ('Other' not in [x.parent.lower() for x in parents]):
                #    formparents.append("Other")
                if request.form['parent%d' %(i+1)]:
                    formparents.append(request.form['parent%d' %(i+1)])

        # if no new parents, enter new parent info
        if error is None:
            for i,par in enumerate(formparents):
                # check if entered parent is already among existing parents
                # if not, try entering them into the db
                if par.lower() not in [x.parent.lower() for x in parents]:
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

    return render_template('auth/addparents.html', ph=ph, formpars=formparents)        

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

