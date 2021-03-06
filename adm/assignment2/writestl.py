#!/usr/bin/env python
# encoding: utf-8
"""
DB2/LogIO/experiment.py

A database must exist and be initialized before the experiment can be run 
(table and index creation in init.sql), data should be loaded (load.sql), 
and the database should be cleant up afterwards (cleanup.sql).

The database parameters are obtained from ../db2.py

Copyright (c) Philippe Bonnet 2010 . All rights reserved.
"""

import sys
import getopt
import timeit
import multiprocessing
import random
import os
import re
import ibm_db
import time
from string import maketrans

### Experiment parameters (default values)
NBRUNS         = 5    # Number of runs
NBTHREADS      = 10   # Number of threads 
ISOL_LEVEL     = 'RR'
WRITE_MODE     = 'insertN' # Write mode (insert or update)
TRANS_MODE     = '1'      # Transaction mode (1 or N) 
NBWRITES       = 1000
NBTUPLES       = 1000000
SPECFILE       = 'accountspec'
NBKEYS         = 1
ATTLIST        = []
TL             = False

### Database parameters (DATABASE; HOSTNAME; PORT; USERNAME; PASSWORD)
sys.path.append("..")
from db2 import DATABASE
from db2 import HOSTNAME
from db2 import PORT
from db2 import USERNAME
from db2 import PASSWORD

# Process Manager data structure
q = None
w = None
l = None

""""
Write threads for updateN and insertN
"""
def write(q,index,mutex):
    # initialize vars
    write_str  = q[0]
    matchList  = re.findall('\?', write_str)
    nbParams   = len(matchList)
    write_data = q[1]
    # Connect to DB
    conn = ibm_db.pconnect(DATABASE, USERNAME, PASSWORD)
    if conn is None: raise Usage(ibm_db.conn_errormsg())
    ibm_db.autocommit(conn,ibm_db.SQL_AUTOCOMMIT_OFF)
    # Set isolation level
    ret = ibm_db.exec_immediate(conn, "SET CURRENT ISOLATION = "+ISOL_LEVEL)
    ret2 = None
    if TL:
        ret2 = ibm_db.exec_immediate(conn, "LOCK TABLE accounts in exclusive mode")
        print "Lock: %s"%ret
    # Prepare Statements
    write_stmt = ibm_db.prepare(conn, write_str)
    if (write_stmt == False): raise Usage("Failed to prepare write statement")
    # Perform insertions/updates
    for i in range(NBWRITES/NBTHREADS):
        mutex.acquire()
        v = index.value
        index.value -= 1
        mutex.release()
        t = write_data.getWrite(v)
        if v >= 0 and t != None:
            # execute insertN statement
            if (WRITE_MODE == 'insertN'):
                if ibm_db.execute(write_stmt, t) == False:
                    raise Usage("Failed to execute insertN statement")
            elif (WRITE_MODE == 'updateN'):
                l = list(t)
                u = [l[j] for j in range(len(l)) if j in ATTLIST]
                if ibm_db.execute(write_stmt, tuple(u)) == False:
                    raise Usage("Failed to execute updateN statement")              
            if (TRANS_MODE == 'N'):
                print "commit"
                ibm_db.commit(conn)
    if (TRANS_MODE == '1'):
        print "commit"
        ibm_db.commit(conn)
    # Disconnect from DB
    status = ibm_db.close(conn)
    if status == False: raise Usage("Failed to close db connection.\n") 


def update1(q):
    write_str = q[0]
    # Connect to DB
    conn = ibm_db.pconnect(DATABASE, USERNAME, PASSWORD)
    if conn is None: raise Usage(ibm_db.conn_errormsg())
    ibm_db.autocommit(conn,ibm_db.SQL_AUTOCOMMIT_OFF)
    # Set isolation level
    ret = ibm_db.exec_immediate(conn, "SET CURRENT ISOLATION = "+ISOL_LEVEL)
    # Prepare statement
    write_stmt   = ibm_db.prepare(conn, write_str)
    if (write_stmt == False): raise Usage("Failed to prepare sum query")
    # Execute statement
    if ibm_db.execute(write_stmt) == False:
        raise Usage("Failed to execute the sum query")
    ibm_db.commit(conn)
    # Disconnect from DB
    status = ibm_db.close(conn)
    if status == False: raise Usage("Failed to close db connection.\n") 

