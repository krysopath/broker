#!/usr/bin/env python3
# coding=utf-8
import atexit
import code
import os
import readline

from broker import app
from broker.database import init_db

init_db()

app.config['SECRET_KEY'] = b"g25v09e85"

# Use the tab key for completion
historyPath = os.path.expanduser("./.broker_history")
readline.parse_and_bind('tab: complete')


def save_history(historyPath=historyPath):
    import readline
    readline.write_history_file(historyPath)


atexit.register(save_history)
if os.path.exists(historyPath):
    readline.read_history_file(historyPath)


def console():
    vars = globals().copy()
    vars.update(locals())
    # vars.__delitem__('console')
    # vars.__delitem__('stop')
    shell = code.InteractiveConsole(vars)
    shell.interact()


try:
    console()
except SyntaxError:
    console()
