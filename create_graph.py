#!/usr/bin/python

import sys, time, uuid
from random import randint, sample

def output_file(file):
    fo = open(file, 'w')
    return fo

def header(type, node_attrs_min, node_attrs_max, edge_attrs_min, edge_attrs_max, fo):
    node_attrs_a = []
    edge_attrs_a = []
    if type == "graphml":
        header = "<?xml version=\"1.0\" ?>\n<graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\">\n"
        fo.write(header)

        # requiring 'name' attribute for nodes
        node_attrs_a.append("name")

        # randomly create other attributes
        i = 0
        while i < node_attrs_max-1:
            node_attrs_a.append("node-type"+str(i))
            i += 1
        i = 0
        while i < edge_attrs_max:
            i += 1
            edge_attrs_a.append("edge-type"+str(i))

        for attr in node_attrs_a:
            node_str = "    <key id=\""+attr+"\" for=\"node\" attr.name=\""+attr+"\" attr.type=\"string\"></key>\n"
            fo.write(node_str)
        for attr in edge_attrs_a:
            edge_str = "    <key id=\""+attr+"\" for=\"edge\" attr.name=\""+attr+"\" attr.type=\"string\"></key>\n"
            fo.write(edge_str)

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


# !! NOTE
# create dictionaries of ids of nodes to keep track of how many degrees have been put on a particular node
# output something that tells the average degree of each node


def create_node(type, node, node_attrs_min, node_attrs_max, num_node_attrs, first_a, last_a, fo):
    if type == "graphml":
        node_str = "        <node id=\""+str(node)+"\">\n"
        num_attrs = randint(node_attrs_min, node_attrs_max)
        attrs_list = 0
        if node_attrs_max != 0:
            attrs_list = sample(xrange(node_attrs_max-1), node_attrs_max-1)
        i = 0
        while i < num_attrs:
            if i == 0:
                index = str(node)
                if node < 10000:
                    val1 = 0
                    val2 = node
                else:
                    val1 = int(index[:-4])
                    val2 = int(index[-4:])
                node_str += "            <data key=\"name\">"+first_a[val1]+" "+last_a[val2]+"</data>\n"
                num_node_attrs += 1
            else:
                node_str += "            <data key=\"type"+str(attrs_list[i-1])+"\">"+str(uuid.uuid4())+"</data>\n"
                num_node_attrs += 1
            i += 1
        node_str += "        </node>\n"
    fo.write(node_str)
    return num_node_attrs

def undirected_edge(source, num_nodes, num_edges, num_edge_attrs, undirected_node_d, min, max, edge_attrs_min, edge_attrs_max, fo):
    # !! NOTE hard coded list of labels (relationship types) for edges
    undirected_edge_labels = ["knows", "connected", "acquainted", "friends", "family"]

    target = source
    # don't create self-loops
    while source == target or undirected_node_d[target] == max:
        target = randint(0, num_nodes-1)
        
    i = 0; j = 0
    while j < num_nodes:
        # check against max
        if undirected_node_d[j] < max and undirected_node_d[j] > min:
            i += 1
        j += 1

    if i != j:
        edge_str = "        <edge id=\""+str(num_nodes+num_edges)+"\" source=\""+str(source)+"\" target=\""+str(target)+"\" label=\""+str(undirected_edge_labels[randint(0, len(undirected_edge_labels)-1)])+"\">"
        num_attrs = randint(edge_attrs_min, edge_attrs_max)
        attrs_list = 0
        if edge_attrs_max != 0:
            attrs_list = sample(xrange(edge_attrs_max-1), edge_attrs_max-1)
        k = 0
        while k < num_attrs:
            edge_str += "\n            <data key=\""+str(attrs_list[k-1])+"\">"+str(uuid.uuid4())+"</data>"
            k += 1 
            num_edge_attrs += 1
        if k < 0:
            edge_str += "\n        "
        edge_str += "</edge>\n"
        undirected_node_d[source] += 1
        undirected_node_d[target] += 1
        num_edges += 1
        fo.write(edge_str)
    return undirected_node_d, num_edges, num_edge_attrs

