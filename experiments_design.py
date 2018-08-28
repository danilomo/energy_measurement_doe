#!/usr/bin/env python

import sys
import os
import json
import clutil
from clutil import command
import functions
import random


def write_config( file_name, dic ):
    try:
        os.remove( file_name )
    except:
        pass
    config_file = json.dumps( dic, sort_keys = True, indent = 4 ) + "\n"
    with open( file_name, "w+" ) as f:
        f.write(config_file)

def _normalize( n1, n2 ):

    if  n1 + n2 <= 100:
        return ( n1, n2 )
    
    factor = 100.0 / (n1 + n2)
    norm_n1, norm_n2 = int( n1 * factor ), int( n2 * factor)
    diff = 100 - ( norm_n1 + norm_n2 )
    return ( norm_n1, norm_n2 + diff )

class Experiment:

    def __init__( self, arg1, arg2 = None, rep = None ):
        if( arg2 is not None ):
            self._config1 = arg1
            self._config2 = arg2
        else:
            l = arg1.split()
            l = [ int(i) for i in l ]
            self._config1 = tuple( l[0:3] )
            self._config2 = tuple( l[3:] )

        self._mapping = { 'cpu': 0, 'io': 1, 'net': 2 }
        self._configs = [ self._config1, self._config2 ]
        self._rep = "" if rep is None else str(rep)
        

    def __eq__( self, o ):
        if isinstance( self, o.__class__ ):
            return (
                self._config1 == o._config1 and self._config2 == o._config2 ) or (
                    self._config1 == o._config2 and self._config2 == o._config1 )        
        return False

    def __hash__( self ):

        c1 = self._config1
        c2 = self._config2

        return ( c1[0] + c2[0], c1[1] + c2[1], c1[2] + c2[2] ).__hash__()

    def __str__( self ):
        return str( list(self._config1) + list( self._config2 ) ).replace("[","").replace("]","").replace(",","")

    def __repr__( self ):
        return self.__str__()
    
    def normalize( self ):
        t1 = self._config1
        t2 = self._config2

        n1 = _normalize( t1[0], t2[0] )
        n2 = _normalize( t1[1], t2[1] )
        n3 = _normalize( t1[2], t2[2] )

        c = [ n1, n2, n3 ]
        c = list(zip( * c ))

        return Experiment( c[0], c[1], self._rep )


    def _generateConfigs( self ):

        with open('base_config.py', 'r') as myfile:
            config_file = myfile.read()

        if( config_file is None or config_file.strip() == "" ):
            return                               
        
        #cpu01 = functions.cpu(     int(self._config1[0]) )
        #io01  = functions.io(      int(self._config1[1]) )
        #net01 = functions.network( int(self._config1[2]) )
        
        #cpu02 = functions.cpu(     int(self._config2[0]) )
        #io02  = functions.io(      int(self._config2[1]) )
        #net02 = functions.network( int(self._config2[2]) )

        cpu01 = int(self._config1[0])
        io01  = int(self._config1[1])
        net01 = int(self._config1[2])
        
        cpu02 = int(self._config2[0])
        io02  = int(self._config2[1])
        net02 = int(self._config2[2])

        
        ldict = locals()
        
        exec( config_file, globals(), ldict )
        
        self.config = ldict["config"]
        self.provider_config = ldict["provider_config"]

    def create_experiment_folder( self ):
        self._generateConfigs()
        
        folder = "exp_" + str( (self._config1, self._config2) ).replace("(","").replace(")","").replace(", ","_")

        if( self._rep ):
            folder = folder + "_" + self._rep

        os.system( "cp -r template/ " + folder )
        
        write_config( folder +  "/configFiles/config.json", self.config )
        write_config( folder + "/configFiles/provider_config.json", self.provider_config )
        
        os.system("mv " + folder + " experiments/" )

        

def get_experiments( levels1 = [ 0 ] , levels2 = [ 0 ], **kvargs ):    
    experiments = []

    levels_cpu1 = kvargs["vm1"]["cpu"] if "vm1" in kvargs and "cpu" in kvargs["vm1"] else levels1
    levels_io1  = kvargs["vm1"][ "io"] if "vm1" in kvargs and  "io" in kvargs["vm1"] else levels1
    levels_net1 = kvargs["vm1"]["net"] if "vm1" in kvargs and "net" in kvargs["vm1"] else levels1

    levels_cpu2 = kvargs["vm2"]["cpu"] if "vm2" in kvargs and "cpu" in kvargs["vm2"] else levels2
    levels_io2  = kvargs["vm2"][ "io"] if "vm2" in kvargs and  "io" in kvargs["vm2"] else levels2
    levels_net2 = kvargs["vm2"]["net"] if "vm2" in kvargs and "net" in kvargs["vm2"] else levels2

    for cpu1 in levels_cpu1:
        for io1 in levels_io1:
            for net1 in levels_net1:
                for cpu2 in levels_cpu2:
                    for io2 in levels_io2:
                        for net2 in levels_net2:
                            exp = Experiment( (cpu1, io1, net1), (cpu2, io2, net2) )
                            experiments.append( exp )

    return set(experiments)

@command
def teste(args):
    e = Experiment("80 100 40 60 100 20")
    print(e)
    print(e.normalize())

    e.create_experiment_folder()
    e.normalize().create_experiment_folder()

@command
def single_parameter(args, vm = "vm1", param = "cpu", values = "[0]"):
    l = eval(values)
    
    arguments = dict()
    arguments[vm] = dict()
    arguments[vm][param] = l
    
    exps = get_experiments( **arguments )

    for e in exps:
        print("Creating experiment: " + str(e))
        e.create_experiment_folder()

@command
def onevm( args ):
    levels = [ 0, 20, 40, 60, 80, 100 ]
    exps = get_experiments( levels )
    
    for i in exps:
        i.create_experiment_folder()
        #print(i)

@command
def twovms( args, norm = False ):
    levels = [ 0, 20, 40, 60, 80, 100 ]
    exps = get_experiments( levels, levels )
    
    for i in exps:
        if norm:
            print( str(i) + " - " + str(i.normalize()) )
        else:
            print(i)

@command
def twovms2( args, norm = False, shuffle = False, number = -1 ):
    levels1 = [ 0, 20, 80, 100 ]
    levels2 = [ 0, 40, 100 ]

    exps = list(get_experiments( levels1, levels2 ))

    if shuffle:
        random.shuffle( exps )


    if number > 0:
        try:
            number = int(number)
            exps = exps[0:number]
        except ValueError:
            pass
    
    for i in exps:
        if norm:
            print( str(i) + " - " + str(i.normalize()) )
        else:
            print(i)

@command
def normtest( args ):
    print( args )
    i = int(args[0])
    j = int(args[1])
    print( (i,j) )

    print( _normalize( i, j ) )

@command
def fromfile( args ):
    if( not (args and args[0]) ): 
        return

    filename = args[0]

    with open(filename,'r') as f:
        for l in (line.strip() for line in f):
            exp = Experiment( l ).normalize()
            exp.create_experiment_folder()

@command
def create( args ):
    if( not( args and args[0] ) ):
        return

    
    if( len(args) <= 1 ):
        exp = Experiment( args[0] ).normalize()
        exp.create_experiment_folder()
    else:
        reps = int( args[1] )
        for i in range( 0, reps ):
            rep = i + 1
            exp = Experiment( args[0], rep = rep )
            exp.create_experiment_folder()

    
clutil.execute()
