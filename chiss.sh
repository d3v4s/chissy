#!/bin/bash

CHISS="$0"

while [ -h "$CHISS" ] ; do
  ls=`ls -ld "$CHISS"`
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    CHISS="$link"
  else
    CHISS=`dirname "$CHISS"`/"$link"
  fi
done

CHISS_DIR=`dirname "$CHISS"`

cd "$CHISS_DIR" && ./run.py $@ # bash -c "exec -a chiss ./run.py $@" #./run.py "$1"
