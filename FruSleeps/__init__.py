from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from sqlalchemy import text
from flask.cli import FlaskGroup


db = SQLAlchemy()
#from .models import Munchkins, Parents, SleepTimes

def create_app():
    #config_name='default',test_config=None
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #app.config.from_object(config.get(config_name or 'default'))
    config_name = 'default'
    app.config.from_object(config.get(config_name))
    #app.secret_key = "secret key" #this comes from env
    config[config_name].init_app(app)
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    from . import about
    app.register_blueprint(about.bp)
    #app.add_url_rule("/",endpoint='about')

    # register authorization blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # register sleep button blueprint
    from . import sleeplab
    app.register_blueprint(sleeplab.bp)
    app.add_url_rule("/",endpoint='index')

    # register sleep dash blueprint
    from . import sleepdash
    app.register_blueprint(sleepdash.bp)
    app.add_url_rule("/",endpoint='sleepdash')

    # incorporate Dash app
    # this is super tedious. It's literally easier to just write plotly into Flask
    #from .plotlydash.dashboard import init_dashboard
    #app = init_dashboard(app)

    return app

cli = FlaskGroup(create_app=create_app)

@cli.command
def custom_command():
    pass

if __name__ == '__main__':
    cli()