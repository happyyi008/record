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
    "sleep",
    "study",
    "cook",
    "shop",
    "exercise",
    "eating",
    "chill",
    "watching-smt",
    "transit",
    "exam",
    "social",
    "coding",
]

def main():
    args = sys.argv
    record_file = os.path.expanduser('~/.record')
    fieldnames = ['date'] + [str(x) for x in range(0,24)]

    if len(args) != 3:
        print "You're missing something"
        return

    if args[1] not in catagories:
        print "activity {} is not in list".format(args[2])
        return

    start, end = (int(i) for i in args[2].split('-'))
    if start >= end:
        print "invalid time interval {}-{}".format(start, end)

    date_today = datetime.date.today()
    activity = {'date':str(date_today)}

    activity_list = list()
    file_exists = os.path.exists(record_file)
    if file_exists:
        with open(record_file, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            activity_list.extend(reader)
        
    with open(record_file, 'wb+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        modifying = False
        for line, row in enumerate(activity_list):
            modified_row = row
            if row['date'] == str(date_today):
                modified_row = modify_activity(row, start, end, args[1])
                modifying = True
            writer.writerow(modified_row)
   
        if not modifying:
            activity = modify_activity(activity, start, end, args[1])
            writer.writerow(activity)


def modify_activity(activity, start, end, activity_name):
    for i in range(start, end):
        activity[str(i)] = activity_name
    return activity

if __name__ == "__main__":
    main()

