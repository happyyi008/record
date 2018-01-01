#! /usr/bin/python

import datetime

def parse_interval(interval):
    l = [int(i) for i in interval.split('-')]
    if len(l) == 1:
        return (l[0], l[0]+1)
    return tuple(l) 

def get_date(args):
    date_today = datetime.date.today()
    if len(args) == 4:
        if args[3] == 'yesterday':
            date_today = datetime.date.today() - datetime.timedelta(days=1)
        else:
            date_today = datetime.datetime.strptime(args[3],'%Y-%m-%d').date()
    return date_today

def modify_record(activity, start, end, activity_name):
    for i in range(start, end):
        activity[str(i)] = activity_name
    return activity

