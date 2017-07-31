#!/usr/bin/python

import subprocess
import shlex
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("in_file", type=str)
parser.add_argument("--json-out", action="store_true")
parser.add_argument("--quiet", action="store_true")

args = parser.parse_args()


cumulative_values = {}
max_cat_length = 0

proc = subprocess.Popen(
        '''grep -F '[time]' {} | sed -e 's_^.*[[]time[]] \([^0-9#]*\) .*took \([^ ]*\) s.*$_\\2 \\1_' ''' \
                .format(shlex.quote(args.in_file))
        , shell=True, stdout=subprocess.PIPE)

for line in proc.stdout:
    t, cat = line.decode("utf-8").strip().split(maxsplit=1)
    t = float(t)

    if cat in cumulative_values:
        p = cumulative_values[cat]
        np = (p[0] + t, p[1] + 1)
        cumulative_values[cat] = np
    else:
        cumulative_values[cat] = (t, 1)
    if len(cat) > max_cat_length:
        max_cat_length = len(cat)

if not args.quiet:
    for k, (t, count) in sorted(cumulative_values.items(), key=lambda p: p[1][0], reverse=True):
        print(("{:6} times {:" + str(max_cat_length) + "} took in total {} s").format(count, k, t))

if args.json_out:
    import json
    out_file = args.in_file + "_total_timings.json"
    with open(out_file, "w") as fh:
        json.dump(cumulative_values, fh, indent=2)

