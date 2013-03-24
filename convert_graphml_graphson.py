#!/usr/bin/python

import json, os, sys, time

# !! TODO need to implement this
def is_directed(i_file):
    cmd = 'grep -m 1 "edgedefault" '+i_file
    dir_line = os.popen(cmd).read()
    dir_array = dir_line.split("\"")
    directed = dir_array[3]
    return 1 if directed == "directed" else 0

def sort_edges(e_fi, e_file, splits):
    cmd = "split -a 4 -l "+splits+" "+e_file+" "+e_file+"-"
    junk = os.popen(cmd).read()
    cmd = "ls -1 "+e_file+"-*"
    files = os.popen(cmd).read()
    files = files.split("\n")

    for file in files[:-1]:
        f = open(file, 'r')
        fs = open(file+"1", 'w')
        sorted_edges = []
        for line in f:
            sorted_edges.append(line)
        sorted_edges = sorted(sorted_edges)
        for line in sorted_edges:
            fs.write(line)
        f.close()
        cmd = "rm -rf "+file
        junk = os.popen(cmd).read()
        fs.close()

    cmd = "ls -1 "+e_file+"-*"
    files = os.popen(cmd).read()
    files = files.split("\n")
    file_str = ""
    for file in files[:-1]:
        file_str += " "+file
    # !! TODO don't hardcode parallel or tmp dir.
    cmd = "sort --parallel=2 -T /graph-data3 -m -o "+e_file+"-sorted"+file_str
    junk = os.popen(cmd).read()

def convert(i_file, n_file, e_file, fo, splits):
    n_fi = open(n_file, 'r')
    e_fi = open(e_file, 'r')
    sort_edges(e_fi, e_file, splits)
    se_fi = open(e_file+"-sorted", 'r')
    out_edge = {}
    in_edge = {}
    for line in n_fi:
        line = line.strip()
        if line != "":
            node = eval(line)
            id = node["_id"]
            source = ""
            target = ""
            if "_outV" in out_edge:
                source = out_edge["_outV"]
            if "_inV" in in_edge:
                target = in_edge["_inV"]
            out_e = []
            in_e = []
            if out_edge == {}:
                e_line = e_fi.readline()
                e_line = e_line.split(" ", 1)
                out_edge = eval(e_line[1])
                source = out_edge["_outV"]
            if source == id:
                while source == id: 
                    del out_edge["_outV"]
                    out_e.append(out_edge)
                    try:
                        e_line = e_fi.readline()
                        e_line = e_line.split(" ", 1)
                        out_edge = eval(e_line[1])
                        source = out_edge["_outV"]
                    except:
                        source = ""
            if in_edge == {}:
                se_line = se_fi.readline()
                se_line = se_line.split(" ", 1)
                in_edge = eval(se_line[1])
                target = in_edge["_inV"]
            if target == id:
                while target == id: 
                    del in_edge["_inV"]
                    in_e.append(in_edge)
                    try:
                        se_line = se_fi.readline()
                        se_line = se_line.split(" ", 1)
                        in_edge = eval(se_line[1])
                        target = in_edge["_inV"]
                    except:
                        target = ""
                
            node["_outE"] = out_e
            node["_inE"] = in_e
            str = json.dumps(node)
            fo.write(str+"\n")

    n_fi.close()
    e_fi.close()
    se_fi.close()
    fo.close()

def field_split(n, field):
    field_a = n.split(field+"=\"")
    field_a = field_a[1].split("\"")
    field = field_a[0]
    return field

def parse(n, type, fi):
    obj = {}
    target = ""
    if type == "node":
        id_a = n.split(type+" id=\"")
        id_a = id_a[1].split("\">")
        obj["_id"] = id_a[0]
    else:
        obj["_id"] = field_split(n, "id")
        obj["_label"] = field_split(n, "label")
        obj["_outV"] = field_split(n, "source")
        target = field_split(n, "target")
        obj["_inV"] = target
        
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
    if type == "node":
        fi.write(str+"\n")
    else:
        fi.write(target+" "+str+"\n")
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
    print "-s \t<number of splits> (default is 10)"
    print "-i \t<path to input file>" 
    print "-o \t<path to output file> (note: it will overwrite any pre-existing file)" 
    print "-t \t<path for temporary files> (note: these will be deleted after the script is finished, roughly the same size as the original input file though)\n"
    sys.exit(0)

def process_args(args):
    i_file = ""
    o_file = ""
    t_file = ""
    splits = "10"
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
        elif args[i] == "-s":
            splits = args[i+1]
        else:
            print_help()
        i += 2

    if i_file == "" or o_file == "" or t_file == "":
        print_help()

    return i_file, o_file, t_file, splits

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    print "NOTE: You should have at least 2 times the current input file size available to complete this operation.\n"
    args = get_args()
    i_file, o_file, t_file, splits = process_args(args)
    fi, fo, n_fi, e_fi = file_handlers(i_file, o_file, t_file+"1", t_file+"2")
    split(i_file, o_file, fi, fo, n_fi, e_fi)
    convert(i_file, t_file+"1", t_file+"2", fo, splits)
    cmd = "rm -rf "+t_file+"1"
    junk = os.popen(cmd).read()
    cmd = "rm -rf "+t_file+"2*"
    junk = os.popen(cmd).read()
    print "Took",time.time()-start_time,"seconds to complete."
