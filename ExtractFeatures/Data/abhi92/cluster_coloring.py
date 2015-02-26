"""
Draws the graph whose adjacency matrix(weighted) is in GRAPHFILE using the
fruchterman reingold layout and gives the different clusters(partition not 
cover) given in CLUSTERFILE different colors(matplotlib jet colormap values 
given in COLORFILE) and plots it and saves the image as a jpg file
"""
#!/usr/bin/env python
import networkx as nx
import matplotlib.pyplot as plt
import sys
import mcl
from random import shuffle
GRAPHFILE=sys.argv[1]
CLUSTERFILE=sys.argv[2]
COLORFILE="colors"
def draw_clusters(G, clusterfile):
    with open(clusterfile) as ifile:
        """colors is list of allowed colors for the clusters"""
        with open(COLORFILE) as cfile:
            colors = cfile.readlines()
        shuffle(colors)
        colormap={}
        i=0
        for line in ifile:
            clusternodes = line.split()
            for node in clusternodes:
                colormap[node] = float(colors[i])
            i+=1
    values = [colormap[str(node+1)] for node in G.nodes()]
    """Drawing starts"""
    node_labels = {i:str(i+1) for i in G.nodes()}
    node_pos = nx.fruchterman_reingold_layout(G)
    edge_widths = [(G.get_edge_data(u,v)['weight']/100.0)*3 
                    for (u,v) in G.edges()]
    nx.draw_networkx(G, cmap='jet', pos=node_pos, node_color = values, 
                        labels=node_labels, width=edge_widths)
    plt.savefig(clusterfile+'-visual.jpg', dpi=200)
    plt.show()

def main():
    G = nx.Graph(mcl.read_adjmat(GRAPHFILE))
    draw_clusters(G,CLUSTERFILE)