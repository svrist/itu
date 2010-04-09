/*
run2-exp1270742391/nli.writes:18.839348793
run2-exp1270742391/nli.writes:18.6967220306
run2-exp1270742391/nli.writes:18.936560154
run2-exp1270742391/nli.writes:18.9449970722
run2-exp1270742391/nli.writes:18.777586937
run2-exp1270737100/logbuf1024.writes:19.5488131046
run2-exp1270737100/logbuf1024.writes:19.4801981449
run2-exp1270737100/logbuf1024.writes:19.8470439911
run2-exp1270737100/logbuf1024.writes:19.6160612106
run2-exp1270737100/logbuf1024.writes:19.7248709202
run2-exp1270737100/logbuf2048.writes:20.0630950928
run2-exp1270737100/logbuf2048.writes:20.2865560055
run2-exp1270737100/logbuf2048.writes:20.9441621304
run2-exp1270737100/logbuf2048.writes:20.3910160065
run2-exp1270737100/logbuf2048.writes:19.514619112
run2-exp1270737100/logbuf512.writes:19.5992619991
run2-exp1270737100/logbuf512.writes:19.5418980122
run2-exp1270737100/logbuf512.writes:19.5287148952
run2-exp1270737100/logbuf512.writes:19.3678359985
run2-exp1270737100/logbuf512.writes:19.5891480446
*/
$(function () { 
var data = [ [1,19.5992619991],
[3,19.5488131046],
[5,20.0630950928],
[7,18.6967220306] ];
var labels= [ "512","1024","2048","NLI" ];

$.plot($("#logb"), [
 { label: "Insert", data: data ,
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
legend:{show:false},
xaxis:{
min: 0,
max: 9,
ticks:[[0,""],[1.5, labels[0]], [3.5,labels[1]],[5.5, labels[2]], [7.5,labels[3]]],
tickSize: 1,
tickFormatter: function(v,axis){ return ":"+labels[v]+"l" },
 },
}
);
});

$(document).ready(function() { 
                        $("#title").html(
                                         "Assignment 1 -Part1a - Parameters"
                                        );
                  });

var graphs = [ ["logb","Parameters graph","profwrites2.py -r 2 -t $t -n 100000" ]];

