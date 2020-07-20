#!/usr/bin/env python

import sys
from lxml import etree as ET

def readPVTU(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    pvtu_files = {}
    pvtu_files['filename'] = []
    for piece in root.xpath('//Piece'):
        pvtu_files['filename'].append(piece.attrib['Source'])
    return pvtu_files

pvtu = readPVTU(sys.argv[1])
for i in range(0, len(pvtu['filename'])):
    print(pvtu['filename'][i])
