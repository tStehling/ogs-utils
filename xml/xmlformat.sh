#!/usr/bin/sh

tmpfile=$(mktemp /tmp/xmlformat.XXXXXX)

xmlstarlet fo -s 4 ${1} > ${tmpfile} && mv ${tmpfile} ${1}

rm -rf ${tmpfile} # if something goes wrong
