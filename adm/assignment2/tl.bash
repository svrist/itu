#!/bin/bash

. setup.bash
base=tl
setup

nums=100000
t=1 
logt "Without TL - insert $t"
basic "withouttlins-t$t" $t 1  >> $slog

tl=1
logt "With TL - insert $t"
basic "withtlins-t$t" $t 1  >> $slog

logt "With TL - update $t"
update "withtlup-t$t" $t 1  >> $slog
unset tl

logt "Without TL - update $t"
update "withouttlup-t$t" $t 1  >> $slog



logt "Done"


