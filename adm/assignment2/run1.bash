#!/bin/bash

. setup.bash
base=run1
setup

logt "Threads experiments"
change_param "LOGBUFSZ" 256 >> $slog
logt "Threads 10"
basic "exp$dd/threads10" 10 >> $slog

logt "Threads 5"
basic "exp$dd/threads5" 5 >> $slog

logt "Threads 3"
basic "exp$dd/threads3" 3 >> $slog

logt "Threads 2"
basic "exp$dd/threads2" 2 >> $slog

logt "Threads 1"
basic "exp$dd/threads1" 1 >> $slog

logt "Threads 20"
basic "exp$dd/threads20" 20 >> $slog

logt "Table clustered index"
basic "exp$dd/indexclust" 10 5 "initpctfree.sql" >> $slog

logt "Table nopk index"
basic "exp$dd/indexnopk" 10 5 "initnopk.sql" >> $slog

logt "Append On experiment"
append "on" >> $slog
basic "exp$dd/append" >> $slog
append "off"  >> $slog

####
logt "Logbufsz 1024 experiment"
change_param "LOGBUFSZ" 1024 >> $slog
basic "exp$dd/logbuf" >> $slog
change_param "LOGBUFSZ" 256 >> $slog


logt "CHNGPGS_THRES experiment 85"
change_param "CHNGPGS_THRESH" 85 >> $slog
basic "exp$dd/chngpgs_thresh" >> $slog
change_param "CHNGPGS_THRESH" 60  >> $slog

logt "Done"
