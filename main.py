###############################
#   Author: Tverdohleb Egor   #
###############################
import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os

os.makedirs('plots', exist_ok=True)

snapshots = [
    ("data/graphml/snapshot_2019_01.graphml", datetime.date(2019,1,1)),       
    ("data/graphml/snapshot_2019_07.graphml", datetime.date(2019,7,1)),       
    ("data/graphml/snapshot_2020_01.graphml", datetime.date(2020,1,1)),       
    ("data/graphml/snapshot_2020_07.graphml", datetime.date(2020,7,1)),       
    ("data/graphml/snapshot_2021_01.graphml", datetime.date(2021,1,1)),       
    ("data/graphml/snapshot_2021_07.graphml", datetime.date(2021,7,1)),       
    ("data/graphml/snapshot_2022_01.graphml", datetime.date(2022,1,1)),
    ("data/graphml/snapshot_2022_07.graphml", datetime.date(2022,7,1)),
    ("data/graphml/snapshot_2023_01.graphml", datetime.date(2023,1,1)),
    ("data/graphml/snapshot_2023_07.graphml", datetime.date(2023,7,1)),
]

categories = ["unfiltered", "channels > 2", "top10 removed", "top100 removed"]
results = {cat: {"dates": [], "and": [], "acc": [], "nc": [], "comp": []} for cat in categories}

def get_nc(g):
    n = g.vcount()
    if n <= 2: return 0
    degs = g.degree()
    d_max = max(degs)
    return sum(d_max - d for d in degs) / ((n - 1) * (n - 2))

for path, date in snapshots:
    if not os.path.exists(path):
        print(f"Skipping {path} - not found")
        continue
        
    g_full = ig.Graph.Read_GraphML(path)
    g_min2 = g_full.subgraph(g_full.vs.select(_degree_gt=2))
    vs_sorted = sorted(g_min2.vs, key=lambda v: v.degree(), reverse=True)
    
    mapping = {
        "unfiltered": g_full,
        "channels > 2": g_min2,
        "top10 removed": g_min2.subgraph([v.index for v in vs_sorted[10:]]),
        "top100 removed": g_min2.subgraph([v.index for v in vs_sorted[100:]])
    }

    for cat in categories:
        graph = mapping[cat]
        results[cat]["dates"].append(date)
        results[cat]["and"].append(np.mean(graph.degree()))
        results[cat]["acc"].append(graph.transitivity_avglocal_undirected())
        results[cat]["nc"].append(get_nc(graph))
        results[cat]["comp"].append(len(graph.connected_components()))

plt.figure(figsize=(7, 5))
degs = g_full.degree()
bins = np.logspace(0, np.log10(max(degs)), 50)
plt.hist(degs, bins=bins, density=True, color='#4e79a7', alpha=0.7, edgecolor='black')
plt.xscale('log')
plt.yscale('log')
plt.title("Degree Distribution (Log-Log) - All Nodes")
plt.xlabel("Degree k (log scale)")
plt.ylabel("Frequency P(k) (log scale)")
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.savefig('plots/DegreeDistribution.png')

plt.figure(figsize=(7, 5))
bet = g_full.betweenness()
plt.scatter(g_full.degree(), bet, alpha=0.6, color='blue', s=20)
plt.title("Relationship between node degree and betweenness centrality")
plt.xlabel("Degree")
plt.ylabel("Betweenness Centrality")
plt.grid(True, alpha=0.3)
plt.savefig('plots/NodeDegreeBetweennessCentrality.png')

def plot_temporal(key, ylabel, title, fname):
    plt.figure(figsize=(9, 5))
    
    styles = {
        'unfiltered': {'color': 'blue', 'ls': '--', 'lw': 2.5, 'zorder': 2},
        'channels > 2': {'color': 'orange', 'ls': '-', 'lw': 1.5, 'zorder': 1},
        'top10 removed': {'color': 'green', 'ls': '-', 'lw': 1.5, 'zorder': 3},
        'top100 removed': {'color': 'red', 'ls': '-', 'lw': 1.5, 'zorder': 4}
    }

    for cat in categories:
        plt.plot(
            results[cat]["dates"], 
            results[cat][key], 
            label=cat, 
            color=styles[cat]['color'],
            linestyle=styles[cat]['ls'],
            linewidth=styles[cat]['lw'],
            marker='o', 
            markersize=5,
            zorder=styles[cat]['zorder']
        )
    
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Year")
    plt.legend(title="Category", loc='best')
    plt.grid(True, linestyle='-', alpha=0.4)
    plt.tight_layout()
    plt.savefig(f'plots/{fname}.png')

plot_temporal("and", "AND", "Average Neighbors Degree (AND) over time", "AverageNeighborsDegree")
plot_temporal("acc", "CC", "Clustering Coefficient (CC) over time", "ClusteringCoefficient")
plot_temporal("comp", "Count", "Connected Components over time", "ConnectedComponents")
plot_temporal("nc", "NC", "Network Centralization (NC) over time", "NetworkCentralization")
