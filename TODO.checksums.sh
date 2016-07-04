#!/bin/sh

source vars.sh

find $srcdir \
  -path '$srcdir/Lightroom/Lightroom 4 Catalog Previews.lrdata' -prune \
  -or -not -name '.DS_Store' \
  -type f \
  -exec cksum "{}" \; >> src_checksums.txt

find $dstdir \
  -path '$dstdir/Lightroom/Lightroom 4 Catalog Previews.lrdata' -prune \
  -or -not -name '.DS_Store' \
  -type f \
  -exec cksum "{}" \; >> dst_checksums.txt

diff src_checksums.txt dst_checksums.txt

