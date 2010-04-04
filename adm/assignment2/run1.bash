#!/bin/bash

. setup.bash
base=run1
setup
script=profwrites2.py
nodd=1
runs=2

logt "Threads experiments"
change_param "LOGBUFSZ" 256 >> $slog
logt "Threads 10"
basic "threads10" 10 $runs >> $slog

logt "Threads 5"
basic "threads5" 5 $runs >> $slog

logt "Threads 3"
basic "threads3" 3 $runs>> $slog

logt "Threads 2"
basic "threads2" 2 $runs>> $slog

logt "Threads 1"
basic "threads1" 1 $runs >> $slog

logt "Threads 20"
basic "threads20" 20 $runs >> $slog

for t in 1 2 5 10 25 50
do
logt "Table clustered index - t$t"
basic "indexclust-t$t" $t $runs "initpctfree.sql" >> $slog

logt "Table nopk index - t$t"
basic "indexnopk-t$t" $t $runs "initnopk.sql" >> $slog

logt "Append On experiment - t$t"
append "on" >> $slog
basic "appendt$t" $t $runs >> $slog
append "off"  >> $slog
done

logt "Done"
