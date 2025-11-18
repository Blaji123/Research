import math
import csv

class DynamicEdge:
    def __init__(self, u, v, a, b, idx):
        self.u = u
        self.v = v
        self.a = a
        self.b = b
        self.idx = idx

    def weight(self, t):
        return self.a + self.b * math.sin(t)


class DSU:
    def __init__(self, n):
        self.p = list(range(n + 1))
        self.r = [0] * (n + 1)

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1
        return True


def kruskal_dynamic(edges, n, t):
    sorted_edges = sorted(edges, key=lambda e: e.weight(t))

    dsu = DSU(n)
    mst = []
    total_cost = 0.0

    for e in sorted_edges:
        if dsu.union(e.u, e.v):
            mst.append(e.idx)
            total_cost += e.weight(t)
        if len(mst) == n - 1:
            break

    return mst, total_cost

def detect_changes(edges, n, t_values):
    prev_mst = None
    changes = []

    for t in t_values:
        mst, cost = kruskal_dynamic(edges, n, t)
        if prev_mst is not None and mst != prev_mst:
            changes.append((t, prev_mst, mst))
        prev_mst = mst

    return changes

def load_edges_csv(fname):
    edges = []
    idx = 0
    max_node = 0

    with open(fname) as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            u = int(row[0])
            v = int(row[1])
            a = float(row[2])
            b = float(row[3])
            edges.append(DynamicEdge(u, v, a, b, idx))
            max_node = max(max_node, u, v)
            idx += 1

    return edges, max_node

if __name__ == "__main__":
    print("=== Dynamic Parametric MST Test ===")

    fname = "edges.csv"
    edges, n = load_edges_csv(fname)

    print(f"Loaded {len(edges)} edges, {n} nodes.")

    t_values = range(0, 101)

    print("Calculăm schimbările MST...")

    changes = detect_changes(edges, n, t_values)

    if not changes:
        print("Nu au fost detectate schimbări ale MST în intervalul t.")
    else:
        print(f"Au fost detectate {len(changes)} schimbări ale MST:")
        for t, old_mst, new_mst in changes:
            print("\n--------------------------------")
            print(f"t = {t}")
            print(f"MST vechi = {old_mst}")
            print(f"MST nou  = {new_mst}")
