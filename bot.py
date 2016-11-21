#!/usr/bin/env python

# Default bot template

from chatServer import sleep, output

def setup():
    output("This is the bot template.")
    sleep(1)
    output('It does nothing more than just responding with "Ok".')
    
def response(input):
    sleep(1)
    print(input)
    output("Ok")