#!/bin/bash

CHISSY="$0"

while [ -h "$CHISSY" ] ; do
  ls=`ls -ld "$CHISSY"`
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    CHISSY="$link"
  else
    CHISSY=`dirname "$CHISSY"`/"$link"
  fi
done

CHISSY=`dirname "$CHISSY"`

cd "$CHISSY" && ./run.py "$@"
