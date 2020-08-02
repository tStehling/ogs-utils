#!/usr/bin/env python

from lxml import etree as ET
import re
import shutil
import sys

def writeResult(filename, tree):
    tree.write(open(filename, 'wb'), encoding=tree.docinfo.encoding, pretty_print=True, xml_declaration=True)

def addOffsetToExponentialProperty(exponential_property):
    exponential_property.append(ET.XML("<offset>0</offset>"))

def addOffsetToExponentialProperties(medium):
    for p in medium.find("./properties"):
        if p.find("./type").text == "Exponential":
            if p.find("./offset") is None:
                addOffsetToExponentialProperty(p)

def processFile(filename):
    shutil.copy2(filename, filename+'.bak')
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(filename, parser)
    root = tree.getroot()

    for medium in tree.xpath('./media/medium'):
        addOffsetToExponentialProperties(medium)
        phase_path = "./phases/phase"
        for phase in medium.xpath(phase_path):
            addOffsetToExponentialProperties(phase)

    writeResult(filename, tree)

processFile(sys.argv[1])
