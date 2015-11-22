#!/usr/bin/python
# For the case of the quiz, it takes 1.2s to finish the page rank iteration
# for http://snap.stanford.edu/data/web-Google.txt.gz data.
import sys
import math
import time
import numpy as np
import scipy.sparse as sp

def read_graph(file):
    graph_index = {}
    index = 0
    row = []
    col = []
    count = {}
    with open(file, 'r') as f:
        lines = f.readlines()
    # process each edge    
    for line in lines:
        if line.startswith('#'):
            continue
        (src, dst) = [int(x) for x in line.split()]
        # index for source
        if not graph_index.has_key(src):
            graph_index[src] = index
            index += 1
        col.append(graph_index[src])
        # index for destination
        if not graph_index.has_key(dst):
            graph_index[dst] = index
            index += 1
        row.append(graph_index[dst])
        # count edges per node
        if count.has_key(col[-1]):
            count[col[-1]] = count[col[-1]] + 1
        else:
            count[col[-1]] = 1
    print 'processing edge = %d, generated %dx%d matrix' % (len(lines), index, index)
    # initial matrix value
    data = [1.0 / count[x] for x in col]
    return (graph_index, index, sp.csc_matrix((data, (row, col)), shape=(index, index)))

def iterate(m, r, size, teleport, beta = 0.8):
    r = beta * m.dot(r) + teleport
    leaked = 1 - r.sum()
    vote = (leaked / size) * np.ones(size)
    return (r + vote, leaked)
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print '%s <file> <number>' % (sys.argv[0])
        sys.exit(1)
        
    number = int(sys.argv[2])
    timer = time.time()
    (graph, size, m) = read_graph(sys.argv[1])
    print >> sys.stderr, 'read graph: {0:.1f} seconds.'.format(time.time() - timer)
   
    r = np.ones(size) / size
    teleport = (0.2 / size) * np.ones(size)
    timer = time.time()
    for i in range(100):
        pre = r
        (r, leaked) = iterate(m, r, size, teleport)
        delta = r - pre
        diff = math.sqrt(delta.dot(delta))
        if diff < 1e-6:
            break
    print >> sys.stderr, 'iteration: {0:.1f} seconds.'.format(time.time() - timer)
    print "total run %d, r[%d] = %s, sum = %f" % (i, graph[number], r[graph[number]], r.sum())
