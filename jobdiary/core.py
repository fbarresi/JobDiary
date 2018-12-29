import sys
from pathlib import Path
from tinydb import TinyDB, Query
from huepy import *
import datetime


from jobdiary.texts import usage


db = TinyDB(str(Path.home().joinpath("jobdiary.json")))


def decode_args(args, encoding=None):
    """
    Convert all bytes args to str
    by decoding them using stdin encoding.
    """
    return [
        arg.decode(encoding)
        if type(arg) == bytes else arg
        for arg in args
    ]

def start():
    now = datetime.datetime.now()
    entry = Query()
    result = db.search(entry.day == str(now.date()))
    if len(result) > 0:
        result[0]['entries'].append({'type':'start','time': str(now.time())})
        db.insert(result[0])
    else:
        db.insert({'day':str(now.date()), 'entries':[{'type':'start','time': str(now.time())}]})
    return run("started!")

def stop():
    now = datetime.datetime.now()
    entry = Query()
    result = db.search(entry.day == str(now.date()))
    if len(result) > 0:
        result[0]['entries'].append({'type':'end','time': str(now.time())})
        db.insert(result[0])
        return info("stopped")
    else:
        return bad("no daily entry found")

def main(args=sys.argv[1:]):
    """
    The main function.
    Pre-process args, handle some special types of invocations,
    and run the main program with error handling.
    Return exit status code.
    """
    args = decode_args(args)

    include_debug_info = '--debug' in args

    if len(args) == 0 : print(usage())

    if include_debug_info :
        print(orange(str(Path.home().joinpath("jobdiary.json"))))


    commands = {
    "start": start,
    "stop": stop
    }

    func = commands.get(args[0], lambda: "Invalid command")
    print(func())
    return
