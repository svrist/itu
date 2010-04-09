#!/bin/bash

. setup.bash

base="run2"

setup
script=profwrites2.py
nodd=1

logt "NLI"
nli >>  $slog
basic "nli" >> $slog

exit


####
logt "Logbufsz 512 experiment"
change_param "LOGBUFSZ" 512 >> $slog
basic "logbuf512" >> $slog

logt "Logbufsz 1024 experiment"
change_param "LOGBUFSZ" 1024 >> $slog
basic "logbuf1024" >> $slog

logt "Logbufsz 2048 experiment"
change_param "LOGBUFSZ" 2048 >> $slog
basic "logbuf2048" >> $slog
change_param "LOGBUFSZ" 256 >> $slog
logt "CHNGPGS_THRES experiment 5"
change_param "CHNGPGS_THRESH" 5 >> $slog
basic "chngpgs_thresh5" >> $slog

logt "CHNGPGS_THRES experiment 15"
change_param "CHNGPGS_THRESH" 15 >> $slog
basic "chngpgs_thresh15" >> $slog


logt "CHNGPGS_THRES experiment 30"
change_param "CHNGPGS_THRESH" 30 >> $slog
basic "chngpgs_thresh30" >> $slog

logt "CHNGPGS_THRES experiment 45"
change_param "CHNGPGS_THRESH" 45 >> $slog
basic "chngpgs_thresh45" >> $slog


logt "CHNGPGS_THRES experiment 85"
change_param "CHNGPGS_THRESH" 85 >> $slog
basic "chngpgs_thresh85" >> $slog

logt "CHNGPGS_THRES experiment 95"
change_param "CHNGPGS_THRESH" 95 >> $slog
basic "chngpgs_thresh95" >> $slog


change_param "CHNGPGS_THRESH" 60  >> $slog

logt "Done"
