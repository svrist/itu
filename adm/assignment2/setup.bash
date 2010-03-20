#!/bin/bash

. cold.sh

function get_snapshots()
{
  local logfile="$1"
  #db2 connect to tuning > /dev/null
  db2 -v "get snapshot for dbm" > $logfile
  db2 -v "get snapshot for all databases">> $logfile
 db2 -v "get snapshot for all bufferpools">> $logfile
  db2 -v "get snapshot for all tables" >> $logfile
}

function set_snapshots()
{
  local logfile="$1"
  db2 -v update monitor switches using bufferpool on lock on uow on sort on table on timestamp on statement on
  db2 -v get monitor switches > $logfile
  db2 -v reset monitor all
}

function basic()
{
  local logfile="${base}-exp$dd/$1"
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

  if [ x$script = x ]; then
    script="writes.py"
  else
    echo "Custom script: $script"
  fi

  if [ x$nums = x ]; then
    nums=100000
  fi
  cold $init

  set_snapshots "$logfile.setsnap"
  db2 -v "get db cfg for tuning" > $logfile.dbcfg
  echo "Starting script..."
  python profwrites2.py -n $nums -r $runs -t  $threads 2>&1 > $logfile.writes
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



function logt()
{
  local now=`date`
  echo "$now: $1" >> $slog
  echo $1
}

function setup()
{
  echo "Setup"
  dd=`date "+%s"`
  mkdir "${base}-exp$dd"
  slog="${base}-exp$dd/script.log"
  logt "Starting ${base}-exp$dd experiments"
}
