import sys
import re

class FlotGraph:
    def __init__(self,name,size=(800,450),pname=None):
        self.size=size
        self.datalines = []
        self.data = {}
        self.name = name
        self.axisd = {}
        self.axisd['x']= {}
        self.axisd['y'] = {}
        self.addinfo =""
        if pname is None:
            self.pname = name
        else:
            self.pname = pname

    def axis(self,xy,unit,scale=1,decimals=0,min=None,max=None):
        self.axisd[xy] = {'tickFormatter':"function(v,axis){ return (v*%d).toFixed(%d)+\" %s\"}"%(scale,decimals,unit)}
        if min:
            self.axisd[xy]['min'] = min
        if max:
            self.axisd[xy]['max'] = max

    def setup_data(self,name,type="line",points=True,axis=1,steps=False,bars=False):
        self.datalines.append( { 'name':name,'lines':'true','points':'true',
                                'bars': 'false','data':[], 'axis':axis,'steps':str(steps).lower()} )
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
        self.datasetup = {}
        self.oc ={}
        self._addinfo = {}
        for d in whitelist:
            self.data[d] = {}
            self.oc[d] = []
            self.datasetup[d]= {}
            self.pname[d] = d
        self.log = (lambda x : sys.stderr.write("%s\n"%x))
        self.filename = filename
        self.axissetup = {}
        self.pname = {}

    def pretty_name(self,name,pretty_name):
        self.pname[name] = pretty_name
        self.data[name] = {}
        self.oc[name] = []
        self.datasetup[name] = {}

    def addinfo(self,graphname,addinfo):
        self._addinfo[graphname] = addinfo

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

    def setup_data(self,graphname,dataname,**kwargs):
        self.datasetup[graphname][dataname]  = kwargs

    def write_data(self,graphname,dataname,data,**kwargs):
        if self.wannawrite(graphname):
            self.data[graphname][dataname] = data
            self.oc[graphname].append(dataname)

    def write(self,graphname,dataname,row):
        if self.wannawrite(graphname):
            if not dataname in self.data[graphname]:
                self.data[graphname][dataname] = []
                self.oc[graphname].append(dataname)
            self.data[graphname][dataname].append(row)

    def flush(self, datanames,experimentname):
        from Cheetah.Template import Template
        from flot import flot
        t = flot()
        #setup data

        graphs = {}
        for graphname,data in self.data.items():
            if not graphname in graphs:
                g = FlotGraph(name=graphname,pname=self.pname[graphname])
                if graphname in self._addinfo:
                    g.addinfo = self._addinfo[graphname]
                for i in self.oc[graphname]:
                    ds = self.datasetup[graphname][i]
                    g.setup_data(i,**ds)
                if graphname in self.axissetup:
                    axs = self.axissetup[graphname]
                    for axis in ['x','y','y2']:
                        if axis in axs:
                            a = axs[axis]
                            g.axis(axis,**a)
                graphs[graphname] = g
            else:
                g = graphs[graphname]
            for dataname,rawdata in [ (d,data[d]) for d in self.oc[graphname] ]:
                rawdata.sort()
                g.add_data(dataname,rawdata)
            g.remove_empty_data()

        t.graphs = graphs
        t.experiment_name = experimentname
        f = open("%s"%(self.filename),"w")
        f.write(str(t))
        f.close()
