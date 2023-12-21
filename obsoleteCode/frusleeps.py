from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    header_frmt = "<center/><h1>{}<h1></center"
    title = header_frmt.format("Welcome to Fru's Sleep Tracker")
    txt = """
    <p/>This app is simply there to record who put the Fru to sleep and at what time.</p>
    <p/>You can then check the stats on Fru's sleeping patterns by parents and across time.</p>
    """

    return(title+txt)

@app.route('/about')
def about():
    header_frmt = "<center/><h1>{}<h1></center"
    title = header_frmt.format("About the tracker")
    txt = """
    <p/>Hobby project and learning pathway for Flask and Docker</p>
    <p/>Author is Gene Burinskiy and all rights are reserved</p>
    """

    return(title+txt)


@app.route("/helloworld")
def helloworld():
    return("<center/><h1>Hello, World!<h1></center")

#url_for('static',filename ='style.css')    

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)    