def directed_edge():
    # !! TODO
    print "todo"
    # !! NOTE hard coded list of labels (relationship types) for edges
    directed_edge_labels = ["knows", "contacted", "manager_of", "works_for"]

def create_edges(type, num_nodes, directed, min, max, mini, mino, maxi, maxo, edge_attrs_min, edge_attrs_max, fo):
    print "Creating edges . . ."
    undirected_node_d = {}
    directed_node_in_d = {}
    directed_node_out_d = {}
    num_edge_attrs = 0
    num_edges = 0

    i = 0
    while i < num_nodes:
        undirected_node_d[i] = 0
        directed_node_in_d[i] = 0
        directed_node_out_d[i] = 0
        i += 1

    if type == "graphml":
        if num_nodes > 1:
            i = 0
            prev = -1
            while i < num_nodes:
                percent_complete = percentage(i, num_nodes)
                if percent_complete % 10 == 0 and prev != percent_complete:
                    prev = percent_complete
                    print str(percent_complete)+"% finished"
                source = i 

                if directed == 0:
                    gen_edges = randint(min, max)
                    j = 0
                    while j < gen_edges:
                        if undirected_node_d[source] < max: 
                            undirected_node_d, num_edges, num_edge_attrs = undirected_edge(source, num_nodes, num_edges, num_edge_attrs, undirected_node_d, min, max, edge_attrs_min, edge_attrs_max, fo)
                        j += 1
                else:
                    # check against mini, mino, maxi, and maxo
                    junk = 1

                i += 1

    return num_edge_attrs, num_edges

def close_graph(type, fo):
    closer = ""
    if type == "graphml":
        closer = "    </graph>\n</graphml>"
    fo.write(closer)
    fo.close()

def get_names():
    first_a = []
    last_a = []
    fname = open('dict/randomNames.csv', 'r')
    for line in fname:
        name = line.split(",")
        first_a.append(name[0])
        last_a.append(name[1])
    fname.close()
    return first_a, last_a

def generate_graph(type, file, num_nodes, directed, node_attrs_min, node_attrs_max, edge_attrs_min, edge_attrs_max, min, max, mini, mino, maxi, maxo):
    fo = output_file(file)
    node_attrs_a, edge_attrs_a = header(type, node_attrs_min, node_attrs_max, edge_attrs_min, edge_attrs_max, fo)
    graph_id = is_directed(type, directed, fo)
    first_a, last_a = get_names()
    
    num_node_attrs = 0
    i = 0
    print "Creating nodes . . ."
    prev = -1
    for node in range(num_nodes):
        num_node_attrs = create_node(type, node, node_attrs_min, node_attrs_max, num_node_attrs, first_a, last_a, fo)
        percent_complete = percentage(i, num_nodes)
        if percent_complete % 10 == 0 and prev != percent_complete:
            prev = percent_complete
            print str(percent_complete)+"% finished"
        i += 1

    num_edge_attrs, num_edges = create_edges(type, num_nodes, directed, min, max, mini, mino, maxi, maxo, edge_attrs_min, edge_attrs_max, fo)

    close_graph(type, fo)
    return graph_id, num_node_attrs, num_edge_attrs, num_edges

def percentage(part, whole):
    return int(100 * float(part)/float(whole))

def print_help():
    print "\n-n \t<num of nodes> (default is 1000, must be between 1 and 100,000,000)\n"
    print "-max \t<max degree of nodes> (only used with undirected, default is 10)\n"
    print "-min \t<min degree of nodes> (only used with undirected, default is 1)\n"
    print "-maxi \t<max in degree of nodes> (only used with directed flag, default is 10)\n"
    print "-maxo \t<max out degree of nodes> (only used with directed flag, default is 10)\n"
    print "-mini \t<min in degree of nodes> (only used with directed flag, default is 1)\n"
    print "-mino \t<min out degree of nodes> (only used with directed flag, default is 1)\n"
    print "-minna \t<min num of node attributes> (default is 2, must be at least 1)\n"
    print "-maxna \t<max num of node attributes> (default is 2)\n"
    print "-minea \t<min num of edge attributes> (default is 0)\n"
    print "-maxea \t<max num of edge attributes> (default is 0)\n"
    print "-d \t(directed, undirected by default)\n"
    print "-t \t<output type> (graphml by default, options include gml and graphson)\n"
    print "-o \t<path to output file> (default is 'graph')\n"
    print "-h \thelp\n"
    sys.exit(0)
    
