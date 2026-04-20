###############################
#   Author: Tverdohleb Egor   #
###############################
import igraph as ig
import matplotlib.pyplot as plt
import datetime

graphs = [
    (ig.Graph.Read_GraphML("data/graphml/snapshot_2020_10.graphml"), datetime.date(2020, 10, 1)),
    (ig.Graph.Read_GraphML("data/graphml/snapshot_2020_11.graphml"), datetime.date(2020, 11, 1)),
    (ig.Graph.Read_GraphML("data/graphml/snapshot_2020_12.graphml"), datetime.date(2020, 12, 1)),
    (ig.Graph.Read_GraphML("data/graphml/snapshot_2021_01.graphml"), datetime.date(2021, 1, 1)),
    (ig.Graph.Read_GraphML("data/graphml/snapshot_2021_09.graphml"), datetime.date(2021, 9, 1)),
    (ig.Graph.Read_GraphML("data/graphml/snapshot_2023_09.graphml"), datetime.date(2023, 9, 1))
]

dates = []
clustering_coefficients = []

for graph, date in graphs:
    cc_global = graph.transitivity_avglocal_undirected()
    dates.append(date)
    clustering_coefficients.append(cc_global)
    print(f"Date: {date.strftime('%Y-%m')} | Clustering coefficient: {cc_global:.4f}")

plt.figure(figsize=(10, 6))

plt.plot(dates, clustering_coefficients, marker='o', linestyle='-', color='b')

plt.title('Average Local Transitivity (Clustering Coefficient) Over Time')
plt.xlabel('Date')
plt.ylabel('Clustering Coefficient')
plt.grid(True, linestyle='--', alpha=0.7)

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plots/clusteringCoefficient.png', dpi=300, bbox_inches='tight')
