#!/bin/bash

. setup.bash

base="run2"

setup

####
logt "Logbufsz 512 experiment"
change_param "LOGBUFSZ" 512 >> $slog
basic "glogbuf512" >> $slog

logt "Logbufsz 1024 experiment"
change_param "LOGBUFSZ" 1024 >> $slog
basic "glogbuf1024" >> $slog

logt "Logbufsz 2048 experiment"
change_param "LOGBUFSZ" 2048 >> $slog
basic "glogbuf2048" >> $slog

change_param "LOGBUFSZ" 256 >> $slog


logt "CHNGPGS_THRES experiment 5"
change_param "CHNGPGS_THRESH" 5 >> $slog
basic "gchngpgs_thresh5" >> $slog

logt "CHNGPGS_THRES experiment 15"
change_param "CHNGPGS_THRESH" 15 >> $slog
basic "gchngpgs_thresh15" >> $slog


logt "CHNGPGS_THRES experiment 30"
change_param "CHNGPGS_THRESH" 30 >> $slog
basic "gchngpgs_thresh30" >> $slog

logt "CHNGPGS_THRES experiment 45"
change_param "CHNGPGS_THRESH" 45 >> $slog
basic "gchngpgs_thresh45" >> $slog


logt "CHNGPGS_THRES experiment 85"
change_param "CHNGPGS_THRESH" 85 >> $slog
basic "gchngpgs_thresh85" >> $slog

logt "CHNGPGS_THRES experiment 95"
change_param "CHNGPGS_THRESH" 95 >> $slog
basic "gchngpgs_thresh95" >> $slog


change_param "CHNGPGS_THRESH" 60  >> $slog

logt "Done"
