#!/bin/bash

. setup.bash
base=run1
setup
script=profwrites3.py

logt "Threads experiments"
change_param "LOGBUFSZ" 256 >> $slog
logt "Threads 10"
basic "threads10" 10 >> $slog

logt "Threads 5"
basic "threads5" 5 >> $slog

logt "Threads 3"
basic "threads3" 3 >> $slog

logt "Threads 2"
basic "threads2" 2 >> $slog

logt "Threads 1"
basic "threads1" 1 >> $slog

logt "Threads 20"
basic "threads20" 20 >> $slog

for i in 1 2 5 10 25 50
do
logt "Table clustered index"
basic "indexclust-t$t" $t 5 "initpctfree.sql" >> $slog

logt "Table nopk index"
basic "indexnopk-t$t" $t 5 "initnopk.sql" >> $slog

logt "Append On experiment"
append "on" >> $slog
basic "append" >> $slog
append "off"  >> $slog
done

logt "Done"
