#!/bin/bash

function cachebuster()
{
  echo "Writing cache buster"
  dd if=/dev/zero of=./cache_buster count=1755492 bs=1500 &
  ddpid=$!
  found=0
  while [ $found = 0 ]; do
    sleep 5
    pkill -USR1 -u db2inst1 ^dd$ 2>&1
    found=$?
  done
  wait $ddpid
  echo "Done busting cache. Cleaing up";
  if [ -f cache_buster ]; then
    rm cache_buster
  else
    echo "No cache_buster written?"
  fi
  sync
  sync
  sync
  sync
  sync
  sync
}

function cold()
{
  local init=$1
  if [ x${init}x = xx ]; then
    init="init.sql"
  fi

  local gentable=""
  if [ ! "x$2" = x ]; then
    gentable=$2
  fi

  db2 connect to tuning
  db2 -v "FLUSH PACKAGE CACHE dynamic"
  db2pdcfg -db tuning -flushbp
  echo "dropping table";
  db2 -vf cleanup.sql
  db2 -vtf $init
  if [ ! "x${gentable}" = x ]; then
    echo "Generating new table .data"
    echo $gentable
    python gentable.py $gentable
    load=1
  fi

  if [ ! x$load = x ]; then
    echo "Loading from load.sql"
    db2 -vf load.sql
  fi

  db2 terminate
  db2stop force
  sudo /etc/init.d/db2exc stop
  sudo umount /ebs/db2
  echo "Stopped db2 and unmounted /ebs/db2"
  if [ x${nodd}x = xx ]; then
    cachebuster
  fi
  sudo mount /dev/sdg1 /ebs/db2 
  sudo /etc/init.d/db2exc start
  db2 connect to tuning
}
