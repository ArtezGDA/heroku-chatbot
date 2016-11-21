#!/usr/bin/env python

# Default bot template

from chatServer import sleepx, output

def setup():
    output("This is the bot template.")
    sleepx(1)
    output('It does nothing more than just responding with "Ok".')
    
def response(input):
    sleepx(1)
    print(input)
    output("Ok")