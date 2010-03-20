#!/bin/bash

. cold.sh

function get_snapshots()
{
  local logfile=$1
  #db2 connect to tuning > /dev/null
  db2 -v "get snapshot for dbm" > $logfile
  db2 -v "get snapshot for all databases">> $logfile
  db2 -v "get snapshot for all bufferpools">> $logfile
  db2 -v "get snapshot for all tables" >> $logfile
}

function set_snapshots()
{
  local logfile=$1
  db2 -v update monitor switches using bufferpool on lock on uow on sort on table on timestamp on statement on
  db2 -v get monitor switches > $logfile
  db2 -v reset monitor all
}

function basic()
{
  local logfile=$1
  local threads=$2
  if [ "x${threads}x" = "xx" ]; then
    threads=10
  fi
  local runs=$3
  if [ "x${runs}x" = "xx" ]; then 
    runs=5
  fi

  local init=$4
  if [ x${init}x = xx ]; then
    init="init.sql"
  else
    echo "Using $init as table"
  fi
  cold $init

  set_snapshots "$logfile.setsnap"
  db2 -v "get db cfg for tuning" > $logfile.dbcfg
  echo "Starting script..."
  python profwrites2.py -n 100000 -r $runs -t  $threads 2>&1 > $logfile.writes
  get_snapshots "$logfile.snapshots"
}

function change_param()
{
  local param=$1
  local value=$2
  echo $1 $2
  db2 -v "update db cfg for tuning using $param $value"
}


function append()
{
  local start=$1
  db2 -v alter table accounts append $start
}


dd=`date "+%s"`
mkdir exp$dd

function logt()
{
  local now=`date`
  echo "$now: $1" >> $slog
  echo $1
}

slog="exp$dd/script.log"
logt "Starting exp$dd experiments"



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
