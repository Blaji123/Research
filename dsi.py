import math
import csv
from math import sin
from heapq import heappush, heappop

class DynamicGraphFile:
    def __init__(self, filename):
        self.edges = []
        self.n = 0
        self.load_file(filename)

    def load_file(self, filename):
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                u, v, a, b = row
                u, v = int(u), int(v)
                a, b = float(a), float(b)
                self.edges.append((u, v, a, b))
                self.n = max(self.n, u, v)

    def get_weights(self, t):
        weighted = []
        for (u, v, a, b) in self.edges:
            w = a + b * math.sin(t)
            weighted.append((w, u, v))
        return weighted


def kruskal_mst(n, weighted_edges):
    parent = list(range(n+1))
    rank = [0] * (n+1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        else:
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
        return True

    mst = []
    total = 0
    for w, u, v in sorted(weighted_edges):
        if union(u, v):
            mst.append((u, v, w))
            total += w
    return mst, total


def mst_stability(prev_mst, new_mst):
    set_prev = {(min(u, v), max(u, v)) for (u, v, _) in prev_mst}
    set_new  = {(min(u, v), max(u, v)) for (u, v, _) in new_mst}
    return len(set_prev.symmetric_difference(set_new))


def run_experiment(filename):
    g = DynamicGraphFile(filename)

    prev_mst = None
    results = []

    for t in range(0, 101, 5):
        edges_t = g.get_weights(t)
        mst, total = kruskal_mst(g.n, edges_t)

        if prev_mst is None:
            stability = 0
        else:
            stability = mst_stability(prev_mst, mst)

        results.append((t, total, stability))
        prev_mst = mst

    return results


if __name__ == "__main__":
    out = run_experiment("edges.csv")
    for t, total, stab in out:
        print(f"t={t:3d}  total={total:.2f}   schimbari={stab}")
