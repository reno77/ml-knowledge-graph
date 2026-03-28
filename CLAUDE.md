# ML Knowledge Graph

Interactive 3D knowledge graph of ~700 ML concepts, visualised with 3D-force-graph + Three.js.

## Architecture

- **Frontend**: Single-file vanilla JS app in `static/index.html` (no build step, CDN deps)
- **Backend**: FastAPI serving `static/` as a static site (`server.py`)
- **Data**: Pre-generated `static/graph.json` — 478 nodes, 554 edges, 7 categories

### Data pipeline (offline)

```
src/graph_data.py  →  src/generate.py  →  static/graph.json + graph.png
                                    ↓
              scripts/embed_ml_graph.py   (sentence-transformers + UMAP)
                                    ↓
              scripts/update_coords.py    (bakes sx/sy/sz into graph.json)
```

## Running

```bash
# Install runtime deps
pip install fastapi uvicorn

# Start server (default port 8000)
python3 server.py
# or explicit port
uvicorn server:app --port 8081
```

Open `http://localhost:8000` (or the port you chose).

## Regenerating graph data

Edit `src/graph_data.py`, then:

```bash
# Rebuild graph.json + graph.png
pip install networkx numpy matplotlib
python3 src/generate.py

# Recompute semantic 3D coords (GPU recommended)
pip install sentence-transformers umap-learn numpy
python3 scripts/embed_ml_graph.py static/graph.json /tmp/graph_coords.json
python3 scripts/update_coords.py /tmp/graph_coords.json static/graph.json
```

## Key files

| File | Purpose |
|------|---------|
| `src/graph_data.py` | Source of truth — all nodes and prerequisite edges |
| `src/generate.py` | Rebuilds `graph.json` and `graph.png` from graph_data |
| `static/index.html` | Entire frontend application |
| `static/graph.json` | Pre-built graph (served directly to browser) |
| `scripts/embed_ml_graph.py` | Computes sentence-transformer embeddings + UMAP coords |
| `scripts/update_coords.py` | Bakes semantic coords into graph.json |

## Graph schema

- **Nodes**: id, label, category (`foundation`/`core`/`supervised`/`unsupervised`/`ensemble`/`neural`/`advanced`), level (0–6), description, x/y/z (spiral layout), sx/sy/sz (semantic layout)
- **Edges**: source, target (directed prerequisite relationship)

## Layout modes

- **Spiral**: level-based hierarchy in spiral arms
- **Semantic**: positions from `all-MiniLM-L6-v2` cosine similarity reduced to 3D via UMAP

## No test suite, CI, or requirements.txt

There are no automated tests or lock files. Dependencies are listed above per task.
