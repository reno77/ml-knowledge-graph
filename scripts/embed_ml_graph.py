#!/usr/bin/env python3
"""
Generate semantic 3D coordinates for ML Knowledge Graph nodes.

Uses sentence-transformers (all-MiniLM-L6-v2) to embed concept names,
then UMAP to reduce to 3D. The resulting coordinates represent cosine
similarity — semantically related concepts cluster together.

Requirements:
    pip install sentence-transformers umap-learn numpy

Usage:
    python3 embed_ml_graph.py [path/to/graph.json] [output_coords.json]

    # From repo root:
    python3 scripts/embed_ml_graph.py static/graph.json /tmp/graph_coords.json

The output JSON is a list of {id, x, y, z} dicts.
To bake coords into graph.json, run update_coords.py after this.
"""

import json
import sys
import os
import numpy as np

def main():
    graph_file  = sys.argv[1] if len(sys.argv) > 1 else 'static/graph.json'
    output_file = sys.argv[2] if len(sys.argv) > 2 else '/tmp/graph_coords.json'

    with open(graph_file) as f:
        data = json.load(f)
    nodes = data['nodes'] if 'nodes' in data else data

    labels = [n['id'] for n in nodes]
    print(f"Embedding {len(labels)} concepts...", flush=True)

    # Enrich with category for better contextual embeddings
    enriched = [f"{n['id']} ({n['category']} in machine learning)" for n in nodes]

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("Installing sentence-transformers...")
        os.system("pip install sentence-transformers --break-system-packages -q")
        from sentence_transformers import SentenceTransformer

    try:
        import umap
    except ImportError:
        print("Installing umap-learn...")
        os.system("pip install umap-learn --break-system-packages -q")
        import umap

    print("Loading all-MiniLM-L6-v2...", flush=True)
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Computing embeddings...", flush=True)
    embeddings = model.encode(enriched, show_progress_bar=True, batch_size=64)
    print(f"Embeddings shape: {embeddings.shape}", flush=True)

    print("Running UMAP 3D reduction (cosine metric)...", flush=True)
    reducer = umap.UMAP(
        n_components=3,
        n_neighbors=15,
        min_dist=0.2,
        metric='cosine',
        random_state=42,
        spread=3.0,
    )
    coords = reducer.fit_transform(embeddings)
    print(f"UMAP done. Shape: {coords.shape}", flush=True)

    # Normalize to ~[-300, 300] range
    scale = 300
    coords = coords - coords.mean(axis=0)
    coords = coords / (coords.std() + 1e-8) * scale

    out = [
        {'id': n['id'], 'x': float(x), 'y': float(y), 'z': float(z)}
        for n, (x, y, z) in zip(nodes, coords)
    ]

    with open(output_file, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\n✅ Saved {len(out)} coords → {output_file}", flush=True)

    # Print cluster sample
    print("\nSample coordinates:")
    for item in out[:6]:
        print(f"  {item['id']}: ({item['x']:.1f}, {item['y']:.1f}, {item['z']:.1f})")

if __name__ == '__main__':
    main()
