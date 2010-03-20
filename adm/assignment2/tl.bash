#!/bin/bash

. setup.bash
base=tl
setup
echo "lslog $slog"

nums=100000
script="writes.py"
logt "Without tablelocking"
basic "withouttl" 1 1  >> $slog


script="writestl.py"
logt "With TL"
basic "withtl" 1 1  >> $slog
logt "Done"
