# -*- coding: utf-8 -*-

import logging
from flask import Flask

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

def storeChat(session, date, actor, message):
    """docstring for storeChat"""
    app.logger.info(u'Storing message: {}'.format(message))
