#!/bin/bash

. setup.bash
base=logb
setup
sql=qs.sql
nogentable=1
load=1
nodd=1

logt "basic"
db2b "basic" $sql >> $slog


logt "Logb 128"
change_param LOGBUFSZ 128
db2b "logb128" $sql >> $slog
change_param LOGBUFSZ 256

logt "npages"
alter_bufferpool 4096
db2b "bufferp4096" $sql >> $slog
alter_bufferpool automatic
db2b "bufferpAuto" $sql >> $slog

logt "Prefetch"
alter_tablespace_prefetch 5K
db2b "prefetch5K" $sql >> $slog

alter_tablespace_prefetch 50K
db2b "prefetch50K" $sql >> $slog
alter_tablespace_prefetch 1000M
db2b "prefetch1G" $sql >> $slog
alter_tablespace_prefetch 10M
db2b "prefetch10M" $sql >> $slog
alter_tablespace_prefetch automatic

logt "Clustering index"
db2b "clustindex" $sql indexC.sql >> $slog


logt "Covering index"
db2b "coverindex" $sql bad_covering_index.sql >> $slog
db2expln -d tuning -t -terminator ";" -f $sql > logb-exp$dd/covindex.expln


logt "Done"
