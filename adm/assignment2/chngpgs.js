/*
[5, 19.9584329128],
[15, 19.2846319675],
[30, 18.5253090858],
[45, 18.5863189697],
[85, 18.4113600254],
[95, 18.5010209084],
*/

$(function () { 
var ch = [
[5, 19.9584329128],
[15, 19.2846319675],
[30, 18.5253090858],
[45, 18.5863189697],
[85, 18.4113600254],
[95, 18.5010209084],
  ];

$.plot($("#chngpgs"), [ 
 {label: "Changed Pages %", data: ch ,
points: { show: true, },
lines: { show: true, steps: false },
bars: { show: false, },
steps: { show: false, },
            },
 ],
{ 
yaxis:{ 
 tickFormatter: function(v,axis){ return (v*1).toFixed(1)+" s" },
},

xaxis:{
 tickFormatter: function(v,axis){ return (v*1).toFixed(0)+" %"
 },
}
}
);


      });

$(document).ready(function() { 
                        $("#title").html(
                                         "Assignment 1 -Part1a - Index"
                                        );
                  });

var graphs = [ ["chngpgs","Changed Pages threshold graph","profwrites2.py -r 2 -t $t -n 100000" ]];

