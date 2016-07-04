#!/bin/sh

rsync -av \
--exclude=.DS_Store \
--delete \
~/Music/iTunes/iTunes\ Media/Music/ \
/Volumes/Archive/Music/

