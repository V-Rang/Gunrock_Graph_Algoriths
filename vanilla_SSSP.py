#vanilla implementation of single source shortest path (SSSP)
#read in a graph in matrix market format and based on a designated source, estimate the shortest distance to all the vertices
#this is a naive serial implementation in python, parallel algorithms will be explored using the Gunrock graph analytics library to achieve speedups

import numpy as np
from scipy.io import mmread

def sssp(mat,source,distance):
    distance[:] = np.inf
    distance[org_source] = 0

    visited = np.zeros(n_vertices) - 1
    visited[org_source] = 0

    present_iter_sources = [org_source]
    next_iter_sources = []

    iteration = 0 #to keep count on which iteration was each vertex visited for the first time

    while( len(present_iter_sources) > 0):
        
        for curr_source in present_iter_sources:
            visited[curr_source] = iteration
            neighbours = mat.indices[mat.indptr[curr_source]:mat.indptr[curr_source+1]]
            n_distances = mat.data[mat.indptr[curr_source]:mat.indptr[curr_source+1]]

            for neighbour,n_distance in zip(neighbours,n_distances):
                old_distance = distance[neighbour]
                new_distance =  distance[curr_source] + n_distance
                distance[neighbour] = min(new_distance,old_distance)
                if(new_distance < old_distance): next_iter_sources.append(neighbour)


        present_iter_sources = []

        #filtering out following kinds of vertices
        #1. if vertex already was a "source" once before, we dont want it to be source again, to prevent infinite loop
        #2. if vertex has no neighbours, there is no point in investigating as a "source" for potential shorter distances to other vertices

        for potential_sources in next_iter_sources:
            if(visited[potential_sources] != -1): continue
            # if(len(mat.indices[mat.indptr[potential_sources]:mat.indptr[potential_sources+1]]) == 0): continue
            if(mat.indptr[potential_sources+1] - mat.indptr[potential_sources] == 0): continue
            present_iter_sources.append(potential_sources)
        iteration += 1
        next_iter_sources = []
   

mat = mmread(r"chesapeake.mtx").tocsr()
n_vertices =  mat.shape[0]
org_source = 0
distance = np.zeros(n_vertices) #distance array for all vertices from the source

sssp(mat,org_source,distance) #assigning 0 to be the source
print(distance)


