#!/bin/bash

. setup.bash
base=clustrerun
setup
nodd=1
load=1
nogentable=1

sql="query_multipoint.sql"


for q in 1 10 50 100 200 500 750 999
do
  extp="-r 1 -a5 -q $q"
  init="init.sql"
  logt "Basic, no index - q$q"
  reads "noindex$q" $sql "$extp" >> $slog
  logt "NonClustering index -q$q"
  reads "nclust$q" $sql "$extp" "indexNC.sql">> $slog
  logt "Clustering index -q$q"
  reads "clust$q" $sql "$extp" "indexC.sql">> $slog

  init="init-compress.sql"
  logt "Basic-compress, no index - q$q"
  reads "noindex-compress$q" $sql "$extp" >> $slog
  logt "NonClustering-compress index -q$q"
  reads "nclust-compress$q" $sql "$extp" "indexNC.sql">> $slog
  logt "Clustering-compress index -q$q"
  reads "clust-compress$q" $sql "$extp" "indexC.sql">> $slog
done

logt "Done"
