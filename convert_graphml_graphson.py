#!/usr/bin/python

import json, os, sys, time

def convert(i_file, fi, fo):
    cmd = 'grep -m 1 "edgedefault" '+i_file
    print cmd
    dir_line = os.popen(cmd).read()
    dir_array = dir_line.split("\"")
    directed = dir_array[3]
    print directed

    # !! TODO split file into nodes and edges

    line = 1
    n = ""
    while line:
        line = fi.readline()
        n += line
        if "</node>" in line:
            print n
            id_a = n.split("node id=\"")
            id_a = id_a[1].split("\">")
            id = id_a[0]
            node = {}

            node["_id"] = id

            types = {}
            type_a = n.split("data key=\"")
            for type in type_a:
                if "</data>" in type:
                    t_a = type.split("</data>")
                    t_a = t_a[0].split("\">")
                    types[t_a[0]] = t_a[1]

            for type in types:
                node[type] = types[type]

            # !! TODO inArray, outArray
            # in and out are arrays of dictionaries of the edges and their properties
            #node["_inE"] = inArray
            #node["_outE"] = outArray

            str = json.dumps(node)
            #fo.write(str)

            print str
            n = ""

    fi.close()
    fi.close()

def file_handlers(i_file, o_file):
    fi = open(i_file, 'r')
    fo = open(o_file, 'w')
    return fi, fo

def print_help():
    print "Please specify the following arguments when executing this script: \n"
    print "-i \t<path to input file>" 
    print "-o \t<path to output file> (note: it will overwrite any pre-existing file)\n" 
    sys.exit(0)

def process_args(args):
    i_file = ""
    o_file = ""
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
        else:
            print_help()
        i += 2

    if i_file == "" or o_file == "":
        print_help()

    return i_file, o_file

def get_args():
    args = []
    for arg in sys.argv:
        args.append(arg)
    return args[1:]

if __name__ == "__main__":
    start_time = time.time()
    args = get_args()
    i_file, o_file = process_args(args)
    fi, fo = file_handlers(i_file, o_file)
    convert(i_file, fi, fo)
    print "Took",time.time()-start_time,"seconds to complete."
