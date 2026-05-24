import igraph as ig
import random

g = ig.Graph.Read_GraphML("./snapshot_2023.graphml")

cc_global = g.transitivity_avglocal_undirected()

print(f"Global clustering coefficient: {cc_global}")
