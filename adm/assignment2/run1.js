/*
run1-exp1270727348/threads10.writes:17.1719839573
run1-exp1270727348/threads10.writes:19.019947052
run1-exp1270727348/threads1.writes:16.1229500771
run1-exp1270727348/threads1.writes:16.3319201469
run1-exp1270727348/threads20.writes:20.2362380028
run1-exp1270727348/threads20.writes:19.1382479668
run1-exp1270727348/threads2.writes:16.4309718609
run1-exp1270727348/threads2.writes:16.4152550697
run1-exp1270727348/threads3.writes:16.8854911327
run1-exp1270727348/threads3.writes:16.6536121368
run1-exp1270727348/threads5.writes:16.4321529865
run1-exp1270727348/threads5.writes:16.6112561226
*/

$(function () { 
var run1 = [[ 1, 16.1229500771], [2, 16.4309718609], [3,16.8854911327],
            [ 5, 16.4321529865], [ 10, 17.1719839573], [20, 20.2362380029]
            ];
$.plot($("#run1"), [ 
            {label: "Timing", data: run1 ,
points: { show: true, },
lines: { show: true, steps: false },
bars: { show: false, },
steps: { show: false, },
            },
 ],
{ 
yaxis:{ 
 tickFormatter: function(v,axis){ return (v*1).toFixed(0)+" s" },
},



xaxis:{
 tickFormatter: function(v,axis){ return (v*1).toFixed(0)+" thread(s)"
 },
}
}
);


      });

$(document).ready(function() { 
                        $("#title").html(
                                         "Assignment 1 -Part1a"
                                        );
                  });

var graphs = [ ["run1","Run1 graph","profwrites2.py -r 2 -t $t -n 100000" ]];

