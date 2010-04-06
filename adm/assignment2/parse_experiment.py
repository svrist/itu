import sys
import re
import os
import glob
from datetime import datetime
from numpy import mean,isnan

from flot_graphs import FlotWriter

class experiments:
    """Overall container of all experiments parsed"""
    def __init__(self):
        self.exps = {}
        self.typemap = {}

    def __getitem__(self,k):
        name,time,dirname = k
        key = "%s%s"%(name,time)
        if not key in self.exps:
            self.exps[key] = experiment(name,time,dirname)
            if not name in self.typemap:
                self.typemap[name] = []
            self.typemap[name].append(key)
        return self.exps[key]

    def avg(self,type=None):
        pass


    def __str__(self):
        ret = []
        for t,keys in self.typemap.items():
            ret.append("%s:\n"%t)
            for e in [self.exps[d] for d in keys]:
                ret.append("\t%s\n"%e)
        return ''.join(ret)





class data:
    """ One data line for an experiment
    Contains aggregate functions for data
    """
    def __init__(self,type,select,count=0):
        self.count = count
        self._cold = 0
        self._hot = []
        self.type=type
        self.select=select
    def cold(self,timing=None):
        if not timing is None:
            self._cold = timing
        return self._cold

    def hot(self,timing=None):
        if timing:
            self._hot.append(timing)
        return self._hot

    def hotavg(self):
        return mean(self.hot())
        #return (sum(self.hot())/len(self.hot()))

    def coldtp(self):
        return float(self.count)/self.cold()

    def hottp(self):
        return float(self.count)/self.hotavg()

    def tp(self):
        return float(self.count)/mean([self.cold()]+self.hot())


    def __str__(self):
        return "(%s,%s)[cold: %f, hotavg: %f, tp:%f]"%\
    (self.type,self.select,self.cold(),self.hotavg(),self.tp())

class experiment:
    """ One specific experiment"""
    def __init__(self,name,time,dirname=None):
        self.name = name
        self.dirname = dirname
        self.time = datetime.utcfromtimestamp(float(time))
        self.data = {}
        self.typemap = {}
        self.selectmap = {}

    def _init_maps(self,indextype,selectivity):
        key = "%s-%s"%(indextype,selectivity)
        if not key in self.data:
            self.data[key] = data(indextype,selectivity)

            if not indextype in self.typemap:
                self.typemap[indextype] = []
            self.typemap[indextype].append(key)

            if not selectivity in self.selectmap:
                self.selectmap[selectivity] = []
            self.selectmap[selectivity].append(key)
        return self.data[key]

    def add(self,indextype,selectivity,file):
        d = self._init_maps(indextype,selectivity)
        f = open(file)
        cold = True
        for l in f:
            mtime = re.match("^([\d\.]+)$",l)
            mrc = re.match("^rc: ([\d\.]+)$",l)
            if mtime:
                timing = float(mtime.group(1))
                if cold:
                    d.cold(timing)
                    cold = False
                else:
                   d.hot(timing)
            elif mrc:
                timing = mrc.group(1)
                d.count = float(timing)
            else:
                #print "ignoring line: %s"%l
                pass


    """Helpermethod returning raw data for plotting
   Hot and cold data both
    """
    def tp_fun_of_selectivity(self,scale=10):
        ret = []

        for t,keys in self.typemap.items():
            dataline = { 'name':t+"_cold", 'data':[] }
            dataline['data'] = [ [self.data[k].select,self.data[k].coldtp()]\
                                for k in keys if not isnan(self.data[k].coldtp())]
            dataline['data'].sort()
            ret.append(dataline)
            dataline = { 'name':t+"_hot", 'data':[] }
            dataline['data'] = [ [self.data[k].select,self.data[k].hottp()]\
                                for k in keys if not isnan(self.data[k].hottp())]
            dataline['data'].sort()
            ret.append(dataline)
        return ret

    def __str__(self):
        ret = []
        ret.append("Experiment %s - %s:\n"%(self.name,self.time))
        for it in [self.typemap.items(),self.selectmap.items()]:
            for i,keys in it:
                ret.append("\t\t%s:\n"%i)
                for d in [ self.data[k] for k in keys ]:
                    ret.append("\t\t\t%s\n"%d)
        return ''.join(ret)


###############################################################################

typere = re.compile("(?:([^-]*)-exp(\d+)/)?([a-z]+)([\d.]+).reads")
"""Traverse file for data"""
def parse_file(f,exps):
        m = typere.match(f)
        if m:
            expname,exptime,type,select = m.groups()
            dirname = "%s-exp%s"%(expname,exptime)
            exps[expname,exptime,dirname].add(type,float(select),f)
        else:
            print "Unknown filename:  %s"%f

"""Traverse dir for files"""
def parse_dir(dir,exps):
    for f in glob.glob(os.path.join(dir,"*.reads")):
        parse_file(f,exps)

if __name__ == '__main__':
    exps = experiments()
    #To include flot.tmpl/flot.py
    sys.path.append("/ebs/home/ubuntu/itu/adm/assignment2")
    for f in sys.argv[1:]:
        if os.path.isdir(f):
            parse_dir(f,exps)
        elif os.path.isfile(f):
            parse_file(f)
        else:
            raise Exception("Unknown file/dir: %s"%f)
    g = FlotWriter("graph.js",whitelist=[])
    for gname,e in exps.exps.items():
        gname2 = "Experiment %s %s (%s)"%(e.name,e.time,e.dirname)
        g.pretty_name(gname,gname2)
        g.setup_axis(gname,axis='x',unit="%",decimals=1)
        print gname2
        tpofselect = e.tp_fun_of_selectivity()
        print "\t%d datalines"%len(tpofselect)
        for dl in tpofselect:
            g.setup_data(gname,dl["name"])
            g.write_data(gname,dl["name"],dl["data"])
            print "\t\t%s: %d values "%(dl["name"],len(dl["data"]))
    g.flush(None,"Part2d")

