#!/usr/bin/env python3
"""align_strip.py — the Commons scene photographs overlap. For each pair of neighbours, find where the
next tile's left edge sits inside the previous tile (and any vertical shift), so the page can lay the
tiles end to end as one strip. Writes x/dy into tools/strip.json."""
import json, os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "..", "docs", "img", "strip")
rows = json.load(open(os.path.join(HERE, "strip.json")))
def g(f):
    return np.asarray(Image.open(os.path.join(D, f)).convert("L"), dtype=np.float32)
x = 0.0
dy = 0
for k, r in enumerate(rows):
    im = g(r["file"]); r["w"], r["h"] = im.shape[1], im.shape[0]
    if k == 0:
        r["x"], r["dy"] = 0, 0
        continue
    a = g(rows[k - 1]["file"])
    best = None
    tw = 120
    for off in (40, 160):  # try two template positions in case one sits on bare backing
        t = im[60:300, off:off + tw]
        for v in range(-10, 11):
            ta = t
            for s in range(max(0, a.shape[1] - 1600), a.shape[1] - tw):
                y0 = 60 + v
                if y0 < 0 or y0 + 240 > a.shape[0]:
                    continue
                e = float(np.mean(np.abs(a[y0:y0 + 240, s:s + tw] - ta)))
                if best is None or e < best[0]:
                    best = (e, s - off, v)
    e, s, v = best
    dy += v
    r["x"] = rows[k - 1]["x"] + s
    r["dy"] = dy
    print(r["file"], "at", r["x"], "dy", dy, "err %.1f" % e, "overlap", a.shape[1] - s)
json.dump(rows, open(os.path.join(HERE, "strip.json"), "w"), indent=1)
last = rows[-1]
print("strip width", last["x"] + last["w"])
