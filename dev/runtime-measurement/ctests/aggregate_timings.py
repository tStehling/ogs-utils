#!/usr/bin/python

import subprocess
import shlex
import argparse
import os
import json

csv_sep = '\t'

parser = argparse.ArgumentParser()

parser.add_argument("root", type=str)
parser.add_argument("csv_output", type=argparse.FileType("w"))

args = parser.parse_args()

columns = set()
table = []

for dirpath, dirnames, filenames in os.walk(args.root):
    for filename in filenames:
        if not filename.endswith("_total_timings.json"):
            continue

        filepath = os.path.join(dirpath, filename)
        with open(filepath) as fh:
            values = json.load(fh)

        values[" test_case"] = os.path.relpath(
                filepath[:-len("_total_timings.json")], args.root)
        table.append(values)
        for k in values: columns.add(k)

table.sort(key=lambda row: row[" test_case"])

columns = sorted(columns)
args.csv_output.write('#' + csv_sep.join(columns) + '\n')

for row in table:
    full_row = [ '' ] * len(columns)
    for i, col in enumerate(columns):
        try:
            value = row[col]
            if type(value) is list:
                # only copy the timing information
                value = "{:.16g}".format(value[0])
            full_row[i] = value
        except KeyError:
            pass

    args.csv_output.write(csv_sep.join(full_row) + '\n')

