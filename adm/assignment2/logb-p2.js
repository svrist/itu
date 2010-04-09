/*
 * logb-exp1270670347/basic.batch:* Total Time:                 5.850128 seconds
 * logb-exp1270670347/bufferp4096.batch:* Total Time:                 5.406438 seconds
 * logb-exp1270670347/bufferpAuto.batch:* Total Time:                 5.103133 seconds
 * logb-exp1270670347/clustindex.batch:* Total Time:                 5.207394 seconds
 * logb-exp1270670347/coverindex.batch:* Total Time:                12.575174 seconds
 * logb-exp1270670347/logb128.batch:* Total Time:                 5.460914 seconds
 * logb-exp1270670347/prefetch10M.batch:* Total Time:                16.240327 seconds
 * logb-exp1270670347/prefetch1G.batch:* Total Time:                 6.239254 seconds
 * logb-exp1270670347/prefetch50K.batch:* Total Time:                 5.787299 seconds
 * logb-exp1270670347/prefetch5K.batch:* Total Time:                 6.829259 seconds
*/
$(function () { 
var basic = [ [1,5.850128],];

var bufp = [ [ 3,5.406438],[4,5.103133] ];

var pref = [ [6, 6.829259],[7,5.787299],[8,16.240327],[9,6.239254] ];

var logb = [[11,5.460914]];
var indx = [[13,5.207394],[14,12.575174]];

var labels= [ "Baseline",
               "BP4096","BPAuto",
               "Pref5k","Pref50k","Pref10M","Pref1G",
               "LogBufSz128",
               "ClustIdx","CoverIdx"
               ];

$.plot($("#logb"), [
 { label: "basic", data: basic ,
points: { show: false, },
lines: { show: false, steps: false },
bars: { show: true, }, },

 { label: "bufp", data: bufp ,
points: { show: false, },
lines: { show: false, steps: false },
bars: { show: true, }, },

 { label: "pref", data: pref ,
points: { show: false, },
lines: { show: false, steps: false },
bars: { show: true, }, },

 { label: "logb", data: logb ,
points: { show: false, },
lines: { show: false, steps: false },
bars: { show: true, }, },

 { label: "indx", data: indx ,
points: { show: false, },
lines: { show: false, steps: false },
bars: { show: true, }, },

 ],
{
yaxis:{
 tickFormatter: function(v,axis){ return (v*1).toFixed(1)+" s"
},
},
legend:{show:false},
xaxis:{
min: 0,
max: 15,
ticks:[[0,""],
   [1.5, labels[0]], 
   [3.5,labels[1]],[4.5, labels[2]], 
   [6.5,labels[3]],[7.5,labels[4]],[8.5,labels[5]],[9.5,labels[6]],
   [11.5,labels[7]],
   [13.5,labels[8]],[14.5,labels[9]]
     ],
tickSize: 1,
tickFormatter: function(v,axis){ return ":"+labels[v]+"l" },
 },
}
);
});

$(document).ready(function() { 
                        $("#title").html(
                                         "Assignment 2 - Part2a - Reads I/o"
                                        );
                  });

var graphs = [ ["logb","Read I/O","db2batch" ]];

