import sys
import re 
import csv
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="write report to FILE",
                  metavar="FILE", default="graph.js")
parser.add_option("-c", "--correct", type="float", dest="correct",
                  default=15002703317.0, help="What is the correct value")

parser.add_option("-n", "--name",  dest="experiment_name",
                  default="DB2 Experiment", help="Overall Title of the experiment")

parser.add_option("--tpu","--throughput-unit",dest="tpu",default="sums/s",
                  help="What should the y-axis on the throughput have as unit?")
parser.add_option("--tpd","--throughput-decimals",dest="tpd",default=2,type="int",
                  help="How many decimals should the ticks on the y-axis on the throughput graph?")

(opt, args) = parser.parse_args(sys.argv)
args.pop(0)



if len(args) < 1:
    raise Exception("at least two arguments is needed")

class Writer:

    def __init__(self,namemap={},delimiter=";",whitelist=None):
        self.namemap = namemap
        self.writers = {}
        self.delimiter=delimiter
        self.log = (lambda x : sys.stderr.write("%s\n"%x))
        self.whitelist = whitelist

    def write(self,type,isol,row):
        key = "%s%s"%(type,isol)

        if not self.wannawrite(type): return


        if not key in self.writers:
            if key in self.namemap:
                name = self.namemap[key]
            else:
                name = "%s-%s.csv"%(type,isol)
            self.log("init writer for %s: %s"%(key,name))
            self.writers[key] = {'data':[]}
            self.writers[key]['writer'] = csv.writer(open(name,'wb'),delimiter=self.delimiter)
        self.writers[key]['data'].append(row)

    def wannawrite(self,name):
       return (self.whitelist is None) or (name in self.whitelist)

    def flush(self):
       for k,v in self.writers.iteritems():
           v['data'].sort()
           for row in v['data']:
               v['writer'].writerow(row)

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

    def wannawrite(self,name):
        return name in self.data

    def write(self,type,isol,row):
        if self.wannawrite(type):
            if not isol in self.data[type]:
                self.data[type][isol] = []
            self.data[type][isol].append(row)

    def flush(self):
        from Cheetah.Template import Template
        from flot import flot
        t = flot()
        #setup data

        graphs = {}
        for type,isoldata in self.data.items():
            if not type  in graphs:
                g = FlotGraph(name=type)
                for i in ["UR","CS","RS","RR"]:
                    g.setup_data(i)
                if type == "correct":
                    g.axis('y',unit="%",scale=100,decimals=0,max=1)
                else:
                    g.axis('y',unit=opt.tpu,decimals=opt.tpd)

                graphs[type] = g
            else:
                g = graphs[type]
            for isol,data in isoldata.items():
                data.sort()
                g.add_data(isol,data)
            g.remove_empty_data()

        t.graphs = graphs
        t.experiment_name = opt.experiment_name
        f = open("%s"%(self.filename),"w")
        f.write(str(t))
        f.close()

def avg(vals):
    avg = (sum(vals,0.0)/len(vals))
    return avg

def correct(real,vals):
    l1 = [ 1 for v in vals if v==real ]
    return float(len(l1))/float(len(vals))

def sumcount(vals,min=1):
    ret = {}
    for v in vals:
        if v in ret:
            ret[v] += 1
        else:
            ret[v] = 1
    return dict([ (v,c) for v,c in ret.iteritems() if c > min])



funs= {'timing':{'avg': lambda x: avg(x)},
       'sum':{'sumcount': (lambda x:sumcount(x)) } }
funs['sum']['correct']=lambda x:correct(opt.correct,x)

namematch = re.compile("([^/-]+)-t(\d+)(..)\.txt")
mr = re.compile("\(?([\d\.]+),?\)?")
wr = FlotWriter(whitelist=["correct","avg"],filename=opt.filename)
for fname in args:
    m = namematch.search(fname)
    if not m is None:
        f = open(fname,'r')
        type,t,isol = m.group(1),m.group(2),m.group(3)

        vals = [ float(re.sub(mr,r'\1',l)) for l in f if re.match(mr,l)]
        if len(vals):
            for name,fu in funs[type].iteritems():
                calc = fu(vals)
                print "%s|%s-%s-%s: %s"%(name,type,isol.lower(),t,calc)
                if wr.wannawrite(name):
                    wr.write(name,isol,[int(t),calc])#("%f"%calc).replace(".",",")])
        else:
            print "No lines in %s"%fname
        f.close()
    else:
        raise Exception("Didnt match filename:%s"%fname)


wr.flush()
