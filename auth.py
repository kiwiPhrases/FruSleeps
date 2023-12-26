import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from FruSleeps.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# function for registering users
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')
    

# function for login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            #return redirect(url_for('index'))
            return redirect(url_for('auth.addparents'))

        flash(error)

    return render_template('auth/login.html')

# function for adding the parents
@bp.route('/addparents', methods=('GET', 'POST'))
def addparents():
    # check if there are parents registered for this child
    db = get_db()
    
    # fetch current user
    username = session.get('username')

    parres = db.execute("SELECT parent FROM parents WHERE munchkin=?",(username,)).fetchall()

    # if there are no parents then add parents
    # if there's at least 1 parent then redirect to index page
    if len(parres)>=1:
        return redirect(url_for('index'))
    if len(parres)==0:
        #return("%d" %len(parres))
        if request.method=='POST': 
            par1 = request.form['parent1']
            par2 = request.form['parent2']
            error = None
            db = get_db()
    
            # check parent inputs. This forces two parents...not great but for now meh
            if not par1:
                error = "Caregiver 1 is required"
            elif not par2:
                error = "Caregiver 2 is required"

            if error is None:
                for par in [par1,par2]:

                    try:
                        db.execute(
                            "INSERT INTO parents (munchkin, parent) VALUES (?, ?)",
                            (username, par),
                        )
                        db.commit()
                    except db.IntegrityError:
                        error = f"Parent {par} is already registered."
                        flash(error)
                    else:
                        return redirect(url_for("index"))                  
            # save error messages to display in the template
            flash(error)

        return render_template('auth/addparents.html')        

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))            

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view    