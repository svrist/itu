#!/bin/bash

. setup.bash
base=select
spec=employeespec2
setup

nogentable=1
load=1

logt "Selectivity experiment"
for s in 0.3  0.8 1 2 3 5 7 10 15 20 25 27 29 30 35 40 50
do
  extp="-r 5 -q 10 -l"
  sql=query_range$s.sql
  logt "Sql: $sql"
  logt "Basic, no index - s$s"
  reads "noindex$s" $sql "$extp" >> $slog

  logt "NonClustering index -s$s"
  reads "nclust$s" $sql "$extp" "indexNC.sql">> $slog
done

logt "Done"
