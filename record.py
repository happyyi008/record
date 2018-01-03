#! /usr/bin/python

import csv
import datetime
import sys
import os
import util

#
# usage:
# record <activity> [0-23]-[0-23]
#   records <activity> by the hour into a csv file
# record show
#   prints activities added today

catagories = [
    "code",
    "cook",
    "chill",
    "class",
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
    date_today = util.get_date(args[2:])
    if args[1] == 'show':
        print_day(str(date_today))
        return

    if len(args) < 3 and args[1] != 'show':
        print "You're missing something"
        return

    new_activity = args[1]
    if new_activity not in catagories:
        print 'activity {} is not in list'.format(new_activity)
        return

    record_activity(new_activity, args[2], date_today)


def record_activity(new_activity, interval, date):
    start, end = util.parse_interval(interval)
    if start >= end:
        print 'invalid time interval {}-{}'.format(start, end)

    record_list = load_record()
    line, record = get_record(record_list, str(date))
    if line != -1:
        record_list[line] = util.modify_record(record, start, end, new_activity)
    else:
        activity = {'date':str(date)}
        activity = util.modify_record(activity, start, end, new_activity)
        record_list.append(activity)
    update_record(record_list)

def update_record(record_list):
    fieldnames = ['date'] + [str(x) for x in range(0,24)]
    with open(record_file, 'wb+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in record_list:
            writer.writerow(record)

def load_record():
    record_list = list()
    if not os.path.exists(record_file):
        return record_list
    with open(record_file, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        record_list.extend(reader)
    return record_list

def print_day(date):
    record_list = load_record()
    _, record = get_record(record_list, date)
    if not record:
        record['date'] = date
    print "Today: {}".format(record['date'])
    for t in range(0, 24):
        print '{}: {}'.format(str(t).rjust(3), record.get(str(t)) or 'nothing')

def get_record(record_list, date):
    for line, row in enumerate(record_list):
        if row['date'] == date:
            return (line, record_list[line])
    return (-1, dict())

if __name__ == '__main__':
    main()

