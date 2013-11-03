#!/bin/bash

root=p

for f in $(find $root -name '*.NEF');
do
  fname=`echo "$f" | cut -d\. -f1`
  if [ -e $fname.jpg ]
  then
    rm -v $fname.jpg
  elif [ -e $fname.JPG ]
  then
    rm -v $fname.JPG
  elif [ -e $fname.jpeg ]
  then
    rm -v $fname.jpeg
  elif [ -e $fname.JPEG ]
  then
    rm -v $fname.JPEG
  fi
done

