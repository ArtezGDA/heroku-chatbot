# -*- coding: utf-8 -*-

import os
import logging
import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.String(60))
    date = db.Column(db.DateTime())
    actor = db.Column(db.Integer)
    message = db.Column(db.String(255))

    def __init__(self, session, date, actor, message):
        self.session = session
        self.date = date
        self.actor = actor
        self.message = message

    def __repr__(self):
        return '<Session: %s, Actor %d: Message %s>' % (self.session, self.actor, self.message)
    

def storeChat(session, actor, message):
    """docstring for storeChat"""
    app.logger.info(u'Storing message: {}'.format(message))
    now = datetime.datetime.now()
    newMessage = Message(session, now, actor, message)
    db.session.add(newMessage)
    db.session.commit()
    
def listAllChats():
    """docstring for listAllChats"""
    all_chats = Message.query.group_by(Message.session).all()
    return [{'session': c.session, 'message': c.message } for c in all_chats]