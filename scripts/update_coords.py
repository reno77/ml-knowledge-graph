#!/usr/bin/env python3
"""
Bake semantic coordinates from embed_ml_graph.py into static/graph.json.

Usage:
    python3 scripts/update_coords.py [coords.json] [graph.json]

    # Default:
    python3 scripts/update_coords.py /tmp/graph_coords.json static/graph.json
"""

import json
import sys

coords_file = sys.argv[1] if len(sys.argv) > 1 else '/tmp/graph_coords.json'
graph_file  = sys.argv[2] if len(sys.argv) > 2 else 'static/graph.json'

with open(graph_file) as f:
    graph = json.load(f)

with open(coords_file) as f:
    coords = {c['id']: c for c in json.load(f)}

updated = 0
for n in graph['nodes']:
    c = coords.get(n['id'])
    if c:
        n['sx'] = round(c['x'], 2)
        n['sy'] = round(c['y'], 2)
        n['sz'] = round(c['z'], 2)
        updated += 1
    else:
        print(f"  ⚠️  No coords for: {n['id']}")
        n.setdefault('sx', 0); n.setdefault('sy', 0); n.setdefault('sz', 0)

with open(graph_file, 'w') as f:
    json.dump(graph, f, indent=2)

print(f"✅ Updated {updated}/{len(graph['nodes'])} nodes in {graph_file}")
