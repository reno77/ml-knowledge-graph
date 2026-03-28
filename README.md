# ML Knowledge Graph

An interactive 3D knowledge graph of **484 Machine Learning concepts** with **575 prerequisite edges** across 7 categories, built with [3d-force-graph](https://github.com/vasturiano/3d-force-graph) and Three.js.

## Live Demo

Deployed on [Vercel](https://ml-knowledge-graph.vercel.app) or run locally (see below).

## Features

- **3D interactive** — drag, zoom, pan with orbit controls
- **Semantic layout** (default) — nodes positioned by cosine similarity using sentence-transformer embeddings + UMAP 3D
- **Timeline layout** — nodes positioned by year of origin (1640–present) with power-law/log scale slider and year range filter
- **Search with autocomplete** — partial matches, keyboard navigation, highlighted subgraph
- **Click any node** — highlights connections, shows prerequisites/enables, depth slider (1–3 hops)
- **Node info panel** — category, level, year of discovery, Grokipedia summary, arXiv/GitHub paper links
- **Lock mode** — lock focus on a node to prevent accidental clicks; unlock separately from clearing highlights
- **Filter panel** — toggle categories, levels, connection types (same-category, cross-category, level-up, level-same, incoming, outgoing)
- **Translucent mode** — reduce node opacity to see labels clearly
- **Rotation gizmo** — Maya-style axis-constrained orbit (X/Y/Z) with auto-rotate
- **Reset controls** — reset all filters or reset camera view independently
- **Panel show/hide** toggle

## Layout Modes

| Mode | How it works |
|------|-------------|
| Semantic (default) | Nodes positioned by `all-MiniLM-L6-v2` cosine similarity reduced to 3D via UMAP |
| Timeline | X-axis = year of concept origin, Y/Z = category/level jitter. Adjustable power-law scale and year range sliders |

## Node Summaries

Each node includes a pre-fetched summary from [Grokipedia](https://grokipedia.com) with a direct page link. Summaries are embedded in `graph.json` (no runtime API calls needed).

## Running Locally

```bash
# Install dependencies
pip install fastapi uvicorn

# Start server
python3 server.py
# or
uvicorn server:app --port 8081

# Open http://localhost:8000
```

## Deploying to Vercel

The project deploys as a static site. `vercel.json` is configured to serve from `static/` with no build step.

## Re-generating Graph Data

```bash
# Edit source of truth
vim src/graph_data.py

# Rebuild graph.json + graph.png
pip install networkx numpy matplotlib
python3 src/generate.py
```

## Re-generating Semantic Coordinates

Run on a machine with GPU for speed (RTX 3090 takes ~3 seconds):

```bash
pip install sentence-transformers umap-learn numpy

# Generate embeddings + UMAP coords
python3 scripts/embed_ml_graph.py static/graph.json /tmp/graph_coords.json

# Bake into graph.json
python3 scripts/update_coords.py /tmp/graph_coords.json static/graph.json
```

## Key Files

| File | Purpose |
|------|---------|
| `src/graph_data.py` | Source of truth — all nodes and prerequisite edges |
| `src/generate.py` | Rebuilds `graph.json` and `graph.png` from graph_data |
| `static/index.html` | Entire frontend application (single file, no build step) |
| `static/graph.json` | Pre-built graph with nodes, edges, summaries, and semantic coords |
| `scripts/embed_ml_graph.py` | Computes sentence-transformer embeddings + UMAP coords |
| `scripts/update_coords.py` | Bakes semantic coords into graph.json |
| `server.py` | FastAPI static file server |
| `vercel.json` | Vercel deployment config |

## Stack

- **Frontend**: Vanilla JS + [3d-force-graph](https://github.com/vasturiano/3d-force-graph) + [Three.js](https://threejs.org/) + [three-spritetext](https://github.com/vasturiano/three-spritetext)
- **Backend**: FastAPI static file server
- **Summaries**: [Grokipedia](https://grokipedia.com) (pre-fetched, embedded in graph.json)
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimensionality reduction**: UMAP (cosine metric, 3 components)
- **Deployment**: Vercel (static)

## Graph Schema

- **Nodes**: id, label, category (foundation/core/supervised/unsupervised/ensemble/neural/advanced), level (0–6), summary, color, sx/sy/sz (semantic coords)
- **Edges**: source → target (directed prerequisite relationship)
- **Categories**: 7 (foundation, core, supervised, unsupervised, ensemble, neural, advanced)
- **Levels**: 0 (foundations) through 6 (expert/cutting-edge)