"""
Gentable class
"""
class GenWrites(object):
    def __init__(self, numrows, numkeys, numwrites, specfile):
        self.numrows   = numrows
        self.numkeys   = numkeys
        self.numwrites = numwrites
        # Extract columns specifications from specfile
        print "reading specfile..."
        f = open(specfile)
        filelines = f.readlines()
        alllines = [(l.strip()).translate(maketrans("",""),"\n") for l in filelines if len(l.translate(maketrans("",""),"\n")) >1] # remove empty lines
        lines = [ll for ll in [l for l in alllines if l[0]!='/'] if ll[0]!=' ']   # remove comments
        colspecs = [l.split(' ') for l in lines]
        numcols = len(colspecs) 
        # Generate Table based on columns specifications
        print "generating rows..."
        self.writes = self.gentable(numcols, colspecs)
        
    def getWrite(self,cursor):
        if cursor < 0: return None
        elif cursor >= len(self.writes) : return None
        else:
            return self.writes[cursor]
        
    def sample_wr(self,population, k):
        # Chooses k random elements (with replacement) from a population
        n = len(population)
        _random, _int = random.random, int  # speed hack 
        result = [None] * k
        for i in xrange(k):
            j = _int(_random() * n)
            result[i] = population[j]
        return result

    def gentable(self,numcols, colspecs):
        attvalues     = [[]]*numcols
        schema   = [[]]*numcols
        i = 0
        while i < numcols:
            # spec is of the form -- attribute draw basevalue distribution
            # for now we ignore distribution
            spec = colspecs[i]
            attribute = spec[0]
            draw = float(spec[1])
            basevalue = 0
            if len(spec)>2:
                basevalue = int(spec[2])
            # generate the numbers used to generate attribute values
            if draw == 1:
                numlist = random.sample(range(self.numrows),self.numwrites)
            # for now we assume uniform distribution        
            elif draw < 1:
                numvalues = int(round(self.numrows*draw, 0))
                numlist   = self.sample_wr(range(numvalues), self.numwrites)
            elif draw > 1:
                numvalues = int(round(draw, 0))
                if numvalues >= self.numwrites:
                    numlist = random.sample(range(numvalues),self.numwrites)
                else:
                    numlist = self.sample_wr(range(numvalues),self.numwrites)
            # adjust list of numbers to account for basevalue   
            numlist = [num+basevalue for num in numlist]        
            # distinction between numerical attributes 'n' and alphanumerical attributes ATT_NAME
            if attribute == 'n':
                att = ''
                s = 'numeric'
                attvalues[i] = [num for num in numlist] 
            else:
                att = attribute
                s = 'varchar('+str(max(numlist))+')'   
                attvalues[i] = [att+str(num) for num in numlist]    
            # record schema
            schema[i] = s
            i += 1
        # remove duplicates for the key values
        if self.numkeys == numcols:
            # - use sets to eliminate duplicates
            tuples = zip(*attvalues)
            writes = set(tuples)
        elif self.numkeys < numcols:
            # - use dictionary to eliminate duplicates
            keys = zip(*attvalues[:self.numkeys])
            rest = zip(*attvalues[self.numkeys:])
            dico = dict(zip(keys,rest))
            writes = set([k+v for k,v in dico.items()])
        else:
            print "error in specfile: numkeys > numcols\n"
            system.exit(2)
        print "done generating rows..."
        return list(writes)
           

"""
Thread wrapper class
"""
class Thread(multiprocessing.Process):
    def __init__(self, target, *args):
        multiprocessing.Process.__init__(self, target=target, args=args)
        self.start()
    
def experiment(q,w,l):
    ThreadL = []
    
    if (WRITE_MODE == 'update1'):
        # Launch update1 statement
        update1(q)
    else:
        # Launch write threads
        for n in range(NBTHREADS):
            ThreadL.append(Thread(write,q,w,l))
        # Barrier
        for t in ThreadL:
            t.join()



