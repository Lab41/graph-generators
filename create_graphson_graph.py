#!/usr/bin/python

import json, math, sys, time, uuid
from random import randint, sample

def output_file(file):
    fo = open(file, 'w')
    return fo

def create_node(node, in_dict, out_dict, in_dict_attrs, out_dict_attrs, num_nodes, node_attrs_min, node_attrs_max, edge_attrs_min, edge_attrs_max, num_node_attrs, num_edge_attrs, num_edges, mini, mino, maxi, maxo, fo):
    num_attrs = randint(node_attrs_min, node_attrs_max)
    attrs_list = 0
    if node_attrs_max != 0:
        attrs_list = sample(xrange(node_attrs_max-1), node_attrs_max-1)

    # create the vertex
    node_str = "{\"_id\":"+str(node)

    i = 0
    while i < num_attrs:
        if i == 0:
            node_str += ",\"name"+"\":\""+str(uuid.uuid1())+"\""
        else:
            node_str += ",\"type"+str(attrs_list[i-1])+"\":\""+str(uuid.uuid1())+"\""
        num_node_attrs += 1
        i += 1

    # create the in edges
    node_str, num_edges, num_edge_attrs, out_dict, out_dict_attrs, in_dict, in_dict_attrs = add_edges("in", "out", out_dict, out_dict_attrs, in_dict, in_dict_attrs, node_str, node, num_nodes, num_edges, num_edge_attrs, edge_attrs_min, edge_attrs_max)
    # create the out edges
    node_str, num_edges, num_edge_attrs, in_dict, in_dict_attrs, out_dict, out_dict_attrs = add_edges("out", "in", in_dict, in_dict_attrs, out_dict, out_dict_attrs, node_str, node, num_nodes, num_edges, num_edge_attrs, edge_attrs_min, edge_attrs_max)

    node_str += "}\n"
    fo.write(node_str)
    return num_node_attrs, num_edge_attrs, num_edges, in_dict, out_dict, in_dict_attrs, out_dict_attrs

def add_edges(direction1, direction2, dict, dict_attrs, dict2, dict_attrs2,  node_str, node, num_nodes, num_edges, num_edge_attrs, edge_attrs_min, edge_attrs_max):
    # !! NOTE hard coded list of labels (relationship types) for edges
    directed_edge_labels = ["knows", "contacted", "manager_of", "works_for"]

    i = flag = 0
    edges = randint(mini,maxi/2)
    if node in dict2:
        node_str += ",\"_"+direction1+"E\":["
        node_str += json.dumps(dict2[node])
        node_str = node_str[:-1]
        node_str += dict_attrs2[node]
        node_str += "}"
        i += len(dict2[node])
        if i >= edges:
            node_str += "]"
        del dict2[node]
        del dict_attrs2[node]
    while i < edges:
        flag = 1
        node_str += ","
        if i == 0:
            node_str += "\"_"+direction1+"E\":["
        num_attrs = randint(edge_attrs_min, edge_attrs_max)
        attrs_list = 0
        if edge_attrs_max != 0:
            attrs_list = sample(xrange(edge_attrs_max-1), edge_attrs_max-1)
        directionV = node
        while directionV == node:
            directionV = randint(0,num_nodes-1)
        random_label = str(directed_edge_labels[randint(0, len(directed_edge_labels)-1)])
        node_str += "{\"_label\":\""+random_label+"\",\"_id\":"+str(num_nodes+num_edges)+",\"_"+direction2+"V\":"+str(directionV)
        j = 0
        attr_str = ""
        while j < num_attrs:
            if j == 0:
                attr_str += ",\"type-"+str(attrs_list[j-1])+"\":\""+str(uuid.uuid1())+"\""
            else:
                attr_str += ",\"type-"+str(attrs_list[j-1]+1)+"\":\""+str(uuid.uuid1())+"\""
            num_edge_attrs += 1
            j += 1
        node_str += attr_str
        node_str += "}"
        num_edges += 1
        dV = "_"+direction1+"V"
        dict[directionV] = {"_label":random_label,"_id":str(num_nodes+num_edges),dV:node}
        dict_attrs[directionV] = attr_str

        num_edges += 1
        i += 1
    if flag == 1:
        node_str += "]"
    return node_str, num_edges, num_edge_attrs, dict, dict_attrs, dict2, dict_attrs2

