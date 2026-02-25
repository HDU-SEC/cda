# Step 1 — Gadget Identification

In this step, we use CodeQL to identify cross-domain gadgets that can be leveraged for CDA.

Specifically, we specify:

- a source function (`src`)
- a destination function (`dst`)

We then perform a depth-first search (DFS) over the call graph to discover all feasible call paths connecting `src` to `dst`.  
Each valid path corresponds to a candidate cross-domain gadget.

In our current implementation, we focus on MMIO-related paths and extract stack-based gadgets derived from MMIO interactions.

To run the analysis:

```bash
python3 main.py
```



