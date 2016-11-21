#!/usr/bin/env python

# Default bot template

import chatServer as c

def setup():
    c.output("This is the bot template.")
    c.sleep(1)
    c.output('It does nothing more than just responding with "Ok".')
    
def response(input):
    c.sleep(1)
    print(input)
    c.output("Ok")