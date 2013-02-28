#!/usr/bin/python

import sys

def header(type):
    # !! TODO
    print "header"

def is_directed(type, directed):
    # !! TODO
    print "directed or undirected"

def create_node(type, num_nodes):
    # !! TODO
    print "node"

def create_edge(type, min, max, mini, mino, maxi, maxo):
    # !! TODO
    print "edge"

def close_graph(type):
    # !! TODO
    print "close graph"

def generate_graph(type):
    # !! TODO
    print "generate graph"

def print_help():
    print "-n <num_of_nodes> (default is 1000)"
    print "-max <max degree of nodes> (only used with undirected, default is 10)"
    print "-min <min degree of nodes> (only used with undirected, default is 1)"
    print "-maxi <max in degree of nodes> (only used with directed flag, default is 10)"
    print "-maxo <max out degree of nodes> (only used with directed flag, default is 10)"
    print "-mini <min in degree of nodes> (only used with directed flag, default is 1)"
    print "-mino <min out degree of nodes> (only used with directed flag, default is 1)"
    print "-d (directed, undirected by default)"
    print "-t <output type> (graphml by default, options include gml and graphson)"
    sys.exit(0)
    
def check_directed(directed, arg, value, flag):
    if directed == flag:
        try:
            arg = int(value)
            if arg < 0:
                print help()
        except:
            print_help()
    else:
        print_help()

    return arg

def process_args(args):
    # default initialization
    num_nodes = 1000
    directed = 0
    min = mini = mino = 1
    max = maxi = maxo= 10
    directed_num = -1
    type = "graphml"

    # process whether it is directed or not
    i = 0
    while i < len(args): 
        if args[i] == "-d":
            directed = 1
            directed_num = i
            min = -1
            max = -1
        i += 1

    if directed_num == -1:
        mini = -1
        mino = -1
        maxi = -1
        maxo = -1
    else:
        del args[directed_num]

    # process rest of the args
    i = 0
    while i < len(args): 
        if args[i] == "-n":
            try:
                num_nodes = int(args[i+1])
                if num_nodes < 1:
                    print_help()
            except:
                print_help()
        elif args[i] == "-max":
            max = check_directed(directed, max, args[i+1], 0)
        elif args[i] == "-min":
            min = check_directed(directed, min, args[i+1], 0)
        elif args[i] == "-mini":
            mini = check_directed(directed, mini, args[i+1], 1)
        elif args[i] == "-mino":
            mino = check_directed(directed, mino, args[i+1], 1)
        elif args[i] == "-maxi":
            maxi = check_directed(directed, maxi, args[i+1], 1)
        elif args[i] == "-maxo":
            maxo = check_directed(directed, maxo, args[i+1], 1)
        elif args[i] == "-t":
            try:
                type = args[i+1]
            except:
                print_help()
        else:
            print_help()
        i += 2
    if max < min or maxi < mini or maxo < mino:
        print_help()
    if type != "graphml" and type != "gml" and type != "graphson":
        print_help()

    return type, num_nodes, directed, min, max, mini, mino, maxi, maxo

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    args = get_args()
    type, num_nodes, directed, min, max, mini, mino, maxi, maxo = process_args(args)
    print type, num_nodes, directed, min, max, mini, mino, maxi, maxo
