#!/bin/bash

. setup.bash
base=run1
setup

logt "Threads experiments"
change_param "LOGBUFSZ" 256 >> $slog
logt "Threads 10"
basic "gthreads10" 10 >> $slog

logt "Threads 5"
basic "gthreads5" 5 >> $slog

logt "Threads 3"
basic "gthreads3" 3 >> $slog

logt "Threads 2"
basic "gthreads2" 2 >> $slog

logt "Threads 1"
basic "gthreads1" 1 >> $slog

logt "Threads 20"
basic "gthreads20" 20 >> $slog

logt "Table clustered index"
basic "gindexclust" 10 5 "initpctfree.sql" >> $slog

logt "Table nopk index"
basic "gindexnopk" 10 5 "initnopk.sql" >> $slog

logt "Append On experiment"
append "on" >> $slog
basic "gappend" >> $slog
append "off"  >> $slog

####
logt "Logbufsz 1024 experiment"
change_param "LOGBUFSZ" 1024 >> $slog
basic "glogbuf" >> $slog
change_param "LOGBUFSZ" 256 >> $slog


logt "CHNGPGS_THRES experiment 85"
change_param "CHNGPGS_THRESH" 85 >> $slog
basic "gchngpgs_thresh" >> $slog
change_param "CHNGPGS_THRESH" 60  >> $slog

logt "Done"
