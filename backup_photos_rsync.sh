#!/bin/sh

source vars.sh

rsync -av \
--exclude=.DS_Store \
--delete \
$srcdir \
$dstdir

