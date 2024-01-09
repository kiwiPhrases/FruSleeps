from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
#from sqlalchemy import text, inspect, exc

#from . import db
#from .models import Munchkins, Parents, SleepTimes
#from .auth import login_required

bp = Blueprint('about', __name__)

@bp.route("/about")
def about():
    return render_template("about/about.html")