#!/bin/bash

. setup.bash
base=clust
setup

sql="query_multipoint.sql"


for q in 1 10 50 100 200 500 750 999
do
extp="-r 1 -a5 -q $q"

logt "Basic, no index - q$q"
reads "noindex$q" $sql "$extp" >> $slog
logt "NonClustering index -q$q"
reads "nclust$q" $sql "$extp" "indexNC.sql">> $slog
logt "Clustering index -q$q"
reads "clust$q" $sql "$extp" "indexC.sql">> $slog
done

logt "Done"
