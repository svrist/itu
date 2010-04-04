#!/bin/bash

. setup.bash
base=tl
setup
script="profwrites2.py"
nodd=1

nums=100000
t=1
logt "Without TL - insert $t"
basic "withouttlins-t$t" $t 1  >> $slog

extraparams=" -l"
logt "With TL - insert $t"
basic "withtlins-t$t" $t 1  >> $slog

logt "With TL - update $t"
update "withtlup-t$t" $t 1  >> $slog
unset extraparams

logt "Without TL - update $t"
update "withouttlup-t$t" $t 1  >> $slog



logt "Done"


