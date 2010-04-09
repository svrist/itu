 
/*
tl-exp1270398655/withouttlins-t1.writes:16.0936601162
tl-exp1270398655/withouttlup-t1.writes:18.5880742073
tl-exp1270398655/withtlins-t1.writes:16.2550151348
tl-exp1270398655/withtlup-t1.writes:18.5071351528
*/
$(function () { 
var ins = [ 
[1,16.0936601162],
[4,18.5071351528],
];
var labels= [ "Insert","Update" ];

var upd = [ 
[5,18.5880742073],
[2,16.2550151348],
            ];


$.plot($("#logb"), [
 { label: "With Rowlocking", data: ins ,
points: { show: false, },
lines: { show: false, steps: false },
bars: { show: true, },
            },
 { label: "With TableLocking", data: upd ,
points: { show: false, },
lines: { show: false, steps: false },
bars: { show: true, },
            },
 ],
{
yaxis:{
 tickFormatter: function(v,axis){ return (v*1).toFixed(1)+" s"
},
},
legend:{show:true},
xaxis:{
min: 0.5,
max: 6.5,
ticks:[[0,""],[2.0, labels[0]], [5.0,labels[1]]],
tickSize: 1,
 },
}
);
});

$(document).ready(function() { 
                        $("#title").html(
                                         "Assignment 1 -Part1b - Table Locking"
                                        );
                  });

var graphs = [ ["logb","Tablelocking graph","profwrites2.py -r 1 -t 1 -n 100000" ]];

