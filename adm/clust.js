
/*
Clust
[1, 0.680012226105],
[10, 1.3481259346],
[50, 2.46350693703],
[100, 3.2929289341],
[200, 5.27281308174],
[500, 11.308701992],
[750, 17.111328125],
[999, 71.0981857777],

NClust
[1, 0.685930013657],
[10, 1.3826789856],
[50, 2.49335193634],
[100, 3.18051791191],
[200, 5.6206099987],
[500, 11.7382919788],
[750, 16.3037109375],
[999, 75.6675841808],

NoIndex
[1, 1.29030489922],
[10, 2.51378512383],
[50, 11.64772892],
[100, 24.704171896],
[200, 43.2236938477],
[500, 100.19040513],
[750, 152.133563995],
[999, 196.208170176],
*/

$(function () { 
  var clust = [
[1, 0.680012226105],
[10, 1.3481259346],
[50, 2.46350693703],
[100, 3.2929289341],
[200, 5.27281308174],
[500, 11.308701992],
[750, 17.111328125],
[999, 71.0981857777],
  ];

  var nclust = [
  [1, 0.685930013657],
  [10, 1.3826789856],
  [50, 2.49335193634],
  [100, 3.18051791191],
  [200, 5.6206099987],
  [500, 11.7382919788],
  [750, 16.3037109375],
  [999, 75.6675841808],
  ];

var noindex = [
[1, 1.29030489922],
  [10, 2.51378512383],
  [50, 11.64772892],
  [100, 24.704171896],
  [200, 43.2236938477],
  [500, 100.19040513],
  [750, 152.133563995],
  [999, 196.208170176],
  ];


function tp(arr){
  var ret = []
    for (v in arr){
      ret[v] = [arr[v][0], arr[v][0]/arr[v][1] ];
    }
  return ret;
}

/*var noindex2 = tp([noindex[3]]);
var nclust2= tp([nclust[3]]);
var clust2 = tp([clust[3]]);*/

var noindex2 = tp(noindex);
var nclust2= tp(nclust);
var clust2 = tp(clust);

$.plot($("#run1"), [ 
       {label: "No Index", data: noindex2 , 
points: { show: true, }, lines: { show: true, steps: false }, bars: { show: false, }, steps: { show: false, }, },

       {label: "Non clustering index", data: nclust2 , 
points: { show: true, }, lines: { show: true, steps: false }, bars: { show: false, }, steps: { show: false, }, },

       {label: "Clustering index", data: clust2 , 
points: { show: true, }, lines: { show: true, steps: false }, bars: { show: false, }, steps: { show: false, },
},
 ],
{ 
yaxis:{ 
 tickFormatter: function(v,axis){ return (v*1).toFixed(2)+" queries/s"}
},

xaxis:{
 tickFormatter: function(v,axis){ return (v*1).toFixed(0)+" queries"
 },
}
}
);


      });

$(document).ready(function() { 
                        $("#title").html(
                                         "Assignment 2 -Part2b- Clustering Index"
                                        );
                  });

var graphs = [ ["run1","Clustering Index","reads.py -r 1 -a5 -q $q" ]];

