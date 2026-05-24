###############################
#   Author: Tverdohleb Egor   #
###############################
import igraph as ig
import networkit as nk
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os
import time
import math
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

BLOCKCHAINS = {
    "bitcoin":  [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "ethereum": [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    # BigQuery non conteneva dati significativa per Dogecoin 2025
    "dogecoin": [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    "litecoin": [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
}

categories = ["channels >= 2", "top10 removed", "top100 removed"]
SAMPLE_SIZE = 10000
APL_SAMPLE  = 1000   # sample size per APL 
APL_TARGETS = 500    # target per la stima dell'APL 


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def get_nc(g):
    n = g.vcount()
    if n <= 2:
        return 0
    degs = g.degree()
    d_max = max(degs)
    return sum(d_max - d for d in degs) / ((n - 1) * (n - 2))


def igraph_to_networkit(g_ig):
    n = g_ig.vcount()
    G_nk = nk.Graph(n, weighted=False, directed=False)
    for e in g_ig.es:
        G_nk.addEdge(e.source, e.target)
    return G_nk


def compute_betweenness_nk(g_ig, sample_size):
    log(f"    Converting graph to NetworKit format...")
    G_nk = igraph_to_networkit(g_ig)

    log(f"    Running ApproxBetweenness (epsilon=0.1, parallel on {nk.getMaxNumberOfThreads()} threads)...")
    # epsilon=0.1 approssimazione, delta=0.1 confidence
    bcc = nk.centrality.ApproxBetweenness(G_nk, epsilon=0.1, delta=0.1)
    bcc.run()

    scores_all = bcc.scores()
    n = g_ig.vcount()
    sample = random.sample(range(n), min(sample_size, n))
    bet_sample = [scores_all[v] for v in sample]
    degs_sample = [g_ig.degree(v) for v in sample]

    return degs_sample, bet_sample


def compute_apl_sampled(g_ig, apl_sample=APL_SAMPLE, apl_targets=APL_TARGETS):
    n = g_ig.vcount()
    sources = random.sample(range(n), min(apl_sample, n))
    all_dists = []
    for src in sources:
        targets = random.sample(range(n), min(apl_targets, n))
        row = g_ig.shortest_paths(source=src, target=targets, mode="all")[0]
        finite = [d for d in row if d > 0 and d != float('inf')]
        all_dists.extend(finite)
    return np.mean(all_dists) if all_dists else float('nan')


def plot_temporal(results, key, ylabel, title, fname, destination):
    plt.figure(figsize=(9, 5))
    styles = {
        'channels >= 2':  {'color': 'orange', 'ls': '-', 'lw': 1.5, 'zorder': 1},
        'top10 removed': {'color': 'green',  'ls': '-', 'lw': 1.5, 'zorder': 3},
        'top100 removed':{'color': 'red',    'ls': '-', 'lw': 1.5, 'zorder': 4},
    }
    for cat in categories:
        if not results[cat]["dates"]:
            continue
        plt.plot(
            results[cat]["dates"], results[cat][key],
            label=cat, color=styles[cat]['color'],
            linestyle=styles[cat]['ls'], linewidth=styles[cat]['lw'],
            marker='o', markersize=5, zorder=styles[cat]['zorder'],
        )
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Year")
    plt.legend(title="Category", loc='best')
    plt.grid(True, linestyle='-', alpha=0.4)
    plt.tight_layout()
    path = os.path.join(destination, f"{fname}.png")
    plt.savefig(path)
    plt.close()
    log(f"  Saved {path}")


for blockchain, years in BLOCKCHAINS.items():
    destination = os.path.join(SCRIPT_DIR, "plots", blockchain)
    os.makedirs(destination, exist_ok=True)
    log(f"=== Processing {blockchain.upper()} ===")

    results = {cat: {"dates": [], "and": [], "acc": [], "nc": [], "comp": []} for cat in categories}
    g_full_last = None

    for year in years:
        path = os.path.join(SCRIPT_DIR, f"{blockchain}_{year}.graphml")
        if not os.path.exists(path):
            log(f"  Skipping {path} - not found")
            continue

        log(f"  Reading {path}...")
        g_full = ig.Graph.Read_GraphML(path)
        g_full_last = g_full
        log(f"  Nodes: {g_full.vcount()}, Edges: {g_full.ecount()}")

        g_min2 = g_full.subgraph(g_full.vs.select(_degree_gt=2))
        vs_sorted = sorted(g_min2.vs, key=lambda v: v.degree(), reverse=True)

        mapping = {
            "channels >= 2":  g_min2,
            "top10 removed": g_min2.subgraph([v.index for v in vs_sorted[10:]]),
            "top100 removed":g_min2.subgraph([v.index for v in vs_sorted[100:]]),
        }

        date = datetime.date(year, 12, 1)
        for cat in categories:
            graph = mapping[cat]
            results[cat]["dates"].append(date)
            results[cat]["and"].append(np.mean(graph.degree()))
            results[cat]["acc"].append(graph.transitivity_avglocal_undirected())
            results[cat]["nc"].append(get_nc(graph))
            results[cat]["comp"].append(len(graph.connected_components()))
            log(f"    [{cat}] AND={results[cat]['and'][-1]:.4f} CC={results[cat]['acc'][-1]:.4f}")

    if g_full_last is None:
        log(f"  No data for {blockchain}, skipping plots.")
        continue

    log(f"  Plotting degree distribution...")
    plt.figure(figsize=(7, 5))
    degs = g_full_last.degree()
    if degs != None and len(degs) > 0 and max(degs) > 0:
        bins = np.logspace(0, np.log10(max(degs)), 50)
        plt.hist(degs, bins=bins, density=True, color='#4e79a7', alpha=0.7, edgecolor='black')
        plt.xscale('log')
        plt.yscale('log')
    plt.title(f"Degree Distribution (Log-Log) - {blockchain.capitalize()} - Last Year")
    plt.xlabel("Degree k (log scale)")
    plt.ylabel("Frequency P(k) (log scale)")
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.savefig(os.path.join(destination, "DegreeDistribution.png"))
    plt.close()

    log(f"  Calculating betweenness centrality (NetworKit ApproxBetweenness, epsilon=0.1)...")
    sample_degs, bet = compute_betweenness_nk(g_full_last, SAMPLE_SIZE)

    plt.figure(figsize=(7, 5))
    plt.scatter(sample_degs, bet, alpha=0.6, color='blue', s=20)
    plt.title(f"Degree vs Betweenness - {blockchain.capitalize()} - Last Year\n(ApproxBetweenness epsilon=0.1, sampled {SAMPLE_SIZE:,} nodes for plot)")
    plt.xlabel("Degree")
    plt.ylabel("Betweenness Centrality (approx)")
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(destination, "NodeDegreeBetweennessCentrality.png"))
    plt.close()

    log(f"  Calculating APL (sample={APL_SAMPLE} sources × {APL_TARGETS} targets)...")
    apl = compute_apl_sampled(g_full_last, APL_SAMPLE, APL_TARGETS)

    n = g_full_last.vcount()
    m = g_full_last.ecount()
    p = m / (n * (n - 1))
    apl_random = math.log(n) / math.log(max(n * p, 1.0001))
    cc = g_full_last.transitivity_avglocal_undirected()

    log(f"  APL real:   {apl:.4f}")
    log(f"  APL random: {apl_random:.4f}")
    log(f"  CC:         {cc:.4f}")

    plt.figure(figsize=(7, 5))
    metrics = [f"APL real\n(s={APL_SAMPLE}×{APL_TARGETS})", "APL random\n(theoretical)", "Clustering\nCoefficient"]
    values  = [apl, apl_random, cc]
    colors  = ['#4e79a7', '#f28e2b', '#59a14f']
    plt.bar(metrics, values, color=colors, edgecolor='black')
    plt.title(f"Small-World Check - {blockchain.capitalize()} - Last Year")
    plt.ylabel("Value")
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(destination, "SmallWorld.png"))
    plt.close()

    log(f"  Plotting temporal metrics...")
    plot_temporal(results, "and",  "AND",   f"Average Neighbors Degree - {blockchain.capitalize()}", "AverageNeighborsDegree", destination)
    plot_temporal(results, "acc",  "CC",    f"Clustering Coefficient - {blockchain.capitalize()}",   "ClusteringCoefficient",  destination)
    plot_temporal(results, "comp", "Count", f"Connected Components - {blockchain.capitalize()}",     "ConnectedComponents",    destination)
    plot_temporal(results, "nc",   "NC",    f"Network Centralization - {blockchain.capitalize()}",   "NetworkCentralization",  destination)

    log(f"=== Done {blockchain.upper()} ===\n")

log("All done!")
