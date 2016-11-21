#!/usr/bin/env python

# Heroku Flask Websockets version

import os
import sys
import json
import redis
import gevent
from chatLog import storeChat

import bot as bot


REDIS_URL = os.environ['REDIS_URL']
REDIS_CHAN = 'chat'

redis = redis.from_url(REDIS_URL)


# Chat Server Framework functions

def sleep(n):
    """Sleep n number of seconds.
    Pauses the execution of the program.
    """
    gevent.sleep(n)
    
def output(s):
    """Outputs string s as chat message.
    Send the given string to the chat client.
    """
    sessionID = sessionFromIntrospection()
    # actor 1  =  bot
    storeChat(sessionID, 1, s)
    data = {}
    data['handle'] = "bot"
    data['text'] = s
    data['session'] = sessionID
    message = json.dumps(data)
    redis.publish(REDIS_CHAN, message)


# Get the session from python introspection

def sessionFromIntrospection():
    selfFile = os.path.basename(__file__)
    callDepth = 1
    caller = None
    try:
        while True:
            caller = sys._getframe(callDepth)
            callerFile = caller.f_code.co_filename
            if callerFile == selfFile:
                break
            callDepth += 1
    except ValueError:
        print "Cannot go deeper than {}".format(callDepth)
        return = ""
    if caller:
        session = caller.f_locals.get('session', "")
        return session
    return ""


# Heroku Flask functions

def bot_setup(session):
    """Runs the setup function in the bot"""
    bot.setup()
    
def bot_response(session, message):
    """Let's the bot create a response for the given message"""
    bot.response(message)