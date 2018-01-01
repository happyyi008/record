#! /usr/bin/python

import csv
import datetime
import sys
import os

#
# usage: record <activity> [0-23]-[0-23]
# record <activity> by the hour into a csv file
#

catagories = [
    "code",
    "cook",
    "chill",
    "eat",
    "exam",
    "exercise",
    "health",
    "prep",
    "shop",
    "sleep",
    "social",
    "study",
    "transit",
    "watching-smt",
]

record_file = os.path.expanduser('~/.record')

def main():
    args = sys.argv

    date_today = get_date(args)
    if args[1] == 'show':
        print_day(str(date_today))
        return

    if len(args) < 3 and args[1] != 'show':
        print "You're missing something"
        return

    new_activity = args[1]

    if new_activity not in catagories:
        print 'activity {} is not in list'.format(args[2])
        return

    record_activity(new_activity, args[2], date_today)


def record_activity(new_activity, interval, date):
    fieldnames = ['date'] + [str(x) for x in range(0,24)]
    start, end = (int(i) for i in interval.split('-'))
    if start >= end:
        print 'invalid time interval {}-{}'.format(start, end)

    record_list = load_record()
    with open(record_file, 'wb+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        modifying = False
        for line, row in enumerate(record_list):
            modified_row = row
            if row['date'] == str(date):
                modified_row = modify_record(row, start, end, new_activity)
                modifying = True
            writer.writerow(modified_row)
   
        if not modifying:
            activity = {'date':str(date)}
            activity = modify_record(activity, start, end, new_activity)
            writer.writerow(activity)


def get_date(args):
    date_today = datetime.date.today()
    if len(args) == 4:
        if args[3] == 'yesterday':
            date_today = datetime.date.today() - datetime.timedelta(days=1)
        else:
            date_today = datetime.datetime.strptime(args[3],'%Y-%m-%d').date()
    return date_today

def load_record():
    record_list = list()
    if not os.path.exists(record_file):
        return record_list
    with open(record_file, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        record_list.extend(reader)
    return record_list

def modify_record(activity, start, end, activity_name):
    for i in range(start, end):
        activity[str(i)] = activity_name
    return activity

def print_day(day):
    record_list = load_record()
    record = get_record(record_list, day)
    print "Today: {}".format(record['date'])
    for t in range(0, 24):
        print '{}: {}'.format(str(t).rjust(3), record.get(str(t)) or 'nothing')

def get_record(record_list, day):
    for line, row in enumerate(record_list):
        if row['date'] == day:
            return record_list[line]
    return dict()

if __name__ == '__main__':
    main()

