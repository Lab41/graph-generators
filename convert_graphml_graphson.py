#!/usr/bin/python

import json, os, sys, time

def is_directed(i_file):
    cmd = 'grep -m 1 "edgedefault" '+i_file
    dir_line = os.popen(cmd).read()
    dir_array = dir_line.split("\"")
    directed = dir_array[3]
    return 1 if directed == "directed" else 0

def edges(id, i_file):
    directed = is_directed(i_file)

    # sed -n '52{p;q}' file

    # !! TODO get edges for the node with id
    in_array = []
    out_array = []

    return in_array, out_array

def convert(i_file, n_file, e_file, fo):
    n_fi = open(n_file, 'r')
    e_fi = open(e_file, 'r')
    edge = {}
    for line in n_fi:
        line = line.strip()
        if line != "":
            node = eval(line)
            id = node["_id"]
            source = ""
            if "source" in edge:
                source = edge["source"]
            out_e = []
            in_e = []
            print "source: ",source
            print "id: ",id
            if edge == {}:
                e_line = e_fi.readline()
                edge = eval(e_line)
                source = edge["source"]
            if source == id:
                while source == id: 
                    out_e.append(edge)
                    try:
                        e_line = e_fi.readline()
                        edge = eval(e_line)
                        source = edge["source"]
                    except:
                        source = ""
                
            node["_outE"] = out_e
            node["_inE"] = in_e
            str = json.dumps(node)
            fo.write(str+"\n")

    n_fi.close()
    e_fi.close()
    fo.close()

def field_split(n, field):
    field_a = n.split(field+"=\"")
    field_a = field_a[1].split("\"")
    field = field_a[0]
    return field

def parse(n, type, fi):
    obj = {}
    if type == "node":
        id_a = n.split(type+" id=\"")
        id_a = id_a[1].split("\">")
        obj["_id"] = id_a[0]
    else:
        obj["_id"] = field_split(n, "id")
        obj["label"] = field_split(n, "label")
        obj["source"] = field_split(n, "source")
        obj["target"] = field_split(n, "target")
        
    types = {}
    type_a = n.split("data key=\"")
    for type in type_a:
        if "</data>" in type:
            t_a = type.split("</data>")
            t_a = t_a[0].split("\">")
            types[t_a[0]] = t_a[1]

    for type in types:
        obj[type] = types[type]

    str = json.dumps(obj)
    fi.write(str+"\n")
    return "" 
    
def split(i_file, o_file, fi, fo, n_fi, e_fi):
    line = 1
    n = ""
    while line:
        line = fi.readline()
        n += line
        if "</edge>" in line:
            n = parse(n, "edge", e_fi)
        if "</node>" in line:
            n = parse(n, "node", n_fi)

    fi.close()
    n_fi.close()
    e_fi.close()

def file_handlers(i_file, o_file, n_file, e_file):
    fi = open(i_file, 'r')
    fo = open(o_file, 'w')
    n_fi = open(n_file, 'w')
    e_fi = open(e_file, 'w')
    return fi, fo, n_fi, e_fi

def print_help():
    print "Please specify the following arguments when executing this script: \n"
    print "-i \t<path to input file>" 
    print "-o \t<path to output file> (note: it will overwrite any pre-existing file)\n" 
    print "-t \t<path for temporary files> (note: these will be deleted after the script is finished, roughly the same size as the original input file though)\n"
    sys.exit(0)

def process_args(args):
    i_file = ""
    o_file = ""
    t_file = ""
    i = 0
    while i < len(args):
        if args[i] == "-i":
            try:
                i_file = args[i+1]
                f = open(i_file, 'r')
                f.close()
            except:
                print_help()
        elif args[i] == "-o":
            try:
                o_file = args[i+1]
                f = open(o_file, 'w')
                f.close()
            except:
                print_help()
        elif args[i] == "-t":
            try:
                t_file = args[i+1]
                f = open(t_file+"1", 'w')
		f.close()
		t_file = args[i+1]
		f = open(t_file+"2", 'w')
                f.close()
            except:
                print_help()
        else:
            print_help()
        i += 2

    if i_file == "" or o_file == "" or t_file == "":
        print_help()

    return i_file, o_file, t_file

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    print "NOTE: You should have at least 2 times the current input file size available to complete this operation.\n"
    args = get_args()
    i_file, o_file, t_file = process_args(args)
    fi, fo, n_fi, e_fi = file_handlers(i_file, o_file, t_file+"1", t_file+"2")
    split(i_file, o_file, fi, fo, n_fi, e_fi)
    convert(i_file, t_file+"1", t_file+"2", fo)
    cmd = "rm -rf "+t_file+"1"
    junk = os.popen(cmd).read()
    cmd = "rm -rf "+t_file+"2"
    junk = os.popen(cmd).read()
    print "Took",time.time()-start_time,"seconds to complete."
