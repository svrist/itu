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


function tablelocking()
{
  db2 -v alter table accounts locksize table
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

  if [ x$nocold = x ]; then
    cold $init
  else
    echo "No cold!"
  fi

  if [ ! x$tl = x ]; then
    echo "Tablelocking $nums $extraparms"
    local oldscript=$script
    local oldextra=$extraparams
    script="writestl.py"
    extraparams="$extraparams -l"
  fi



  set_snapshots "$logfile.setsnap"
  db2 -v "get db cfg for tuning" > $logfile.dbcfg
  echo "Starting script... $script $extraparams -n $nums -r $runs -t $threads 2>&1"
  python $script $extraparams -n $nums -r $runs -t  $threads 2>&1 > $logfile.writes
  get_snapshots "$logfile.snapshots"

  if [ ! x$tl = x ]; then
    script=$oldscript
    exraparams=$oldextraparams
  fi
}

function update()
{
  nocold=1
  extraparams="$extraparams -wupdateN -a0 -a2"
  basic $@
  unset nocold
  unset extraparams
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
  echo "===========================================================================" >> $slog
  echo "$now: $1" >> $slog
  echo "===========================================================================" >> $slog
  echo $1
}

function setup()
{
  dd=`date "+%s"`
  mkdir "${base}-exp$dd"
  slog="${base}-exp$dd/script.log"
  logt "Starting ${base}-exp$dd experiments"
}

function db2b()
{
  local logfile="${base}-exp$dd/$1"
  local sql=$2
  local index=$3


  if [ x$nocold = x ]; then
    cold init.sql "2500000 employees.data employeespec 1"
    if [ ! x${index}x = xx ]; then
      echo "Adding index: $index"
      db2 -vf $index
    fi
  else
    echo "No cold!"
  fi
  echo $sql
  db2batch -d tuning -f $sql -o r 0 p 5 > $logfile.batch
}

function alter_bufferpool()
{
  local size=$1
  db2 -v "alter bufferpool IBMDEFAULTBP size $size"
}

function alter_tablespace_prefetch()
{
  local size=$1

  db2 -v "alter tablespace USERSPACE1 PREFETCHSIZE $size"

}

function reads()
{
  local logfile="${base}-exp$dd/$1"
  local sql=$2
  local params=$3

  local index=$4

  if [ x$spec = x ]; then
    local spec=employeespec
  else
    echo "Spec: $spec"
  fi


  if [ x$nocold = x ]; then
    cold init.sql "1000000 employees.data $spec 1"

    if [ ! x${index}x = xx ]; then
      echo "Adding index: $index"
      db2 -vf $index
    fi
  else
    echo "No cold!"
  fi
  set_snapshots "$logfile.setsnap"
  db2 -v "get db cfg for tuning" > $logfile.dbcfg
  echo "Params: $params"
  python reads.py -p $sql $params > $logfile.reads
  get_snapshots "$logfile.snapshots"
}
