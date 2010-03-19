import sys
import re 

class FlotGraph:
    def __init__(self,name,size=(800,450)):
        self.size=size
        self.datalines = []
        self.data = {}
        self.name = name
        self.axisd = {}
        self.axisd['x']= {}
        self.axisd['y'] = {}

    def axis(self,xy,unit,scale=1,decimals=0,min=None,max=None):
        self.axisd[xy] = {'tickFormatter':"function(v,axis){ return (v*%d).toFixed(%d)+\" %s\"}"%(scale,decimals,unit)}
        if min:
            self.axisd[xy]['min'] = min
        if max:
            self.axisd[xy]['max'] = max

    def setup_data(self,name,type="line",points=True,axis=1):
        self.datalines.append( { 'name':name,'lines':'true','points':'true',
                                'bars': 'false','data':[], 'axis':axis} )
        self.data[name] = []
    def add_data(self,name,data):
        self.data[name] = data

    def remove_empty_data(self):
        for d in self.datalines[:]:
            if len(self.data[d['name']])==0:
                self.datalines.remove(d)
    def __contains__(self,other):
        return other in self.data

class FlotWriter:
    def __init__(self,filename,whitelist=['avg','correct']):
        self.data = {}
        for d in whitelist:
            self.data[d] = {}
        self.log = (lambda x : sys.stderr.write("%s\n"%x))
        self.filename = filename
        self.axissetup = {}

    def wannawrite(self,name):
        return name in self.data

    def setup_axis(self,graphname,axis='y',**kwargs):
        if not graphname in self.axissetup:
            self.axissetup[graphname] = {}
        if not axis in self.axissetup[graphname]:
            self.axissetup[graphname][axis] = {}
        brutto=['unit','scale','decimals','max']
        for b in brutto:
            if b in kwargs:
                self.axissetup[graphname][axis][b] = kwargs[b]

    def write(self,graphname,dataname,row):
        if self.wannawrite(graphname):
            if not dataname in self.data[graphname]:
                self.data[graphname][dataname] = []
            self.data[graphname][dataname].append(row)

    def flush(self, datanames):
        from Cheetah.Template import Template
        from flot import flot
        t = flot()
        #setup data

        graphs = {}
        for graphname,data in self.data.items():
            if not graphname in graphs:
                g = FlotGraph(name=graphname)
                for i in data.keys():
                    g.setup_data(i)
                if graphname in self.axissetup:
                    axs = self.axissetup[graphname]
                    for axis in ['x','y','y2']:
                        if axis in axs:
                            a = axs[axis]
                            g.axis(axis,**a)
                graphs[graphname] = g
            else:
                g = graphs[graphname]
            for isol,data in isoldata.items():
                data.sort()
                g.add_data(isol,data)
            g.remove_empty_data()

        t.graphs = graphs
        t.experiment_name = opt.experiment_name
        f = open("%s"%(self.filename),"w")
        f.write(str(t))
        f.close()
