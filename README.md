graph-generators
================

Scripts for generating graphs in various formats.

Will be looking at outputting into the following formats first: 

    https://github.com/tinkerpop/blueprints/wiki/GraphML-Reader-and-Writer-Library
    https://github.com/tinkerpop/blueprints/wiki/GraphSON-Reader-and-Writer-Library
    https://github.com/tinkerpop/blueprints/wiki/GML-Reader-and-Writer-Library

=================
parameters:

    -n               <num of nodes> (default is 1000, must be greater than 0)
    -min/max         <min/max degree of nodes> (only used with undirected, default is 1/10)
    -mini/maxi       <min/max in degree of nodes> (only used with directed flag, default is 1/10)
    -mino/maxo       <max/max out degree of nodes> (only used with directed flag, default is 1/10)
    -minna/maxna     <min/max num of node attributes> (default is 2, must be at least 1)  
    -minea/maxea     <min/max num of edge attributes> (default is 0)
    -d               (directed, undirected by default)
    -t*              <output type> (graphml by default, options include gml and graphson)
    -o               <path to output file> (default is 'graph')
    -h               help
    
    * only graphml and graphson have been implemented so far


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/Lab41/graph-generators/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

