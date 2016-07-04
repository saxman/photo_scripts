#!/bin/sh

rsync -av \
--exclude=.DS_Store \
--delete \
~/Music/iTunes/ \
/Volumes/Archive/iTunes/

