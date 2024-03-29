# -*- coding: utf-8 -*-

import os
import logging
import datetime
from operator import itemgetter

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.debug = 'DEBUG' in os.environ
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class Message(db.Model):
    __tablename__ = "chat_messages"
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


def start():
    db.create_all()


def storeChat(session, actor, message):
    """docstring for storeChat."""
    app.logger.info(u'Storing message: {}'.format(message))
    now = datetime.datetime.now()
    newMessage = Message(session, now, actor, message)
    db.session.add(newMessage)
    db.session.commit()

    
def listAllChats():
    """docstring for listAllChats"""
    all_chats = Message.query.order_by(Message.date).all()
    sessionIDs = []
    sessions = []
    # Organize per sessions
    for chat in all_chats:
        # Do we already have this session?
        if chat.session in sessionIDs:
            sessionIndex = sessionIDs.index(chat.session)
            session = sessions[sessionIndex]
        else:
            # Add this session
            session = {'id': chat.session, 'messages': [], 'startDate': chat.date, 'lastDate': chat.date}
            sessionIDs.append(chat.session)
            sessions.append(session)
            session = sessions[-1]
        # Update the start or last date of the session, if necessary
        if chat.date < session['startDate']:
            session['startDate'] = chat.date
        if chat.date > session['lastDate']:
            session['lastDate'] = chat.date
        # Append the message
        if chat.actor == 0:
            style = "me"
        elif chat.actor == 1:
            style = "bot"
        else:
            style = ""
        message = {'text': chat.message, 'date': chat.date.strftime("%a %d-%b-%Y %H:%M:%S"), 'style': style}
        session['messages'].append(message)
    # Order the sessions by start date
    orderedSessions = sorted(sessions, key=itemgetter('startDate'), reverse=True)
    for index, session in enumerate(orderedSessions):
        session['startOrder'] = index
    # Order the sessions by most recent
    mostrecentSessions = sorted(sessions, key=itemgetter('lastDate'), reverse=True)
    for index, session in enumerate(mostrecentSessions):
        session['recentOrder'] = index
    # Return the a dict of ordered set and total count
    returnDict = {}
    returnDict['sessions'] = orderedSessions
    returnDict['sessionCount'] = len(orderedSessions)
    returnDict['chatCount'] = len(all_chats)
    return returnDict