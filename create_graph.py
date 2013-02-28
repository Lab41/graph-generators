#!/usr/bin/python

import sys, uuid

def output_file(file):
    fo = open(file, 'w')
    return fo

def header(type, node_attrs, edge_attrs, fo):
    node_attrs_a = []
    edge_attrs_a = []
    if type == "graphml":
        header = "<?xml version=\"1.0\" ?>\n<graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\">\n"
        fo.write(header)

        # !! TODO add keys for attr types for nodes and edges

    return node_attrs_a, edge_attrs_a

def is_directed(type, directed, fo):
    graph_id = str(uuid.uuid4())
    directed_str = "undirected" 
    if directed == 1:
        directed_str = "directed"

    if type == "graphml":
        graph_str = "    <graph id=\""+graph_id+"\" edgedefault=\""+directed_str+"\">\n"
        fo.write(graph_str)

    return graph_id

def create_node(type, num_nodes, node_attrs, fo):
    # !! TODO
    print "node"

def create_edge(type, min, max, mini, mino, maxi, maxo, edge_attrs, fo):
    # !! TODO
    print "edge"

def close_graph(type, fo):
    closer = ""
    if type == "graphml":
        closer = "    </graph>\n</graphml>"
    fo.write(closer)
    fo.close()

def generate_graph(type, file, num_nodes, directed, node_attrs, edge_attrs, min, max, mini, mino, maxi, maxo):
    fo = output_file(file)
    node_attrs_a, edge_attrs_a = header(type, node_attrs, edge_attrs, fo)
    graph_id = is_directed(type, directed, fo)

    # !! TODO node creation
    # !! TODO edge creation

    close_graph(type, fo)

def print_help():
    print "\n-n <num of nodes> (default is 1000)\n"
    print "-max <max degree of nodes> (only used with undirected, default is 10)\n"
    print "-min <min degree of nodes> (only used with undirected, default is 1)\n"
    print "-maxi <max in degree of nodes> (only used with directed flag, default is 10)\n"
    print "-maxo <max out degree of nodes> (only used with directed flag, default is 10)\n"
    print "-mini <min in degree of nodes> (only used with directed flag, default is 1)\n"
    print "-mino <min out degree of nodes> (only used with directed flag, default is 1)\n"
    print "-na <num of node attributes> (default is 2)\n"
    print "-ea <num of edge attributes> (default is 0)\n"
    print "-d (directed, undirected by default)\n"
    print "-t <output type> (graphml by default, options include gml and graphson)\n"
    print "-o <path to output file> (default is 'graph')\n"
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
    node_attrs = 2
    edge_attrs = 0
    directed_num = -1
    type = "graphml"
    output = "graph"

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
        elif args[i] == "-na":
            try:
                node_attrs = int(args[i+1])
                if node_attrs < 1:
                    print_help()
            except:
                print_help()
        elif args[i] == "-ea":
            try:
                edge_attrs = int(args[i+1])
                if edge_attrs < 0:
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
        elif args[i] == "-o":
            try:
                output = args[i+1]
                f = open(output, 'w')
                f.close()
            except:
                print_help()
        else:
            print_help()
        i += 2
    if max < min or maxi < mini or maxo < mino:
        print_help()
    if type != "graphml" and type != "gml" and type != "graphson":
        print_help()

    return type, output, num_nodes, directed, min, max, mini, mino, maxi, maxo, node_attrs, edge_attrs

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    args = get_args()
    type, output, num_nodes, directed, min, max, mini, mino, maxi, maxo, node_attrs, edge_attrs = process_args(args)
    print "Generating the following graph:"
    print "\tType: \t\t\t",type
    print "\tOutput File: \t\t",output
    print "\tNodes: \t\t\t",num_nodes
    if directed == 0:
        print "\tDirected: \t\tNo"
        print "\tMinimum Degree: \t",min
        print "\tMaximum Degree: \t",max
    else:
        print "\tDirected: \t\tYes"
        print "\tMinimum In Degree: \t",mini
        print "\tMaximum In Degree: \t",maxi
        print "\tMinimum Out Degree: \t",mino
        print "\tMaximum Out Degree: \t",maxo
    print "\tNode Attributes: \t",node_attrs
    print "\tEdge Attributes: \t",edge_attrs 
    
    generate_graph(type, output, num_nodes, directed, node_attrs, edge_attrs, min, max, mini, mino, maxi, maxo)
