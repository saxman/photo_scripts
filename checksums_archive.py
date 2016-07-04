#!/usr/bin/python

import os
import sys
import hashlib
import csv

SRC_DIR = '/Volumes/Archive/Pictures'
OUT_FILE = 'checksums_archive.tsv'

with open(OUT_FILE, 'wb') as fout:
    writer = csv.writer(fout, delimiter='\t', quotechar='\"', quoting=csv.QUOTE_MINIMAL)

    for root, subdirs, files in os.walk(SRC_DIR):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            while open(file_path, 'rb') as fin:
                checksum = hashlib.md5(fin.read()).hexdigest()

            writer.writerow([root, file_name, checksum])
