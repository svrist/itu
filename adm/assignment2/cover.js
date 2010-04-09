/*
 * cover-exp1270812343/badcov.reads:73.4637069702
 * cover-exp1270812343/clust.reads:32.6090970039
 * cover-exp1270812343/goodcov.reads:2.76852202415
 * cover-exp1270812343/nclust.reads:161.660966158
 * cover-exp1270812343/noindex.reads:126.342866182
 *
 * cover-exp1270813319/badcov.reads:8.67679905891
 * cover-exp1270813319/clust.reads:4.69936609268
 * cover-exp1270813319/goodcov.reads:1.3845949173
 * cover-exp1270813319/nclust.reads:4.93899393082
 * cover-exp1270813319/noindex.reads:17.0445811749
*/
  var count=75
$(function () { 
 var cover = [ [1,count/1.3845949173]];
 var badcover = [ [3,count/8.67679905891 ]];
 var nclust = [ [ 5, count/4.93899393082 ]];
 var clust = [[ 7, count/4.69936609268]];

var labels= [ "Cover","BadCov","NClust","Clust" ];

$.plot($("#logb"), [
 { label: "cover", data: cover ,
points: { show: false, },
lines: { show: false, steps: false },
bars: { show: true, }, },

 { label: "badcover", data: badcover ,
points: { show: false, },
lines: { show: false, steps: false },
bars: { show: true, }, },

 { label: "nclust", data: nclust ,
points: { show: false, },
lines: { show: false, steps: false },
bars: { show: true, }, },

 { label: "clust", data: clust ,
points: { show: false, },
lines: { show: false, steps: false },
bars: { show: true, }, },

 ],
{
yaxis:{
 tickFormatter: function(v,axis){ return (v*1).toFixed(1)+" q/s"
},
},
legend:{show:false},
xaxis:{
min: 0,
max: 9,
ticks:[[0,""],
   [1.5, labels[0]], 
   [3.5,labels[1]],
   [5.5, labels[2]],
   [7.5, labels[3]],
     ],
tickSize: 1,
tickFormatter: function(v,axis){ return ":"+labels[v]+"l" },
 },
}
);
});

$(document).ready(function() { 
                        $("#title").html(
                                         "Assignment 2 - Part2c - Covering Index"
                                        );
                  });

var graphs = [ ["logb","Covering Index","reads.py -q "+count+" -r1 query_multipoint.sql" ]];

