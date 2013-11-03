#!/bin/bash

root=/Volumes/Archive/Pictures

for f in $(find $root -name '*.JPG')
do
  fname=`echo $f | cut -d\. -f1`
  if ls $fname-?.JPG &> /dev/null
  then
    ls $fname-?.JPG
  elif ls $fname-?.jpg &> /dev/null
  then
    ls $fname-?.jpg
  fi
done

