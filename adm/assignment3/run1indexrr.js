
/*
 *
run1rr-exp1270825999/indexclust-compress-t10.writes:22.7110610008
run1rr-exp1270825999/indexclust-compress-t10.writes:21.9688310623
run1rr-exp1270825999/indexclust-t10.writes:19.1647338867
run1rr-exp1270825999/indexclust-t10.writes:18.201748848
run1rr-exp1270825999/indexnopk-compress-t10.writes:20.7748699188
run1rr-exp1270825999/indexnopk-compress-t10.writes:20.0238790512
run1rr-exp1270825999/indexnopk-t10.writes:16.49229002
run1rr-exp1270825999/indexnopk-t10.writes:16.4757268429
run1rr-exp1270825999/threads10.writes:18.0744009018
run1rr-exp1270825999/threads10.writes:18.3764648438
run1rr-exp1270825999/threads-compress10.writes:22.5775411129
run1rr-exp1270825999/threads-compress10.writes:21.8363919258
*/

$(function () { 

var normal = [
[1,18.0744009018],
[4,16.49229002],
[7,19.1647338867]
];
var compress =[
[2,22.5775411129],
[5,20.7748699188],
[8,22.7110610008],
];
var labels= [ "Normal","NoPk","ClustPK" ];

$.plot($("#logb"), [
 { label: "Normal", data: normal ,
points: { show: false, },
lines: { show: false, steps: false },
bars: { show: true, }, },


 { label: "Compressed", data: compress ,
points: { show: false, },
lines: { show: false, steps: false },
bars: { show: true, }, },
 ],
{
yaxis:{
 tickFormatter: function(v,axis){ return (v*1).toFixed(1)+" s"
},
},
legend:{show:true},
xaxis:{
min: 0,
max: 10,
ticks:[[0,""],[1.5, labels[0]], [3.5,labels[1]],[5.5, labels[2]] ],
tickSize: 1,
tickFormatter: function(v,axis){ return ":"+labels[v]+"l" },
 },
}
);
});

$(document).ready(function() { 
                        $("#title").html(
                                         "Assignment 3 -Part2 - Writes Performance - Compress"
                                        );
                  });

var graphs = [ ["logb","Write performance row-compression","profwrites2.py -r 2 -t 10 -n 100000" ]];

