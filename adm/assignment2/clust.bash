#!/bin/bash

. setup.bash
base=clust
setup

sql="query_multipoint.sql"
extp="-r 10 -a5 -q 500"

logt "Basic, no index"
reads "noindex" $sql "$extp" >> $slog
logt "Clustering index"
reads "clust" $sql "$extp" "indexC.sql">> $slog

logt "NonClustering index"
reads "nclust" $sql "$extp" "indexNC.sql">> $slog

logt "Done"
