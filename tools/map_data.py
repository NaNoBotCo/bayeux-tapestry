#!/usr/bin/env python3
"""map_data.py — cuts the English Channel out of Natural Earth's 1:50m land (world-atlas land-50m.json,
public domain) and writes docs/land.js: polygons as [lon, lat] rings, rounded, clipped to the box."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
BOX = (-9.0, 45.0, 8.0, 54.5)  # lon0, lat0, lon1, lat1
topo = json.load(open(os.path.join(HERE, "land-50m.json")))
sx, sy = topo["transform"]["scale"]; tx, ty = topo["transform"]["translate"]
arcs = []
for a in topo["arcs"]:
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy
        pts.append((x * sx + tx, y * sy + ty))
    arcs.append(pts)
def ring(ids):
    out = []
    for i in ids:
        p = arcs[i] if i >= 0 else arcs[~i][::-1]
        out += p[1:] if out else p
    return out
def clip(poly):
    # Sutherland–Hodgman against the box
    def cut(pts, inside, inter):
        res = []
        for i in range(len(pts)):
            a, b = pts[i - 1], pts[i]
            if inside(b):
                if not inside(a): res.append(inter(a, b))
                res.append(b)
            elif inside(a):
                res.append(inter(a, b))
        return res
    x0, y0, x1, y1 = BOX
    def ix(a, b, x): t = (x - a[0]) / (b[0] - a[0]); return (x, a[1] + t * (b[1] - a[1]))
    def iy(a, b, y): t = (y - a[1]) / (b[1] - a[1]); return (a[0] + t * (b[0] - a[0]), y)
    p = poly
    for ins, inter in ((lambda q: q[0] >= x0, lambda a, b: ix(a, b, x0)), (lambda q: q[0] <= x1, lambda a, b: ix(a, b, x1)),
                       (lambda q: q[1] >= y0, lambda a, b: iy(a, b, y0)), (lambda q: q[1] <= y1, lambda a, b: iy(a, b, y1))):
        if not p: break
        p = cut(p, ins, inter)
    return p
polys = []
for g in topo["objects"]["land"]["geometries"]:
    parts = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
    for part in parts:
        r = clip(ring(part[0]))
        if len(r) > 3:
            q = []
            for x, y in r:
                pt = [round(x, 3), round(y, 3)]
                if not q or abs(pt[0] - q[-1][0]) + abs(pt[1] - q[-1][1]) > 0.006:
                    q.append(pt)
            if len(q) > 3: polys.append(q)
open(os.path.join(HERE, "..", "docs", "land.js"), "w").write("window.LAND=" + json.dumps({"box": BOX, "polys": polys}, separators=(",", ":")) + ";\n")
print(len(polys), "polygons", sum(len(p) for p in polys), "points")
