#!/bin/bash
#ython run.py [options] #options:
#-h, --help       : this help message
#-t, --threads=   : number of swap threads (1..59)
#-s, --swaps=     : total number of swaps (< 1000) 
#-r, --runs=      : number of repetitions (< 100)
#-i, --isol=      : isolation level ('UR', 'CS', 'RS','RR')
#-o, --output=    : path to output file (result.txt)
dd=`date "+%s"`
if [ -d output ];then
echo "Moving old output to output-$dd"
mv output output-$dd
fi
mkdir output

run=12
s=100
isols=( CS RR )
threads=( 1 2 5 10 25 50 )
swaps=(   400 400 400 400 400 400 )

count=0
for t in ${threads[@]}
  do
    echo "Threads $t (run:$run, swaps:${swaps[$count]})"
    for i in ${isols[@]}
    do
    echo "Isolation $i (${swaps[$count]})"
    python origrun.py -r$run --threads=$t --isol=$i --swaps=${swaps[$count]} -o output/sum-t$t$i.txt 2>>runlog.log > output/timing-t$t$i.txt 
    date >> runlog.log
    sh clean.sh >> runlog.log
  done
  let count++
done
echo "Done. Exit"
