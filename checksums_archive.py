#!/usr/bin/python

import os
import sys
import hashlib
import csv

SRC_DIR = '/Volumes/Archive/Pictures'
OUT_FILE = 'checksums_archive.tsv'

checksums = []

for root, subdirs, files in os.walk(SRC_DIR):
    for file in files:
        if file != '.DS_Store':
            with open(os.path.join(root, file), 'rb') as _file:
                checksums.append([root, file, hashlib.md5(_file.read()).hexdigest()])

with open(OUT_FILE, 'wb') as fout:
    writer = csv.writer(fout, delimiter='\t', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(checksums)
