#!/bin/sh

rsync -av \
--exclude="Lightroom/Lightroom 4 Catalog Previews.lrdata" \
--exclude=.DS_Store \
--delete \
/Volumes/Archive/Pictures/ \
/Volumes/Backup/Pictures/

