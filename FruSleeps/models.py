from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

from . import db

class Munchkins(db.Model):
    #id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(80),unique=True, nullable=False, primary_key=True)
    email = sa.Column(sa.String(80), nullable=False, unique=True)
    password = sa.Column(sa.String(80),nullable=False)
     #email_confirmed_at = sa.Column(sa.DateTime())
    def __repr__(self):
        return '<User %r>' % self.username
    
class Parents(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    munchkin = sa.Column(sa.String(80),nullable=False, unique=False)
    parent = sa.Column(sa.String(80), nullable=True)

class SleepTimes(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    munchkin = sa.Column(sa.String(80), nullable=False)
    parent = sa.Column(sa.String(80),nullable=False)
    sleeptime = sa.Column(sa.DateTime, nullable=False)
    #sleeptype = sa.Column(sa.String(80), default='sleep',nullable=False)
    #sleeploc = sa.Column(sa.String(80), default='home',nullable=False)
    #sleepType = sa.Column(sa.String(10), nullable=False )



    
