"""
Implementation of the Markov Cluster algorithm
author: Abhijith V Mohan
"""
#!/usr/bin/env python
import numpy as np
import sys
NO_OF_ELEMENTS=9614

def read_adjmat(filename):
    """Read the adjacency matrix from csv file"""
    adjmat = np.loadtxt(filename,delimiter=',',skiprows=1,usecols=range(1,NO_OF_ELEMENTS+1))
    return adjmat

def norm_mat(a):
    """Normalize the matrix"""
    return a / a.sum(axis=0)[:np.newaxis]

def inflate(a, i):
    """Inflation operation"""
    return norm_mat(a ** i)

def expand(a, e):
    """Expansion operation"""
    return np.linalg.matrix_power(a, e)

def mcl_clusterize(a, e, i, steps=20):
    """MCL clustering algorithm"""
    a = norm_mat(a)
    for step in range(steps):
        a = expand(a, e)
        a = inflate(a, i)
    return a

def interpret_clusters(a):
    """Interpret the final matrix that MCL converges to and identify the clusters"""
    clusters=[]
    flag=[False for i in range(len(a))]
    for row in range(len(a)):
        clusternodes=[]
        for col in range(len(a[0])):
            if not flag[col] and a[row][col]!=0:
                clusternodes.append(col+1)
                flag[col]=True
        if clusternodes:
            clusters.append(clusternodes)
    return clusters         

def main():
    if len(sys.argv) == 4:
        inputfile = sys.argv[1]
        expansion_parameter, inflation_parameter = map(int, sys.argv[2:4])
    else:
        inputfile, expansion_parameter, inflation_parameter = 'graph.csv', 2, 2
    adjmat = read_adjmat(inputfile)
    a = mcl_clusterize(adjmat, expansion_parameter, inflation_parameter)
    clusters = interpret_clusters(a)
    for cluster in clusters:
        print '{' + ' '.join([str(i) for i in cluster]) +'}'

if __name__ == '__main__':
    main()