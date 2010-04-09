#!/bin/bash

. setup.bash
base=cover
setup
nodd=1
load=1
nogentable=1

sql="query_multipoint.sql"
extp="-r 1 -a5 -q 75"

logt "Basic, no index"
reads "noindex" $sql "$extp" >> $slog
logt "GoodCover index"
reads "goodcov" $sql "$extp" "good_covering_index.sql">> $slog
logt "BadCover index index"
reads "badcov" $sql "$extp" "bad_covering_index.sql">> $slog
logt "NonClustering index -q$q"
reads "nclust$q" $sql "$extp" "indexNC.sql">> $slog
logt "Clustering index -q$q"
reads "clust$q" $sql "$extp" "indexC.sql">> $slog
logt "Done"
