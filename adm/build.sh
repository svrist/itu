#!/bin/sh

. buildinit.sh

if [ "x$1" = "x" ]; then
  name=project
else
  name=$1
fi
dobuild $name