def check_directed(directed, arg, args, i, flag):
    if directed == flag:
        try:
            arg = int(args[i+1])
            if arg < 0:
                print help()
        except:
            print_help()
    else:
        print_help()

    return arg

def check_attrs(arg, args, i, flag):
    try:
        arg = int(args[i+1])
        if arg < flag:
            print_help()
    except:
        print_help()

    return arg

def process_args(args):
    # default initialization
    num_nodes = 1000
    directed = 0
    min = mini = mino = 1
    max = maxi = maxo= 10
    node_attrs_min = 2
    node_attrs_max = 2
    edge_attrs_min = 0
    edge_attrs_max = 0
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
                if num_nodes < 1 or num_nodes > 100000000:
                    print_help()
            except:
                print_help()
        elif args[i] == "-minna":
            node_attrs_min = check_attrs(node_attrs_min, args, i, 1)
        elif args[i] == "-maxna":
            node_attrs_max = check_attrs(node_attrs_max, args, i, node_attrs_min)
        elif args[i] == "-minea":
            edge_attrs_min = check_attrs(edge_attrs_min, args, i, 0)
        elif args[i] == "-maxea":
            edge_attrs_max = check_attrs(edge_attrs_max, args, i, edge_attrs_min)
        elif args[i] == "-max":
            max = check_directed(directed, max, args, i, 0)
        elif args[i] == "-min":
            min = check_directed(directed, min, args, i, 0)
        elif args[i] == "-mini":
            mini = check_directed(directed, mini, args, i, 1)
        elif args[i] == "-mino":
            mino = check_directed(directed, mino, args, i, 1)
        elif args[i] == "-maxi":
            maxi = check_directed(directed, maxi, args, i, 1)
        elif args[i] == "-maxo":
            maxo = check_directed(directed, maxo, args, i, 1)
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
    if node_attrs_max < node_attrs_min or edge_attrs_max < edge_attrs_min:
        print_help()

    return type, output, num_nodes, directed, min, max, mini, mino, maxi, maxo, node_attrs_min, node_attrs_max, edge_attrs_min, edge_attrs_max

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    type, output, num_nodes, directed, min, max, mini, mino, maxi, maxo, node_attrs_min, node_attrs_max, edge_attrs_min, edge_attrs_max = process_args(args)
    print "Generating the following graph:"
    print "\tType: \t\t\t\t",type
    print "\tOutput File: \t\t\t",output
    print "\tNodes: \t\t\t\t",num_nodes
    if directed == 0:
        print "\tDirected: \t\t\tNo"
        print "\tMinimum Degree: \t\t",min
        print "\tMaximum Degree: \t\t",max
    else:
        print "\tDirected: \t\t\tYes"
        print "\tMinimum In Degree: \t\t",mini
        print "\tMaximum In Degree: \t\t",maxi
        print "\tMinimum Out Degree: \t\t",mino
        print "\tMaximum Out Degree: \t\t",maxo
    print "\tMinimum Node Attributes: \t",node_attrs_min
    print "\tMaximum Node Attributes: \t",node_attrs_max
    print "\tMinimum Edge Attributes: \t",edge_attrs_min
    print "\tMaximum Edge Attributes: \t",edge_attrs_max
    
    graph_id, num_node_attrs, num_edge_attrs, num_edges = generate_graph(type, output, num_nodes, directed, node_attrs_min, node_attrs_max, edge_attrs_min, edge_attrs_max, min, max, mini, mino, maxi, maxo)
    
    print "Graph ID = ",graph_id
    print "Number of edges created = ",num_edges
    print "Average number of node attributes = ",num_node_attrs
    print "Average number of edge attributes = ",num_edge_attrs
    print "Took",time.time() - start_time,"seconds to complete."
