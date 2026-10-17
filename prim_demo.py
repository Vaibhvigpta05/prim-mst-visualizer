

"""Prim's MST - step-by-step visualiser (matplotlib only).
 
Usage:
    python prim_demo.py                # saves figures/frame0..frame6.png
    python prim_demo.py --start D      # start from another vertex
    python prim_demo.py --gif          # also saves prim.gif (needs pillow)
"""
import argparse
import heapq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
 
NAVY, ORANGE, GREEN, GREY = "#1F3864", "#E08A00", "#2E8B57", "#B0B0B0"
 
POS = {"A": (0, 1.5), "B": (2, 3), "C": (4.6, 3.2), "D": (2, 0),
       "E": (4.6, 1.5), "F": (4.6, -0.2), "G": (7, 1.5)}
EDGES = [("A", "B", 7), ("A", "D", 5), ("B", "C", 8), ("B", "D", 9),
         ("B", "E", 7), ("C", "E", 5), ("D", "E", 15), ("D", "F", 6),
         ("E", "F", 8), ("E", "G", 9), ("F", "G", 11)]
 
 
def adjacency(edges=EDGES):
    g = {}
    for u, v, w in edges:
        g.setdefault(u, []).append((v, w))
        g.setdefault(v, []).append((u, w))
    return g
 
 
def prim_steps(graph, start="A"):
    """Return list of (vertex_added, edge_used or None, keys_after_update)."""
    INF = float("inf")
    key = {v: INF for v in graph}
    parent = {v: None for v in graph}
    key[start] = 0
    in_tree, steps = set(), []
    heap = [(0, start)]
    while heap:
        k, u = heapq.heappop(heap)
        if u in in_tree:
            continue
        in_tree.add(u)
        for v, w in graph[u]:
            if v not in in_tree and w < key[v]:
                key[v], parent[v] = w, u
                heapq.heappush(heap, (w, v))
        edge = (parent[u], u, k) if parent[u] else None
        steps.append((u, edge, dict(key), set(in_tree)))
    return steps
 
 
def draw_state(ax, in_tree, tree_edges, chosen=None, title=""):
    ax.set_title(title, fontsize=10, color=NAVY, fontweight="bold")
    tset = {frozenset((u, v)) for u, v, _ in tree_edges}
    for u, v, w in EDGES:
        (x1, y1), (x2, y2) = POS[u], POS[v]
        fs = frozenset((u, v))
        crossing = (u in in_tree) != (v in in_tree)
        if chosen and fs == frozenset(chosen[:2]):
            ax.plot([x1, x2], [y1, y2], color=GREEN, lw=4, zorder=1)
        elif fs in tset:
            ax.plot([x1, x2], [y1, y2], color=NAVY, lw=3, zorder=1)
        elif crossing:
            ax.plot([x1, x2], [y1, y2], color=ORANGE, lw=1.8, ls="--", zorder=1)
        else:
            ax.plot([x1, x2], [y1, y2], color=GREY, lw=1, zorder=1)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, str(w), fontsize=8, ha="center",
                va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    for v, (x, y) in POS.items():
        inside = v in in_tree
        ax.scatter([x], [y], s=520, zorder=4, color=NAVY if inside else "#EAF1FB",
                   edgecolors=NAVY, linewidths=1.5)
        ax.text(x, y, v, color="white" if inside else NAVY, ha="center",
                va="center", fontsize=11, fontweight="bold", zorder=5)
    ax.set_xlim(-0.8, 7.8); ax.set_ylim(-0.9, 3.8)
    ax.set_aspect("equal"); ax.axis("off")
 
 
def states(start="A"):
    """Yield (in_tree, tree_edges, chosen_edge, title) for every stage."""
    out, tree, seen = [], [], set()
    for i, (u, edge, key, S) in enumerate(prim_steps(adjacency(), start)):
        if edge:
            tree = tree + [edge]
        seen = S
        title = f"Start: add {u}" if i == 0 else f"Step {i}: add {u} via {edge[0]}-{u} ({edge[2]})"
        out.append((set(S), list(tree), edge, title))
    return out
 
 
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="A")
    ap.add_argument("--gif", action="store_true")
    a = ap.parse_args()
    sts = states(a.start)
    for i, (S, T, ch, t) in enumerate(sts):
        fig, ax = plt.subplots(figsize=(6, 3.6))
        draw_state(ax, S, T, ch, t)
        fig.savefig(f"figures/frame{i}.png", dpi=200, bbox_inches="tight")
        plt.close(fig)
    print("MST weight:", sum(w for *_, w in sts[-1][1]))
    if a.gif:
        from PIL import Image
        imgs = [Image.open(f"figures/frame{i}.png") for i in range(len(sts))]
        imgs[0].save("prim.gif", save_all=True, append_images=imgs[1:], duration=1200, loop=0)
 
 
if __name__ == "__main__":
    main()
 

