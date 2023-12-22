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
    # grab username and password from the   page
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # if empty, return these errors
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # check if ther username is already in the db or not
        # if already in there, return an error
        # otherwise, commit to the db
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            # redirect to the login page
            else:
                return redirect(url_for("auth.login"))
        # save error messages to display in the template
        flash(error)

    return render_template('auth/register.html')

# function for login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        # grab user inputs
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
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')    

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
    return redirect(url_for('sleeplab.index'))            

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view    