#!/bin/sh

root=/Volumes/Archive

cd $root

tar cvzf \
  /Volumes/Backup/Pictures-`date +%F`.tar.gz \
  --exclude='Lightroom/Lightroom 4 Catalog Previews.lrdata' \
  --exclude='Lightroom/Plugins' \
  --exclude='.DS_Store' \
  Pictures \
  Lightroom
