# -*- coding: utf-8 -*-

"""
Chat Server
===========

This simple application uses WebSockets to run a primitive chat server.
"""

import os
import json
import logging
import redis
import gevent
from flask import Flask, render_template
from flask_sockets import Sockets

from chatLog import storeChat, listAllChats

REDIS_URL = os.environ['REDIS_URL']
REDIS_CHAN = 'chat'

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)
redis = redis.from_url(REDIS_URL)



class ChatBackend(object):
    """Interface for registering and updating WebSocket clients."""

    def __init__(self):
        self.clients = dict()
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(REDIS_CHAN)

    def __iter_data(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            if message['type'] == 'message':
                app.logger.info(u'Sending message: {}'.format(data))
                yield data

    def register(self, client, sessionID):
        """Register a WebSocket connection for Redis updates."""
        self.clients[sessionID] = client

    def send(self, client, data):
        """Send given data to the registered client.
        Automatically discards invalid connections."""
        try:
            client.send(data)
        except Exception:
            # Remove the client from the dictionary
            self.clients = {key: value for key, value in self.clients.items() if value is not client}

    def run(self):
        """Listens for new messages in Redis, and sends them to clients."""
        for data in self.__iter_data():
            for session in self.clients.keys():
                # Only send the data if it meant of the same session as the client
                # Or if the client is listening to all (session = "")
                # Or if the message is to be broadcasted (session = "broadcast")
                messageDict = json.loads(data)
                messageSession = messageDict['session']
                if session == "" or messageSession == "broadcast" or session == messageSession:
                    gevent.spawn(self.send, self.clients[session], data)

    def start(self):
        """Maintains Redis subscription in the background."""
        gevent.spawn(self.run)

chats = ChatBackend()
chats.start()


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/logs')
def all_logs():
    allLogs = listAllChats()
    return render_template('logs.html', logs = allLogs)

@sockets.route('/submit')
def inbox(ws):
    """Receives incoming chat messages, inserts them into Redis."""
    while not ws.closed:
        # Sleep to prevent *constant* context-switches.
        gevent.sleep(0.1)
        message = ws.receive()

        if message:
            data = json.loads(message)
            
            # Get the handle
            handle = data['handle']
            
            # Set the session
            session = sessionID(ws)
            data['session'] = session
            # With the handle * , the message will be broadcasted
            if handle == "*":
                data['session'] = "broadcast"
            message = json.dumps(data)
            
            # Log this message
            app.logger.info(u'Inserting message by {}: {}'.format(handle, message))
            
            # Store the chat in the database
            # TODO: not only use agent 0
            storeChat(data['session'], 0, data['text'])
            redis.publish(REDIS_CHAN, message)
            
            # After a second, send a response
            response = "Ok. Thanks."
            storeChat(session, 1, response)
            data = {}
            data['handle'] = "bot"
            data['text'] = response
            data['session'] = session
            message = json.dumps(data)
            redis.publish(REDIS_CHAN, message)

@sockets.route('/receive')
def outbox(ws):
    """Sends outgoing chat messages, via `ChatBackend`."""
    session = sessionID(ws)
    app.logger.debug(u'session id for outbox: {}'.format(session))
    chats.register(ws, session)

    while not ws.closed:
        # Context switch while `ChatBackend.start` is running in the background.
        gevent.sleep(0.1)

def sessionID(ws):
    """Returns the sessionID, given as url parameter to the request."""
    request = ws.environ.get('werkzeug.request')
    session = request.args.get('session', "")
    return session
    
