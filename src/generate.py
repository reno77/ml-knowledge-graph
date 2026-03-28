#!/usr/bin/env python3
"""Generate ML knowledge graph as static HTML (pyvis interactive) and PNG."""

import json, os, sys
import networkx as nx
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from graph_data import NODES, EDGES, CATEGORY_COLORS

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'static')
os.makedirs(OUT_DIR, exist_ok=True)

def build_graph():
    G = nx.DiGraph()
    for name, (lv, cat) in NODES.items():
        G.add_node(name, level=lv, category=cat, color=CATEGORY_COLORS[cat])
    G.add_edges_from(EDGES)
    return G

def generate_png(G):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    level_nodes = {}
    for n, (lv, _) in NODES.items():
        level_nodes.setdefault(lv, []).append(n)

    pos = {}
    for lv, nlist in sorted(level_nodes.items()):
        xs = np.linspace(-len(nlist)*1.5, len(nlist)*1.5, len(nlist))
        for i, n in enumerate(nlist):
            pos[n] = (xs[i], -lv * 2.2)

    node_colors = [CATEGORY_COLORS[G.nodes[n]["category"]] for n in G.nodes]
    node_sizes  = [2400 if G.nodes[n]["level"] <= 1 else 1800 for n in G.nodes]

    fig, ax = plt.subplots(figsize=(22, 20))
    fig.patch.set_facecolor("#0d0d1a")
    ax.set_facecolor("#0d0d1a")

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#445566", arrows=True,
        arrowsize=18, width=1.4, alpha=0.7, connectionstyle="arc3,rad=0.05",
        min_source_margin=20, min_target_margin=20)

    for alpha, sm in [(0.15, 2.8), (0.3, 1.8), (1.0, 1.0)]:
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
            node_size=[s*sm for s in node_sizes], alpha=alpha)

    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8.5,
        font_color="white", font_weight="bold")

    legend_patches = [mpatches.Patch(color=c, label=k.title())
                      for k, c in CATEGORY_COLORS.items()]
    leg = ax.legend(handles=legend_patches, loc="lower right",
        facecolor="#1a1a2e", edgecolor="#445566", fontsize=10,
        title="Category", framealpha=0.9)
    plt.setp(leg.get_texts(), color='white')
    plt.setp(leg.get_title(), color='white')

    ax.set_title("Machine Learning Knowledge Graph",
        color="white", fontsize=20, fontweight="bold", pad=20)
    ax.axis("off")
    plt.tight_layout()
    out = os.path.join(OUT_DIR, 'graph.png')
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"PNG saved: {out}")

def generate_json(G):
    """Export graph as JSON for the interactive JS viewer."""
    nodes_export = []
    for n in G.nodes:
        nodes_export.append({
            "id": n,
            "label": n,
            "level": G.nodes[n]["level"],
            "category": G.nodes[n]["category"],
            "color": CATEGORY_COLORS[G.nodes[n]["category"]],
        })
    edges_export = [{"from": u, "to": v} for u, v in G.edges]
    out = os.path.join(OUT_DIR, 'graph.json')
    with open(out, 'w') as f:
        json.dump({"nodes": nodes_export, "edges": edges_export,
                   "categories": CATEGORY_COLORS}, f, indent=2)
    print(f"JSON saved: {out}")

if __name__ == "__main__":
    G = build_graph()
    generate_png(G)
    generate_json(G)
    print("Done.")
