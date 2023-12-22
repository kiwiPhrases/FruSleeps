import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'FruSleeps.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # a simple page that says hello
    #@app.route('/index')
    #def index():
    #    return 'Hello, World!'

    # initialize database
    from . import db
    db.init_app(app)

    # register sleep button blueprint
    from . import sleeplab
    app.register_blueprint(sleeplab.bp)
    app.add_url_rule("/",endpoint='index')

    # register authorization blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # incorporate Dash app
    from .plotlydash.dashboard import create_dashboard
    app = create_dashboard(app)

    
    return app