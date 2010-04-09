#!/bin/bash

. setup.bash
base=run1rr
setup
script=profwrites2.py
nodd=1
runs=2
nogentable=1

for t in 1 2 5 10 25 50
do
logt "Threads $t compress"
basic "threads-compress$t" $t $runs "init-compress.sql" >> $slog
logt "Threads $t"
basic "threads$t" $t $runs "init.sql" >> $slog

logt "Table clustered index - t$t compress"
basic "indexclust-compress-t$t" $t $runs "initpctfree-compress.sql" >> $slog
logt "Table clustered index - t$t"
basic "indexclust-t$t" $t $runs "initpctfree" >> $slog

logt "Table nopk index - t$t compress"
basic "indexnopk-compress-t$t" $t $runs "initnopk-compress.sql" >> $slog
logt "Table nopk index - t$t"
basic "indexnopk-t$t" $t $runs "initnopk.sql" >> $slog
done

logt "Done"
