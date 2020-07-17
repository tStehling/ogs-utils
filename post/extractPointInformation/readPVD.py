#!/usr/bin/env python

import sys
from lxml import etree as ET

def readPVD(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    ts_files = {}
    ts_files['ts'] = []
    ts_files['filename'] = []
    for collection in root.getchildren():
        for dataset in collection.getchildren():
            ts_files['ts'].append(dataset.attrib['timestep'])
            ts_files['filename'].append(dataset.attrib['file'])
    return ts_files

print('number of arguments: ' + str(len(sys.argv)))
for i in range(2, len(sys.argv)):
    print('arg ' + str(i) + ': ' + sys.argv[i])
#pvd = readPVD(sys.argv[1])
#for i in range(0, len(pvd['ts'])):
#    print(pvd['ts'][i] + ' ' + pvd['filename'][i])
