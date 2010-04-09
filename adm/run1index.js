
/*
[1, 16.0884299278],
[2, 16.2531318665],
[5, 16.7085270882],
[10, 17.3799421787],
[25, 19.5636370182],
[50, 23.4955589771],

appendmode
[1, 16.1559550762],
[2, 16.3467428684],
[5, 16.5900390148],
[10, 17.3757171631],
[25, 19.4317209721],
[50, 25.5764188766],
*/

$(function () { 
var indexclust = [
[1, 16.0884299278],
[2, 16.2531318665],
[5, 16.7085270882],
[10, 17.3799421787],
[25, 19.5636370182],
[50, 23.4955589771], ];
var noindex = [
[1, 15.15731287],
[2, 14.6075379848],
[5, 15.2076699734],
[10, 15.8784039021],
[25, 18.2642121315],
[50, 22.5277500153],
];
var pk = [[ 1, 16.1229500771], [2, 16.4309718609], [3,16.8854911327],
            [ 5, 16.4321529865], [ 10, 17.1719839573], [20, 20.2362380029]
            ];

var append =[
[1, 16.1559550762],
  [2, 16.3467428684],
  [5, 16.5900390148],
  [10, 17.3757171631],
  [25, 19.4317209721],
  [50, 25.5764188766],
  ];

$.plot($("#run1index"), [ 
 {label: "STD PK(baseline)", data: pk ,
points: { show: true, },
lines: { show: true, steps: false },
bars: { show: false, },
steps: { show: false, },
            },


            {label: "Clustering PK", data: indexclust ,
points: { show: true, },
lines: { show: true, steps: false },
bars: { show: false, },
steps: { show: false, },
            },
 {label: "No PK", data: noindex ,
points: { show: true, },
lines: { show: true, steps: false },
bars: { show: false, },
steps: { show: false, },
            },
 {label: "Append Mode", data: append ,
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
                                         "Assignment 1 -Part1a - Index"
                                        );
                  });

var graphs = [ ["run1index","Run1 graph","profwrites2.py -r 2 -t $t -n 100000" ]];

