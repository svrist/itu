import sys
import re 
import csv
from optparse import OptionParser
from flot_graphs import FlotWriter, FlotGraph


parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="write report to FILE",
                  metavar="FILE", default="graph.js")
parser.add_option("-c", "--correct", type="float", dest="correct",
                  default=15002703317.0, help="What is the correct value")

parser.add_option("-n", "--name",  dest="experiment_name",
                  default="DB2 Experiment", help="Overnall Title of the experiment")

parser.add_option("--tpu","--throughput-unit",dest="tpu",default="sums/s",
                  help="What should the y-axis on the throughput have as unit?")
parser.add_option("--tpd","--throughput-decimals",dest="tpd",default=2,type="int",
                  help="How many decimals should the ticks on the y-axis on the throughput graph?")

(opt, args) = parser.parse_args(sys.argv)
args.pop(0)



if len(args) < 1:
    raise Exception("at least two arguments is needed")

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
wr.setup_axis(graphname="correct",axis="y",unit='%',scale=10,decimals=0,max=1)
wr.setup_axis(graphname="avg",axis="y",unit=opt.tpu,decimals=opt.tpd)

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


wr.flush(datanames=["UR","CS","RS","RR"],experimentname=opt.experiment_name)
