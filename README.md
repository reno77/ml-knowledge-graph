# 🧠 ML Knowledge Graph

An interactive 3D knowledge graph of Machine Learning concepts built with [3d-force-graph](https://github.com/vasturiano/3d-force-graph).

**234 concepts · 279 prerequisite edges · Two layout modes**

## Live Demo
> Deploy locally (see below) or open `static/index.html` via a static file server.

## Features
- **3D interactive** — drag, zoom, pan
- **Spiral layout** — level-based hierarchy (foundations → expert)
- **Semantic layout** — nodes positioned by cosine similarity using sentence-transformer embeddings + UMAP 3D
- **Search with autocomplete** — partial matches, keyboard navigation, highlighted results
- **Click any node** — highlights connections, shows prerequisites/enables, depth slider (1–3 hops)
- **Filter panel** — toggle categories, levels, connection types
- **Panel show/hide** toggle

## Layout Modes

| Mode | How it works |
|------|-------------|
| 🌀 Spiral | Nodes arranged in spiral arms by level (0=foundations → 6=expert) |
| 🧠 Semantic | Nodes positioned by `all-MiniLM-L6-v2` cosine similarity → UMAP 3D reduction |

## Running Locally

```bash
# Install dependencies
pip install fastapi uvicorn

# Start server
python3 server.py
# or
uvicorn server:app --port 8081

# Open http://localhost:8081
```

## Re-generating Semantic Coordinates

Run on a machine with GPU for speed (RTX 3090 takes ~3 seconds):

```bash
# 1. Install deps
pip install sentence-transformers umap-learn numpy

# 2. Generate embeddings + UMAP coords
python3 scripts/embed_ml_graph.py static/graph.json /tmp/graph_coords.json

# 3. Bake into graph.json
python3 scripts/update_coords.py /tmp/graph_coords.json static/graph.json
```

## Adding New Concepts

Edit `src/graph_data.py` — add nodes and edges, then regenerate:

```bash
python3 src/generate.py          # regenerates static/graph.json + graph.png
python3 scripts/embed_ml_graph.py    # recompute embeddings
python3 scripts/update_coords.py     # bake into graph.json
```

## Stack
- Frontend: vanilla JS + [3d-force-graph](https://github.com/vasturiano/3d-force-graph) + [three-spritetext](https://github.com/vasturiano/three-spritetext)
- Backend: FastAPI static file server
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2`
- Dimensionality reduction: UMAP (cosine metric, 3 components)
