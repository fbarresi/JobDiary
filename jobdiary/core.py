import sys
from pathlib import Path
from tinydb import TinyDB, Query
from huepy import *
import datetime
import pprint


from jobdiary.texts import usage


db = TinyDB(str(Path.home().joinpath("jobdiary.json")))
pp = pprint.PrettyPrinter(indent=4)

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

def start(args):
    now = datetime.datetime.now()
    entry = Query()
    results = db.search(entry.day == str(now.date()))
    if len(results) > 0:
        result = results[0]
        #check entries already was ended
        starts_and_stops = [e for e in result['entries'] if (e['type'] == 'start') | (e['type'] == 'end')]
        if len(starts_and_stops) % 2 == 0:
            result['entries'].append({'type':'start','time': str(now.time())})
            db.update(result)
        else:
            return bad("unable to start")
    else:
        db.insert({'day':str(now.date()), 'entries':[{'type':'start','time': str(now.time())}]})
    return run("started!")

def stop(args):
    now = datetime.datetime.now()
    entry = Query()
    results = db.search(entry.day == str(now.date()))
    if len(results) > 0:
        result = results[0]
        #check entries already was ended
        starts_and_stops = [e for e in result['entries'] if (e['type'] == 'start') | (e['type'] == 'end')]
        if len(starts_and_stops) % 2 != 0:
            result['entries'].append({'type':'end','time': str(now.time())})
            db.update(result)
            return run("stopped")
        return bad("unable to stop")
    else:
        return bad("no daily entry found")

def project(args):
    now = datetime.datetime.now()
    entry = Query()
    results = db.search(entry.day == str(now.date()))
    if len(results) > 0:
        result = results[0]
        #check entries already was ended
        starts_and_stops = [e for e in result['entries'] if (e['type'] == 'start') | (e['type'] == 'end')]
        if len(starts_and_stops) % 2 != 0:
            result['entries'].append({'type':'project','time': str(now.time()), 'project': args[0]})
            db.update(result)
            return good("Project : " + args[0])
        return bad("unable add entry")
    else:
        return bad("no daily entry found")

def task(args):
    now = datetime.datetime.now()
    entry = Query()
    results = db.search(entry.day == str(now.date()))
    if len(results) > 0:
        result = results[0]
        #check entries already was ended
        starts_and_stops = [e for e in result['entries'] if (e['type'] == 'start') | (e['type'] == 'end')]
        if len(starts_and_stops) % 2 != 0:
            result['entries'].append({'type':'task','time': str(now.time()), 'task': args[0]})
            db.update(result)
            return good("Task : " + args[0])
        return bad("unable add entry")
    else:
        return bad("no daily entry found")

def day_is_calendar_week(date_string, week_number):
    return datetime.datetime.strptime(date_string, "%Y-%m-%d").date().isocalendar()[1] == int(week_number)

def report(args):
    now = datetime.datetime.now()
    target_date = now.date()
    entry = Query()
    if len(args) != 0:
        if "-m" in args:
            target_date = "^"+datetime.datetime.strptime(args[1], "%m.%Y").strftime("%Y-%m")+"*"
        elif "-w" in args:
            results = db.search(entry.day.test(day_is_calendar_week, args[1]))
            if len(results) > 0:
                return pp.pformat(list(result for result in results))
            else:
                return bad("no entry found")
        else:
            target_date = datetime.datetime.strptime(args[0], "%d.%m.%Y").strftime("%Y-%m-%d")
    else:
        target_date = now.date()

    results = db.search(entry.day.matches(str(target_date)))
    if len(results) > 0:
        return pp.pformat(list(result for result in results))
    else:
        return bad("no entry found")

def main(args=sys.argv[1:]):
    """
    The main function.
    Pre-process args, handle some special types of invocations,
    and run the main program with error handling.
    Return exit status code.
    """
    args = decode_args(args)

    include_debug_info = '--debug' in args

    if len(args) == 0 :
        print(usage())
        return

    if include_debug_info :
        print(orange(str(Path.home().joinpath("jobdiary.json"))))
        print(args)

    commands = {
        "start": start,
        "stop": stop,
        "project": project,
        "task": task,
        "report": report
    }

    func = commands.get(args[0], lambda: "Invalid command")
    print(func(args[1:]))
    return