help_message = '''
python writes.py [options]
options:
-h, --help       : this help message
-t, --threads=   : number of threads (1..59)
-n, --n=         : number of insertion/updates (in insertN/updateN modes)
-r, --runs=      : number of repetitions (< 100)
-i, --isol=      : isolation level ('UR', 'CS', 'RS','RR')
-w, --write=     : write mode ('insertN', 'update1', 'updateN')
-x, --trans=     : transaction mode (all writes wrapped in '1' or 'N' transactions)
-s, --specfile=  : specification file (gentable format)
-k, --numkeys=   : number of keys in specification file
-m, --numtuples= : max number of tuples in specification file (should be greater than -n)
-a, --attribute= : position of the attribute referenced in update file (multiple -a considered in order)
Executes writes against the database described in ../db2.py and prints timing 

Examples: 
python writes.py -t10 -r1 -iCS --write=insertN -x1 -n10000
python writes.py -t1 -r1 -iRR -wupdateN -xN -n1000 -a2 -a0
'''

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    global NBRUNS, NBTHREADS, ISOL_LEVEL, WRITE_MODE, TRANS_MODE
    global NBWRITES, NBTUPLES, SPECFILE, NBKEYS, ATTLIST, TL
    global q, w, l

    # Initialize variables
    n = 0
    specfile = ""
    numkeys = 0

    try:
        if argv is None:
            argv = sys.argv

        try:
            opts, args = getopt.getopt(argv[1:], 
                    "hvlr:t:i:w:x:n:s:k:m:a:", 
            ["help", "runs=","threads=", "isol=", "write=", "trans=", "n=", 
              "specfile=", "numkeys=", "numtuples=", "tablelock","attribute="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # Option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-r", "--runs"):
                v = int(value)
                if not (v < 100): raise Usage("Runs out of bounds")
                NBRUNS = v
            if option in ("-t", "--threads"): 
                v = int(value)
                if (v < 0 or v>60): raise Usage("Threads out of bounds")
                NBTHREADS = v
            if option in ("-i", "--isol"):
                if not value in ['UR', 'CS', 'RS', 'RR']: raise Usage("Isolation level not supported")
                ISOL_LEVEL = value
            if option in ("-w", "--write"):
                if not value in ['insertN', 'update1', 'updateN']: raise Usage("Write mode not supported (insertN, update1 or updateN)")
                WRITE_MODE = value
            if option in ("-x", "--trans"):
                if not value in ['1', 'N']: raise Usage("Transaction mode not supported (1 or N)")
                TRANS_MODE = value
            if option in ("-n", "--n"): 
                v = int(value)
                if (n < 0 or n>1000000): raise Usage("N out of bounds")
                NBWRITES = v
            if option in ("-s", "--specfile"):
                if not os.path.exists(value): raise Usage("Spec file does not exist")
                SPECFILE = value
            if option in ("-k", "--numkeys"):
                v = int(value)
                NBKEYS = v
            if option in ("-m", "--numtuples"):
                v = int(value)
                NBTUPLES = v
            if option in ("-a","--attribute"):
                v = int(value)
                ATTLIST.append(v)
            if option in ("-l","-tablelock"):
                TL = True

        # Verify preconditions: modes are compatible, required sql files exist
        if (WRITE_MODE == 'update1'): TRANS_MODE = '1'  

        write_str = None
        if (WRITE_MODE == 'insertN'):
            try:
                f = open('insertN.sql', 'r')
                write_str = f.readline()
                f.close()
            except IOError, e:
                raise Usage("Failed to open insertN.sql.\n")
        if (WRITE_MODE == 'update1'):
            try:
                f = open('update1.sql', 'r')
                write_str = f.readline()
                f.close()
            except IOError, e:
                raise Usage("Failed to open update1.sql.\n")    
        if (WRITE_MODE == 'updateN'):   
            try:
                f = open('updateN.sql', 'r')
                write_str = f.readline()
                f.close()
            except IOError, e:
                raise Usage("Failed to open updateN.sql.\n")
        if (write_str == None): raise Usage("Failed to read from SQL file") 
        
        print ('run (isol: '+ISOL_LEVEL+', threads: '+str(NBTHREADS)+', n: '+str(NBWRITES)+
               ', write_mode:'+WRITE_MODE+', trans_mode:'+TRANS_MODE+', tablelock:'+str(TL)+')')

        # Manager Initialization
        g = GenWrites(NBTUPLES, NBKEYS, NBWRITES, SPECFILE)
        
        manager = multiprocessing.Manager()
        q = manager.list([write_str,g])
        w = manager.Value('i', NBWRITES-1)
        l = manager.Lock()
        
        # Timed experiment 
        print "Starting experiment ..."
        t = timeit.Timer("experiment(q,w,l)", "from __main__ import experiment,q,w,l")
        timings = []
        try:
            # repeat 1 experiment NBRUNS time - output is a list of timing
            timings = t.repeat(NBRUNS,1)  
            print "Done."  
            # Log timing
            for timing in timings:
                s = str(timing)
                print s 
        except:
            raise Usage(t.print_exc())      

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())

