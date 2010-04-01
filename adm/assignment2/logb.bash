#!/bin/bash

. setup.bash
base=logb
setup
sql=qs.sql

logt "Logb 128"
change_param LOGBUFSZ 128
db2b "logb128" $sql
change_param LOGBUFSZ 256

logt "npages"
alter_bufferpool 4096
db2b "bufferp4096" $sql
alter_bufferpool automatic
db2b "bufferpAuto" $sql

logt "Prefetch"
alter_tablespace_prefetch 10M
db2b "prefetch10M" $sql
alter_tablespace_prefetch 50K
db2b "prefetch50K" $sql
alter_tablespace_prefetch 1G
db2b "prefetch1G" $sql
alter_tablespace_prefetch automatic

logt "Clustering index"
db2b "clustindex" $sql indexC.sql


logt "Done"