def generate_graph(file, num_nodes, node_attrs_min, node_attrs_max, edge_attrs_min, edge_attrs_max, mini, mino, maxi, maxo):
    fo = output_file(file)
    
    in_dict = {}
    out_dict = {}
    in_dict_attrs = {}
    out_dict_attrs = {}
    num_node_attrs = num_edge_attrs = num_edges = 0
    i = 0
    print "Creating nodes . . ."
    prev = -1
    for node in range(num_nodes):
        num_node_attrs, num_edge_attrs, num_edges, in_dict, out_dict, in_dict_attrs, out_dict_attrs = create_node(node, in_dict, out_dict, in_dict_attrs, out_dict_attrs, num_nodes, node_attrs_min, node_attrs_max, edge_attrs_min, edge_attrs_max, num_node_attrs, num_edge_attrs, num_edges, mini, mino, maxi, maxo, fo)
        percent_complete = percentage(i, num_nodes)
        if percent_complete % 10 == 0 and prev != percent_complete:
            prev = percent_complete
            print str(percent_complete)+"% finished"
        i += 1

    return num_node_attrs, num_edge_attrs, num_edges

def percentage(part, whole):
    return int(100 * float(part)/float(whole))

def print_help():
    print "\n-n \t<num of nodes> (default is 1000, must be greater than 0)\n"
    print "-maxi \t<max in degree of nodes> (only used with directed flag, default is 10)\n"
    print "-maxo \t<max out degree of nodes> (only used with directed flag, default is 10)\n"
    print "-mini \t<min in degree of nodes> (only used with directed flag, default is 1)\n"
    print "-mino \t<min out degree of nodes> (only used with directed flag, default is 1)\n"
    print "-minna \t<min num of node attributes> (default is 2, must be at least 1)\n"
    print "-maxna \t<max num of node attributes> (default is 2)\n"
    print "-minea \t<min num of edge attributes> (default is 0)\n"
    print "-maxea \t<max num of edge attributes> (default is 0)\n"
    print "-o \t<path to output file> (default is 'graph')\n"
    print "-h \thelp\n"
    sys.exit(0)
    
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
    mini = mino = 1
    maxi = maxo= 10
    node_attrs_min = 2
    node_attrs_max = 2
    edge_attrs_min = 0
    edge_attrs_max = 0
    output = "graph"

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
        elif args[i] == "-minna":
            node_attrs_min = check_attrs(node_attrs_min, args, i, 1)
        elif args[i] == "-maxna":
            node_attrs_max = check_attrs(node_attrs_max, args, i, node_attrs_min)
        elif args[i] == "-minea":
            edge_attrs_min = check_attrs(edge_attrs_min, args, i, 0)
        elif args[i] == "-maxea":
            edge_attrs_max = check_attrs(edge_attrs_max, args, i, edge_attrs_min)
        elif args[i] == "-mini":
            mini = args[i+1]
        elif args[i] == "-mino":
            mino = args[i+1]
        elif args[i] == "-maxi":
            maxi = args[i+1]
        elif args[i] == "-maxo":
            maxo = args[i+1]
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
    if maxi < mini or maxo < mino:
        print_help()
    if node_attrs_max < node_attrs_min or edge_attrs_max < edge_attrs_min:
        print_help()

    return output, num_nodes, mini, mino, maxi, maxo, node_attrs_min, node_attrs_max, edge_attrs_min, edge_attrs_max

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    output, num_nodes, mini, mino, maxi, maxo, node_attrs_min, node_attrs_max, edge_attrs_min, edge_attrs_max = process_args(args)
    print "Generating the following graph:"
    print "\tOutput File: \t\t\t",output
    print "\tNodes: \t\t\t\t",num_nodes
    print "\tMinimum In Degree: \t\t",mini
    print "\tMaximum In Degree: \t\t",maxi
    print "\tMinimum Out Degree: \t\t",mino
    print "\tMaximum Out Degree: \t\t",maxo
    print "\tMinimum Node Attributes: \t",node_attrs_min
    print "\tMaximum Node Attributes: \t",node_attrs_max
    print "\tMinimum Edge Attributes: \t",edge_attrs_min
    print "\tMaximum Edge Attributes: \t",edge_attrs_max
    
    num_node_attrs, num_edge_attrs, num_edges = generate_graph(output, num_nodes, node_attrs_min, node_attrs_max, edge_attrs_min, edge_attrs_max, mini, mino, maxi, maxo)
    
    print "Number of edges created =",num_edges
    print "Average number of node attributes =",num_node_attrs/num_nodes
    if num_edges != 0:
        print "Average number of edge attributes =",num_edge_attrs/num_edges
    else:
        print "Average number of edge attributes = 0"
    print "Took",time.time() - start_time,"seconds to complete."
