#!/usr/bin/python

import json, sys, time

def convert(fi, fo):
    # !! TODO
    # for each node
        node = {}

        # !! TOOD id
        # id is the id of the node
        node["_id"] = id

        # !! TODO types, value
        # types is a dictionary of each type of property and its value for this node
        for type in types:
            node[type] = types[type]

        # !! TODO inArray, outArray
        # in and out are arrays of dictionaries of the edges and their properties
        node["_inE"] = inArray
        node["_outE"] = outArray

        str = json.dumps(node)
        fo.write(str)

    fi.close()
    fi.close()

def file_handlers(i_file, o_file):
    fi = open(i_file, 'r')
    fo = open(o)file, 'w')
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
    convert(fi, fo)
    print "Took",time.time()-start_time,"seconds to complete."
